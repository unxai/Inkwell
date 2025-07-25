<template>
  <div class="text-editor">
    <!-- 编辑器工具栏 -->
    <editor-toolbar :editor="editor" v-if="editor" />
    
    <!-- 编辑器内容区 -->
    <div class="editor-content-wrapper relative" ref="editorContainer">
      <editor-content :editor="editor" class="editor-content prose max-w-none" />
      
      <!-- AI补全建议 -->
      <completion-suggestion
        :suggestion="completionSuggestion"
        :visible="showSuggestion"
        :position="suggestionPosition"
        @accept="acceptSuggestion"
        @reject="rejectSuggestion"
      />
      
      <!-- AI处理中指示器 -->
      <div 
        v-if="aiStatus === 'processing'" 
        class="absolute bottom-4 right-4 bg-white bg-opacity-90 rounded-full shadow-md p-2 flex items-center space-x-2 text-sm text-gray-600 border border-gray-200"
      >
        <svg class="animate-spin h-4 w-4 text-[#4FD1C5]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        <span>AI 思考中...</span>
      </div>
    </div>
    
    <!-- 编辑器底部状态栏 -->
    <div class="py-2 px-4 border-t border-gray-200 flex justify-between items-center text-sm text-gray-500 bg-gray-50">
      <div class="flex items-center space-x-4">
        <span class="flex items-center">
          <svg class="w-4 h-4 mr-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="16" y1="13" x2="8" y2="13"></line>
            <line x1="16" y1="17" x2="8" y2="17"></line>
            <polyline points="10 9 9 9 8 9"></polyline>
          </svg>
          {{ wordCount }} 字
        </span>
        <span class="hidden md:inline-flex items-center">
          <svg class="w-4 h-4 mr-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10"></circle>
            <polyline points="12 6 12 12 16 14"></polyline>
          </svg>
          {{ formatTime(editingTime) }}
        </span>
      </div>
      <div class="flex items-center">
        <span 
          class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
          :class="{
            'bg-green-100 text-green-800': aiStatus === 'idle',
            'bg-yellow-100 text-yellow-800': aiStatus === 'processing',
            'bg-gray-100 text-gray-800': aiStatus !== 'idle' && aiStatus !== 'processing'
          }"
        >
          <span 
            class="w-2 h-2 mr-1.5 rounded-full"
            :class="{
              'bg-green-500': aiStatus === 'idle',
              'bg-yellow-500': aiStatus === 'processing',
              'bg-gray-500': aiStatus !== 'idle' && aiStatus !== 'processing'
            }"
          ></span>
          {{ aiStatus === 'idle' ? 'AI 就绪' : aiStatus === 'processing' ? 'AI 处理中' : 'AI ' + aiStatus }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick, computed } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Placeholder from '@tiptap/extension-placeholder'
import Highlight from '@tiptap/extension-highlight'
import { useEditorStore } from '@/store/modules/editor'
import EditorToolbar from './EditorToolbar.vue'
import CompletionSuggestion from './CompletionSuggestion.vue'

const props = defineProps({
  initialContent: {
    type: String,
    default: '<p>欢迎使用墨井智能写作助手！</p>'
  },
  autoCompleteEnabled: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['update:content', 'text-change', 'completion-accepted', 'completion-rejected'])

// 使用编辑器状态管理
const editorStore = useEditorStore()
const wordCount = ref(0)
const aiStatus = ref('idle')
const editingTime = ref(0) // 编辑时间（秒）
let editingTimer = null

// 自动完成相关状态
const editorContainer = ref(null)
const completionSuggestion = ref('')
const showSuggestion = ref(false)
const suggestionPosition = ref({ top: 0, left: 0 })
const currentCursorPosition = ref(0)

// 格式化时间
const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  
  if (hours > 0) {
    return `${hours}小时 ${minutes}分钟`
  } else if (minutes > 0) {
    return `${minutes}分钟 ${secs}秒`
  } else {
    return `${secs}秒`
  }
}

// 初始化编辑器
const editor = useEditor({
  extensions: [
    StarterKit.configure({
      heading: {
        levels: [1, 2, 3]
      }
    }),
    Placeholder.configure({
      placeholder: '开始写作，或输入 / 使用 AI 辅助功能...'
    }),
    Highlight.configure({
      multicolor: true
    }),
  ],
  content: props.initialContent,
  onUpdate: ({ editor }) => {
    const html = editor.getHTML()
    const text = editor.getText()
    
    // 更新字数统计（中文字符计数）
    wordCount.value = text.replace(/\s+/g, '').length
    
    // 更新状态管理中的内容
    editorStore.updateContent(html)
    // 注意：updateContent 方法已经包含了字数统计的更新
    
    // 向父组件发送更新事件
    emit('update:content', html)
    emit('text-change', text)
    
    // 保存当前光标位置
    if (editor.state.selection) {
      currentCursorPosition.value = editor.state.selection.from
      editorStore.updateCursorPosition(currentCursorPosition.value)
    }
  },
  onSelectionUpdate: ({ editor }) => {
    // 更新光标位置
    if (editor.state.selection) {
      currentCursorPosition.value = editor.state.selection.from
      editorStore.updateCursorPosition(currentCursorPosition.value)
      
      // 如果有建议显示，更新建议位置
      if (showSuggestion.value) {
        updateSuggestionPosition()
      }
    }
  },
  onFocus: () => {
    // 编辑器获得焦点时，开始计时
    if (!editingTimer) {
      editingTimer = setInterval(() => {
        editingTime.value++
      }, 1000)
    }
  },
  onBlur: () => {
    // 编辑器失去焦点时，停止计时
    if (editingTimer) {
      clearInterval(editingTimer)
      editingTimer = null
    }
  }
})

// 监听AI状态变化
watch(() => editorStore.aiStatus, (newStatus) => {
  aiStatus.value = newStatus
})

// 监听编辑器状态管理中的补全内容变化
watch(() => editorStore.completionText, (newCompletion) => {
  if (newCompletion && editor.value) {
    completionSuggestion.value = newCompletion
    showSuggestion.value = true
    nextTick(() => {
      updateSuggestionPosition()
    })
  } else {
    showSuggestion.value = false
  }
})

// 更新建议位置
const updateSuggestionPosition = () => {
  if (!editor.value || !editorContainer.value) return
  
  const { state, view } = editor.value
  const { from } = state.selection
  
  // 获取光标位置的坐标
  const coords = view.coordsAtPos(from)
  
  // 计算相对于编辑器容器的位置
  const containerRect = editorContainer.value.getBoundingClientRect()
  
  suggestionPosition.value = {
    top: coords.top - containerRect.top,
    left: coords.left - containerRect.left
  }
}

// 接受建议
const acceptSuggestion = (suggestion) => {
  if (!editor.value || !suggestion) return
  
  // 在当前光标位置插入建议文本
  editor.value.chain().focus().insertContent(suggestion).run()
  
  // 隐藏建议
  showSuggestion.value = false
  completionSuggestion.value = ''
  
  // 通知父组件建议已接受
  emit('completion-accepted', suggestion)
}

// 拒绝建议
const rejectSuggestion = () => {
  showSuggestion.value = false
  completionSuggestion.value = ''
  
  // 通知父组件建议已拒绝
  emit('completion-rejected')
}

// 处理键盘事件
const handleKeyDown = (event) => {
  // 如果有建议显示
  if (showSuggestion.value && completionSuggestion.value) {
    // Tab键接受建议
    if (event.key === 'Tab') {
      event.preventDefault()
      acceptSuggestion(completionSuggestion.value)
    }
    // Esc键拒绝建议
    else if (event.key === 'Escape') {
      event.preventDefault()
      rejectSuggestion()
    }
  }
}

// 生命周期钩子
onMounted(() => {
  // 添加键盘事件监听
  if (editorContainer.value) {
    editorContainer.value.addEventListener('keydown', handleKeyDown)
  }
})

onBeforeUnmount(() => {
  // 移除键盘事件监听
  if (editorContainer.value) {
    editorContainer.value.removeEventListener('keydown', handleKeyDown)
  }
  
  // 清除计时器
  if (editingTimer) {
    clearInterval(editingTimer)
    editingTimer = null
  }
  
  // 销毁编辑器
  if (editor.value) {
    editor.value.destroy()
  }
})

// 暴露编辑器实例和方法，以便父组件可以访问
defineExpose({
  editor,
  acceptSuggestion,
  rejectSuggestion,
  currentCursorPosition
})
</script>

<style>
.text-editor {
  display: flex;
  flex-direction: column;
  height: 100%;
  border-radius: 0.5rem;
  overflow: hidden;
}

.editor-content-wrapper {
  flex-grow: 1;
  overflow-y: auto;
  padding: 1.5rem;
  background-color: white;
}

.editor-content {
  min-height: 500px;
  outline: none;
}

/* Tiptap编辑器样式 */
.ProseMirror {
  min-height: 500px;
  outline: none;
  font-size: 16px;
  line-height: 1.6;
  color: #333;
}

.ProseMirror p {
  margin-bottom: 1em;
}

.ProseMirror h1 {
  font-size: 1.75rem;
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: #1A365D;
}

.ProseMirror h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-top: 1.25rem;
  margin-bottom: 0.75rem;
  color: #1A365D;
}

.ProseMirror h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-top: 1rem;
  margin-bottom: 0.5rem;
  color: #1A365D;
}

.ProseMirror ul,
.ProseMirror ol {
  padding-left: 1.5rem;
  margin-bottom: 1em;
}

.ProseMirror ul li {
  list-style-type: disc;
  margin-bottom: 0.25em;
}

.ProseMirror ol li {
  list-style-type: decimal;
  margin-bottom: 0.25em;
}

.ProseMirror blockquote {
  border-left: 3px solid #4FD1C5;
  padding-left: 1rem;
  color: #4A5568;
  margin: 1rem 0;
  font-style: italic;
}

.ProseMirror pre {
  background-color: #F7FAFC;
  padding: 0.75rem;
  border-radius: 0.25rem;
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  margin: 1rem 0;
  overflow-x: auto;
}

.ProseMirror code {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  background-color: #F7FAFC;
  padding: 0.1em 0.3em;
  border-radius: 0.2em;
  font-size: 0.9em;
}

.ProseMirror mark {
  background-color: rgba(79, 209, 197, 0.2);
  padding: 0.1em 0;
}

.ProseMirror a {
  color: #4FD1C5;
  text-decoration: underline;
  text-underline-offset: 2px;
}

.ProseMirror p.is-editor-empty:first-child::before {
  content: attr(data-placeholder);
  float: left;
  color: #adb5bd;
  pointer-events: none;
  height: 0;
}

/* 编辑器滚动条样式 */
.editor-content-wrapper::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.editor-content-wrapper::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.editor-content-wrapper::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.editor-content-wrapper::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>