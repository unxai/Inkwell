<template>
  <div class="container mx-auto px-4 py-6">
    <!-- 编辑器顶部工具栏 -->
    <div class="mb-4 flex flex-wrap items-center justify-between gap-4">
      <div class="flex items-center space-x-4">
        <h1 class="text-xl font-semibold text-[#1A365D]">墨井编辑器</h1>
        <div class="flex items-center">
          <span 
            class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
            :class="isConnected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
          >
            <span 
              class="w-2 h-2 mr-1.5 rounded-full"
              :class="isConnected ? 'bg-green-400' : 'bg-red-400'"
            ></span>
            {{ isConnected ? 'AI 已连接' : 'AI 未连接' }}
          </span>
        </div>
      </div>
      
      <div class="flex items-center space-x-4">
        <span class="text-sm text-gray-500">{{ wordCount }} 字</span>
        <button 
          @click="toggleSidebar" 
          class="inline-flex items-center px-3 py-1.5 border border-gray-300 text-sm leading-5 font-medium rounded-md text-gray-700 bg-white hover:text-[#4FD1C5] focus:outline-none focus:border-[#4FD1C5] focus:shadow-outline-blue transition ease-in-out duration-150"
        >
          <svg class="h-4 w-4 mr-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path v-if="!isSidebarOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          {{ isSidebarOpen ? '隐藏面板' : '显示面板' }}
        </button>
      </div>
    </div>
    
    <div class="flex flex-col md:flex-row gap-6">
      <!-- 侧边功能面板 -->
      <transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0 transform -translate-x-4"
        enter-to-class="opacity-100 transform translate-x-0"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100 transform translate-x-0"
        leave-to-class="opacity-0 transform -translate-x-4"
      >
        <div 
          v-show="isSidebarOpen" 
          class="w-full md:w-72 bg-white rounded-lg shadow-md border border-gray-200 p-4 h-fit"
        >
          <ai-assist-panel
            :is-connected="isConnected"
            :ai-status="aiStatus"
            :context-window-before="contextWindowBefore"
            :context-window-after="contextWindowAfter"
            @auto-complete="handleAutoComplete"
            @rewrite="handleRewrite"
            @expand="handleExpand"
            @simplify="handleSimplify"
          />
        </div>
      </transition>
      
      <!-- 主编辑区域 -->
      <div class="flex-1">
        <div class="bg-white rounded-lg shadow-md border border-gray-200 overflow-hidden">
          <text-editor
            ref="textEditorRef"
            :initial-content="editorContent"
            @update:content="handleContentUpdate"
            @text-change="handleTextChange"
            @completion-accepted="handleCompletionAccepted"
            @completion-rejected="handleCompletionRejected"
          />
        </div>
        
        <!-- 编辑器底部状态栏 -->
        <div class="mt-2 flex items-center justify-between text-sm text-gray-500">
          <div class="flex items-center space-x-4">
            <span>{{ aiStatus === 'idle' ? 'AI 就绪' : aiStatus === 'processing' ? 'AI 思考中...' : 'AI 空闲' }}</span>
            <span>上下文窗口: {{ contextWindowBefore }} / {{ contextWindowAfter }} tokens</span>
          </div>
          <div>
            <span>按 Tab 接受建议 | Esc 拒绝建议</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed, watch } from 'vue'
import { useEditorStore } from '@/store/modules/editor'
import { useCompletion } from '@/composables/useCompletion'
import TextEditor from '@/components/editor/TextEditor.vue'
import AiAssistPanel from '@/components/editor/AiAssistPanel.vue'

// 使用编辑器状态管理
const editorStore = useEditorStore()

// 使用文本补全组合式函数
const completion = useCompletion({
  wsUrl: 'ws://localhost:8000/api/v1/completion/ws',
  contextWindowBefore: 1536,
  contextWindowAfter: 256
})

// 编辑器状态
const textEditorRef = ref(null)
const editorContent = ref('<p>欢迎使用墨井智能写作助手！</p>')
const isConnected = computed(() => completion.isConnected)
const aiStatus = computed(() => completion.status)
const contextWindowBefore = computed(() => completion.contextWindowBefore)
const contextWindowAfter = computed(() => completion.contextWindowAfter)
const currentCompletion = ref('')
const isSidebarOpen = ref(true) // 侧边栏默认打开

// 计算属性
const wordCount = computed(() => {
  // 从编辑器内容中提取纯文本并计算字数
  if (textEditorRef.value && textEditorRef.value.editor) {
    const text = textEditorRef.value.editor.getText()
    return text.replace(/\s+/g, '').length
  }
  return editorStore.wordCount || 0
})

// 切换侧边栏显示状态
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

// 监听补全状态变化
watch(() => completion.isConnected, (newValue) => {
  editorStore.setConnectionStatus(newValue)
})

watch(() => completion.status, (newValue) => {
  editorStore.updateAiStatus(newValue)
})

watch(() => completion.currentCompletion, (newValue) => {
  currentCompletion.value = newValue
  
  // 如果有新的补全内容，更新编辑器状态管理中的补全文本
  if (newValue) {
    editorStore.updateCompletionText(newValue)
  }
})

// 监听编辑器状态管理中的补全文本变化
watch(() => editorStore.completionText, (newValue) => {
  // 更新当前补全内容
  currentCompletion.value = newValue
})

// 处理编辑器内容更新
const handleContentUpdate = (content) => {
  editorContent.value = content
}

// 处理文本变化
const handleTextChange = (text) => {
  // 更新编辑器状态管理中的光标位置
  if (textEditorRef.value && textEditorRef.value.editor) {
    const { from } = textEditorRef.value.editor.state.selection
    editorStore.updateCursorPosition(from)
  }
}

// 处理补全接受
const handleCompletionAccepted = (completionText) => {
  // 通知编辑器状态管理补全已接受
  editorStore.acceptCompletion()
}

// 处理补全拒绝
const handleCompletionRejected = () => {
  // 通知编辑器状态管理补全已拒绝
  editorStore.rejectCompletion()
}

// 获取上下文窗口内容
const getContextWindow = (editor) => {
  if (!editor) return { before: '', after: '' }
  
  const { state } = editor
  const { selection } = state
  const { from, to } = selection
  
  // 获取当前位置之前的文本作为上文
  const beforeText = state.doc.textBetween(0, from)
  
  // 获取当前位置之后的文本作为下文
  const afterText = state.doc.textBetween(to, state.doc.content.size)
  
  return {
    before: beforeText,
    after: afterText
  }
}

// AI辅助功能处理方法
const handleAutoComplete = () => {
  const editor = textEditorRef.value.editor
  if (!editor) return
  
  // 获取当前编辑器内容和光标位置
  const currentText = editor.getText()
  const { from } = editor.state.selection
  
  // 获取上下文窗口
  const { before, after } = getContextWindow(editor)
  
  // 请求文本补全，传递光标位置
  completion.requestCompletion(currentText, before, after, from)
}

const handleRewrite = () => {
  const editor = textEditorRef.value.editor
  if (!editor) return
  
  // 获取选中的文本
  const { from, to } = editor.state.selection
  if (from === to) {
    alert('请先选择要改写的文本')
    return
  }
  
  const selectedText = editor.state.doc.textBetween(from, to)
  
  // 使用WebSocket发送改写请求
  if (completion.isConnected) {
    completion.send({
      text: selectedText,
      action: 'rewrite'
    })
    
    // 监听改写结果
    const handleRewriteResult = (data) => {
      if (data.type === 'end' && data.action === 'rewrite') {
        editor.chain().focus().deleteSelection().insertContent(data.completion).run()
        completion.off('completion', handleRewriteResult)
      }
    }
    
    completion.on('completion', handleRewriteResult)
  } else {
    // 如果WebSocket未连接，使用HTTP API
    editorStore.optimizeText(selectedText, 'rewrite')
      .then(optimizedText => {
        editor.chain().focus().deleteSelection().insertContent(optimizedText).run()
      })
      .catch(error => {
        console.error('改写失败:', error)
      })
  }
}

const handleExpand = () => {
  const editor = textEditorRef.value.editor
  if (!editor) return
  
  // 获取选中的文本
  const { from, to } = editor.state.selection
  if (from === to) {
    alert('请先选择要扩写的文本')
    return
  }
  
  const selectedText = editor.state.doc.textBetween(from, to)
  
  // 使用WebSocket发送扩写请求
  if (completion.isConnected) {
    completion.send({
      text: selectedText,
      action: 'expand'
    })
    
    // 监听扩写结果
    const handleExpandResult = (data) => {
      if (data.type === 'end' && data.action === 'expand') {
        editor.chain().focus().deleteSelection().insertContent(data.completion).run()
        completion.off('completion', handleExpandResult)
      }
    }
    
    completion.on('completion', handleExpandResult)
  } else {
    // 如果WebSocket未连接，使用HTTP API
    editorStore.optimizeText(selectedText, 'expand')
      .then(optimizedText => {
        editor.chain().focus().deleteSelection().insertContent(optimizedText).run()
      })
      .catch(error => {
        console.error('扩写失败:', error)
      })
  }
}

const handleSimplify = () => {
  const editor = textEditorRef.value.editor
  if (!editor) return
  
  // 获取选中的文本
  const { from, to } = editor.state.selection
  if (from === to) {
    alert('请先选择要简化的文本')
    return
  }
  
  const selectedText = editor.state.doc.textBetween(from, to)
  
  // 使用WebSocket发送简化请求
  if (completion.isConnected) {
    completion.send({
      text: selectedText,
      action: 'simplify'
    })
    
    // 监听简化结果
    const handleSimplifyResult = (data) => {
      if (data.type === 'end' && data.action === 'simplify') {
        editor.chain().focus().deleteSelection().insertContent(data.completion).run()
        completion.off('completion', handleSimplifyResult)
      }
    }
    
    completion.on('completion', handleSimplifyResult)
  } else {
    // 如果WebSocket未连接，使用HTTP API
    editorStore.optimizeText(selectedText, 'simplify')
      .then(optimizedText => {
        editor.chain().focus().deleteSelection().insertContent(optimizedText).run()
      })
      .catch(error => {
        console.error('简化失败:', error)
      })
  }
}

// 生命周期钩子
onMounted(() => {
  // WebSocket连接已经在useCompletion中自动建立
})

onBeforeUnmount(() => {
  // 断开WebSocket连接
  completion.disconnect()
})
</script>
