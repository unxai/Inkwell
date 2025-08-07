<template>
  <div class="text-editor h-full">
    
    <!-- 编辑器内容区 -->
    <div class="editor-content-wrapper relative h-full w-full paper-effect" ref="editorContainer">
      <editor-content :editor="editor" class="editor-content prose max-w-none h-full" />
      
      <!-- AI补全建议 -->
      <completion-suggestion
        :suggestion="completionSuggestion"
        :visible="showSuggestion"
        :position="suggestionPosition"
        @accept="acceptSuggestion"
        @reject="rejectSuggestion"
        @regenerate="regenerateSuggestion"
      />
      
      <!-- AI操作提示指示器 -->
      <div 
        v-if="showSuggestion || aiStatus === 'processing'" 
        class="absolute bottom-4 right-4 bg-white bg-opacity-90 rounded-full shadow-md p-2 flex items-center space-x-2 text-sm text-gray-600 border border-gray-200"
      >
        <div v-if="aiStatus === 'processing'" class="flex items-center space-x-2">
          <svg class="animate-spin h-4 w-4 text-[#4FD1C5]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>生成中...</span>
        </div>
        <div v-else-if="showSuggestion" class="flex items-center space-x-2">
          <svg class="h-4 w-4 text-[#4FD1C5]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
          <span>Tab: 接受 | Esc: 拒绝</span>
        </div>
      </div>
      
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
    
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Placeholder from '@tiptap/extension-placeholder'
import Highlight from '@tiptap/extension-highlight'
import { useEditorStore } from '@/store/modules/editor'
import CompletionSuggestion from './CompletionSuggestion.vue'

const props = defineProps({
  initialContent: {
    type: String,
    default: '<p>欢迎使用墨井智能写作助手！</p>'
  },
  autoCompleteEnabled: {
    type: Boolean,
    default: true
  },
  isConnected: {
    type: Boolean,
    default: false
  },
  references: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits([
  'update:content',
  'text-change',
  'completion-accepted',
  'completion-rejected',
  'selection-change',
  'show-floating-toolbar',
  'hide-floating-toolbar',
  'request-completion'
])

// 使用编辑器状态管理
const editorStore = useEditorStore()
const wordCount = ref(0)
const aiStatus = ref('idle')
// 文本选择状态
const selectedText = ref('')
const selectionRange = ref({ from: 0, to: 0 })

// 编辑时间
const editingTime = ref(0)
let editingTimer = null

// 自动完成相关状态
const editorContainer = ref(null)
const completionSuggestion = ref('')
const showSuggestion = ref(false)
const suggestionPosition = ref({ top: 0, left: 0 })
const currentCursorPosition = ref(0)
const typingTimer = ref(null) // 用户输入定时器
const showToolbarTimeout = ref(null) // 浮动工具条显示延迟定时器
const typingDelay = 1000 // 用户停止输入后等待时间(毫秒)
const lastCompletionTime = ref(0) // 上次请求补全的时间
const completionCooldown = 3000 // 补全请求冷却时间(毫秒)

// 监听文本选择变化
const handleSelectionUpdate = ({ editor }) => {
  const { state } = editor
  const { selection } = state
  const { from, to } = selection
  
  // 更新选择范围
  selectionRange.value = { from, to }
  
  // 获取选中的文本
  const text = state.doc.textBetween(from, to)
  selectedText.value = text
  
  // 发送选择变化事件
  emit('selection-change', {
    text,
    from,
    to,
    hasSelection: from !== to
  })
  
  // 如果有选中文本，显示浮动工具条
  if (text.trim() && from !== to && text.trim().length >= 2) { // 至少选择2个字符才显示
    // 获取选择位置的坐标
    try {
      // 获取选择的开始和结束位置坐标
      const startCoords = editor.view.coordsAtPos(from)
      const endCoords = editor.view.coordsAtPos(to)
      const containerRect = editorContainer.value?.getBoundingClientRect()
      
      if (containerRect) {
        // 计算选择文本的中心位置
        const selectionCenterX = (startCoords.left + endCoords.left) / 2
        const selectionTop = startCoords.top
        
        // 工具条尺寸估算 - 减少估算宽度
        const toolbarWidth = 350  // 调整为更精确的宽度
        const toolbarHeight = 50
        const margin = 10
        
        // 计算相对于编辑器容器的位置
        let left = selectionCenterX - containerRect.left - (toolbarWidth / 2)
        let top = selectionTop - containerRect.top - toolbarHeight - margin
        
        // 获取编辑器容器的实际宽度
        const containerWidth = containerRect.width
        
        // 防止工具条超出左边界
        if (left < margin) {
          left = margin
        }
        // 防止工具条超出右边界
        else if (left + toolbarWidth > containerWidth - margin) {
          left = containerWidth - toolbarWidth - margin
        }
        
        // 防止工具条超出上边界，如果上方空间不够，显示在选择文本下方
        if (top < margin) {
          // 获取选择区域底部位置
          const selectionBottom = Math.max(startCoords.bottom, endCoords.bottom)
          top = selectionBottom - containerRect.top + margin
        }
        
        const position = { top, left }
        
        // 调试信息
        console.log('浮动工具条位置计算:', {
          selectionCenterX,
          selectionTop,
          containerRect,
          toolbarWidth,
          calculatedPosition: position,
          selectedText: text
        })
        
        // 延迟显示工具条，避免快速选择时的闪烁
        clearTimeout(showToolbarTimeout)
        showToolbarTimeout = setTimeout(() => {
          emit('show-floating-toolbar', {
            position,
            selectedText: text,
            selectionRange: { from, to }
          })
        }, 200) // 200ms 延迟
      }
    } catch (error) {
      console.warn('无法计算浮动工具条位置:', error)
    }
  } else {
    // 清除延迟显示的定时器
    clearTimeout(showToolbarTimeout)
    emit('hide-floating-toolbar')
  }
  
  // 更新光标位置
  currentCursorPosition.value = from
  editorStore.updateCursorPosition(from)
  
  // 如果有建议显示，更新建议位置
  if (showSuggestion.value) {
    updateSuggestionPosition()
  }
}

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
    
    // 如果启用了自动完成，设置定时器
    if (props.autoCompleteEnabled) {
      // 清除之前的定时器
      if (typingTimer.value) {
        clearTimeout(typingTimer.value)
      }
      
      // 设置新的定时器，用户停止输入后触发
      typingTimer.value = setTimeout(() => {
        triggerAutoCompletion()
      }, typingDelay)
    }
  },
  onSelectionUpdate: handleSelectionUpdate,
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
    // 延迟隐藏浮动工具条，给用户时间点击工具条
    setTimeout(() => {
      emit('hide-floating-toolbar')
    }, 150)
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

// 在 TextEditor.vue 中添加以下优化

// 更新建议位置计算函数
const updateSuggestionPosition = () => {
  if (!editor.value || !editorContainer.value) return
  
  const { state, view } = editor.value
  const { from } = state.selection
  
  try {
    // 获取光标位置的坐标
    const coords = view.coordsAtPos(from)
    
    // 计算相对于编辑器容器的位置
    const containerRect = editorContainer.value.getBoundingClientRect()
    
    suggestionPosition.value = {
      top: coords.top - containerRect.top + window.scrollY,
      left: coords.left - containerRect.left + window.scrollX
    }
  } catch (error) {
    console.warn('无法计算建议位置:', error)
    // 使用默认位置
    suggestionPosition.value = { top: 100, left: 100 }
  }
}

// 添加重新生成建议的方法
const regenerateSuggestion = () => {
  if (!editor.value) return
  
  // 清除当前建议
  showSuggestion.value = false
  completionSuggestion.value = ''
  
  // 重新触发自动完成
  setTimeout(() => {
    triggerAutoCompletion()
  }, 100)
}

// 优化触发自动完成的逻辑
const triggerAutoCompletion = () => {
  if (!editor.value || aiStatus.value === 'processing') return
  
  const now = Date.now()
  // 检查是否在冷却期内
  if (now - lastCompletionTime.value < completionCooldown) {
    return
  }
  
  const { state } = editor.value
  const { from } = state.selection
  const text = editor.value.getText()
  
  // 获取光标前后的上下文
  const contextBefore = text.slice(0, from)
  const contextAfter = text.slice(from)
  
  // 改进触发条件 - 添加更严格的检查
  if (!contextBefore.trim() || contextBefore.length < 10) return
  
  // 检查是否在句子中间（避免在单词中间触发）
  const lastChar = contextBefore.slice(-1)
  const isAtWordEnd = /[\s\.,;:!?。，；：！？]/.test(lastChar)
  
  if (!isAtWordEnd && contextBefore.length > 20) {
    // 如果不在单词结尾，检查是否有足够的上下文
    const words = contextBefore.trim().split(/\s+/)
    if (words.length < 5) return
  }
  
  // 检查编辑器是否仍然处于活动状态
  if (!editor.value.isFocused) {
    return
  }
  
  // 检查当前是否有选中的文本，如果有则不触发自动完成
  if (from !== state.selection.to) {
    return
  }
  
  // 更新上次请求时间
  lastCompletionTime.value = now
  
  // 设置AI状态为处理中
  editorStore.updateAiStatus('processing')
  
  // 请求补全
  emit('request-completion', {
    text: contextBefore,
    contextBefore,
    contextAfter,
    cursorPosition: from
  })
}

// 更新键盘事件处理
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
    // Ctrl+R 重新生成
    else if (event.ctrlKey && event.key === 'r') {
      event.preventDefault()
      regenerateSuggestion()
    }
  }
}

// 在模板中更新 CompletionSuggestion 组件
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
  
  // 清除输入定时器
  if (typingTimer.value) {
    clearTimeout(typingTimer.value)
    typingTimer.value = null
  }
  
  // 清除浮动工具条显示定时器
  if (showToolbarTimeout.value) {
    clearTimeout(showToolbarTimeout.value)
    showToolbarTimeout.value = null
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
  currentCursorPosition,
  selectedText,
  selectionRange
})
</script>

<style>
.text-editor {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.editor-content-wrapper {
  flex-grow: 1;
  overflow-y: auto;
  padding: 1rem 1rem; /* 减少内边距，让内容区域更大 */
  background-color: #f9f9f9;
  height: calc(100vh - 180px); /* 调整编辑器高度，确保不会太高 */
}

.paper-effect {
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
  border-radius: 2px;
  max-width: 95%; /* 将编辑器宽度设置为95% */
  margin: 0 auto;
  padding: 40px 60px;
  position: relative;
  min-height: calc(100% - 40px);
}

.paper-effect::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(to right, transparent, rgba(79, 209, 197, 0.3), transparent);
}

.editor-content {
  height: 100%;
  outline: none;
}

/* Tiptap编辑器样式 */
.ProseMirror {
  height: 100%;
  outline: none;
  font-size: 16px;
  line-height: 1.8;
  color: #333;
  font-family: 'Noto Serif SC', serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
  letter-spacing: 0.02em;
  min-height: 400px; /* 调整编辑器的最小高度 */
}

.ProseMirror p {
  margin-bottom: 1.2em;
  text-align: justify;
}

.ProseMirror h1 {
  font-size: 1.8rem;
  font-weight: 600;
  margin-top: 1.8rem;
  margin-bottom: 1.2rem;
  color: #1A365D;
  border-bottom: 1px solid #eaeaea;
  padding-bottom: 0.3rem;
}

.ProseMirror h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: #1A365D;
}

.ProseMirror h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-top: 1.2rem;
  margin-bottom: 0.8rem;
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
  padding: 0.5rem 1rem;
  color: #4A5568;
  margin: 1.5rem 0;
  font-style: italic;
  background-color: rgba(79, 209, 197, 0.05);
  border-radius: 0 4px 4px 0;
}

.ProseMirror pre {
  background-color: #F7FAFC;
  padding: 1rem;
  border-radius: 0.25rem;
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  margin: 1.5rem 0;
  overflow-x: auto;
  border: 1px solid #edf2f7;
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