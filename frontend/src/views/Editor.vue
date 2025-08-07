<template>
  <div class="min-h-screen bg-white flex flex-col">

    <div class="border-b border-gray-200 px-4 py-2 bg-white shadow-sm">
      <div class="flex items-center justify-between gap-4">
        <div class="flex items-center space-x-4">
          <h1 class="text-xl font-semibold text-[#1A365D]">墨井</h1>
          <div class="flex items-center">
            <span 
              class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
              :class="isConnected.value ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
            >
              <span 
                class="w-2 h-2 mr-1 rounded-full"
                :class="isConnected.value ? 'bg-green-400' : 'bg-red-400'"
              ></span>
              {{ isConnected.value ? 'AI 已连接' : 'AI 未连接' }}
            </span>
          </div>
        </div>
        
        <div class="flex items-center">
          <!-- 工具组 1: 文档工具 -->
          <div class="flex items-center space-x-2 mr-4">
            <button
              @click="showVersionHistory = !showVersionHistory"
              :class="showVersionHistory ? 'bg-yellow-100 text-yellow-700 border-yellow-200' : 'text-gray-600 hover:text-gray-800 border-gray-200 hover:bg-gray-50'"
              class="flex items-center px-3 py-2 rounded-lg transition-colors duration-200 border text-sm"
              title="版本历史"
            >
              <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              版本历史
            </button>
            <button
              @click="showExportPanel = !showExportPanel"
              :class="showExportPanel ? 'bg-blue-100 text-blue-700 border-blue-200' : 'text-gray-600 hover:text-gray-800 border-gray-200 hover:bg-gray-50'"
              class="flex items-center px-3 py-2 rounded-lg transition-colors duration-200 border text-sm"
              title="导出文档"
            >
              <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
              导出文档
            </button>
          </div>
          
          <!-- 工具组 2: 学术工具 -->
          <div class="flex items-center space-x-2 mr-4">
            <button
              @click="showCitationManager = !showCitationManager"
              :class="showCitationManager ? 'bg-emerald-100 text-emerald-700 border-emerald-200' : 'text-gray-600 hover:text-gray-800 border-gray-200 hover:bg-gray-50'"
              class="flex items-center px-3 py-2 rounded-lg transition-colors duration-200 border text-sm"
              title="引用管理"
            >
              <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
              引用管理
            </button>
            <button
              @click="showResearchPanel = !showResearchPanel"
              :class="showResearchPanel ? 'bg-green-100 text-green-700 border-green-200' : 'text-gray-600 hover:text-gray-800 border-gray-200 hover:bg-gray-50'"
              class="flex items-center px-3 py-2 rounded-lg transition-colors duration-200 border text-sm"
              title="研究助手"
            >
              <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
              研究助手
            </button>
          </div>
          
          <!-- 工具组 3: AI 和模板工具 -->
          <div class="flex items-center space-x-2 mr-4">
            <button
              @click="showTemplatesPanel = !showTemplatesPanel"
              :class="showTemplatesPanel ? 'bg-purple-100 text-purple-700 border-purple-200' : 'text-gray-600 hover:text-gray-800 border-gray-200 hover:bg-gray-50'"
              class="flex items-center px-3 py-2 rounded-lg transition-colors duration-200 border text-sm"
              title="文档模板"
            >
              <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
              文档模板
            </button>
          </div>
          
          <!-- 开始写作按钮 -->
          <button
            @click="showOutlineGenerator = true"
            class="px-4 py-2 bg-[#4FD1C5] text-white rounded-lg hover:bg-[#3DB9B0] transition-colors font-medium mr-4"
          >
            🚀 开始写作
          </button>
        </div>
        
        <!-- AI聊天面板固定在右侧 -->
        <div class="flex items-center">
          <button
            @click="showChatPanel = !showChatPanel"
            :class="showChatPanel ? 'bg-blue-100 text-blue-700 border-blue-200' : 'text-gray-600 hover:text-gray-800 border-gray-200 hover:bg-gray-50'"
            class="flex items-center px-3 py-2 rounded-lg transition-colors duration-200 border text-sm"
            title="AI 聊天助手"
          >
            <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
            </svg>
            AI 助手
          </button>
        </div>
      </div>
    </div>
    
    <div class="flex flex-grow h-full relative">
      <!-- 左侧面板区域 -->
      <div class="flex">
        <!-- 版本历史面板 -->
        <div 
          v-if="showVersionHistory" 
          class="w-80 border-r border-gray-200 bg-white flex-shrink-0 z-10"
        >
          <version-history-panel
            :current-content="editorContent"
            :word-count="wordCount"
            @toggle-panel="showVersionHistory = false"
            @restore-version="handleRestoreVersion"
          />
        </div>
        
        <!-- 导出面板 -->
        <div 
          v-if="showExportPanel" 
          class="w-80 border-r border-gray-200 bg-white flex-shrink-0 z-10"
        >
          <export-panel
            :document-content="editorContent"
            :word-count="wordCount"
            :references="references"
            @toggle-panel="showExportPanel = false"
          />
        </div>
        
        <!-- 引用管理面板 -->
        <div 
          v-if="showCitationManager" 
          class="w-80 border-r border-gray-200 bg-white flex-shrink-0 z-10"
        >
          <citation-manager
            :references="references"
            @toggle-panel="showCitationManager = false"
            @add-reference="handleAddReference"
            @update-reference="handleUpdateReference"
            @delete-reference="handleDeleteReference"
            @insert-text="handleChatInsertText"
          />
        </div>
        
        <!-- 研究助手面板 -->
        <div 
          v-if="showResearchPanel" 
          class="w-80 border-r border-gray-200 bg-white flex-shrink-0 z-10"
        >
          <research-panel
            @toggle-panel="showResearchPanel = false"
            @add-reference="handleAddReference"
            @insert-text="handleChatInsertText"
          />
        </div>
        
        <!-- 模板面板 -->
        <div 
          v-if="showTemplatesPanel" 
          class="w-80 border-r border-gray-200 bg-white flex-shrink-0 z-10"
        >
          <templates-panel
            @toggle-panel="showTemplatesPanel = false"
            @use-template="handleUseTemplate"
          />
        </div>
      </div>
      
      <!-- 主编辑区域 -->
      <div class="flex-1 flex flex-col h-full overflow-hidden relative">
        <div class="flex-1 bg-white overflow-hidden relative">
          <text-editor
            ref="textEditorRef"
            :initial-content="editorContent"
            :auto-complete-enabled="false"
            :is-connected="isConnected.value"
            :references="references"
            @update:content="handleContentUpdate"
            @text-change="handleTextChange"
            @completion-accepted="handleCompletionAccepted"
            @completion-rejected="handleCompletionRejected"
            @selection-change="handleSelectionChange"
            @show-floating-toolbar="showFloatingToolbar"
            @hide-floating-toolbar="hideFloatingToolbar"
            @request-completion="handleRequestCompletion"
          />
          
          <!-- 浮动工具条 -->
          <floating-toolbar
            :show="showFloatingMenu"
            :position="floatingMenuPosition"
            :selected-text="selectedText"
            :is-processing="isAiProcessing"
            :processing-type="aiProcessingType"
            @action="handleFloatingAction"
          />
        </div>
        
        <!-- 底部工具栏 -->
        <bottom-toolbar 
          :editor="textEditorRef?.editor"
          :is-connected="isConnected.value"
          :ai-status="aiStatus.value"
          :word-count="wordCount"
          @format="handleFormat"
        />
      </div>
      
      <!-- AI 聊天助手面板 - 固定右侧 -->
      <div 
        v-if="showChatPanel" 
        class="w-80 border-l border-gray-200 bg-white flex-shrink-0 z-10"
      >
        <ai-chat-panel
          :is-connected="isConnected.value"
          :current-document="editorContent"
          @toggle-panel="showChatPanel = false"
          @insert-text="handleChatInsertText"
        />
      </div>
      
      <!-- 大纲生成弹层 -->
      <div 
        v-if="showOutlineGenerator" 
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
        @click="!isGeneratingOutline && (showOutlineGenerator = false)"
      >
        <div 
          class="bg-white rounded-lg p-6 max-w-md w-full mx-4 relative"
          @click.stop
        >
          <!-- Loading 遮罩 -->
          <div 
            v-if="isGeneratingOutline"
            class="absolute inset-0 bg-white bg-opacity-80 flex items-center justify-center rounded-lg z-10"
          >
            <div class="flex flex-col items-center">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-[#4FD1C5]"></div>
              <p class="mt-2 text-sm text-gray-600">AI正在智能生成大纲...</p>
            </div>
          </div>
          
          <h3 class="text-lg font-semibold mb-4">🎯 开始您的写作之旅</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">写作主题</label>
              <input 
                v-model="outlineTopicInput"
                type="text" 
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#4FD1C5]"
                placeholder="请输入您想要写作的主题或问题"
                :disabled="isGeneratingOutline"
                @keyup.enter="!isGeneratingOutline && generateOutlineFromTopic()"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">文档类型</label>
              <select 
                v-model="selectedDocumentType" 
                :disabled="isGeneratingOutline"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#4FD1C5] disabled:bg-gray-100"
              >
                <option value="essay">论文/论述文</option>
                <option value="research">研究报告</option>
                <option value="business">商业文档</option>
                <option value="creative">创意写作</option>
                <option value="technical">技术文档</option>
              </select>
            </div>
            <div class="flex space-x-3">
              <button 
                @click="generateOutlineFromTopic"
                :disabled="!outlineTopicInput.trim() || isGeneratingOutline"
                class="flex-1 px-4 py-2 bg-[#4FD1C5] text-white rounded-md hover:bg-[#3DB9B0] disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
              >
                <span v-if="!isGeneratingOutline">🤖 AI 生成大纲</span>
                <span v-else class="flex items-center">
                  <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  生成中...
                </span>
              </button>
              <button 
                @click="skipOutlineGeneration"
                :disabled="isGeneratingOutline"
                class="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                直接开始
              </button>
            </div>
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
import AiChatPanel from '@/components/editor/AiChatPanel.vue'
import TemplatesPanel from '@/components/editor/TemplatesPanel.vue'
import ResearchPanel from '@/components/editor/ResearchPanel.vue'
import CitationManager from '@/components/editor/CitationManager.vue'
import ExportPanel from '@/components/editor/ExportPanel.vue'
import VersionHistoryPanel from '@/components/editor/VersionHistoryPanel.vue'
import BottomToolbar from '@/components/editor/BottomToolbar.vue'
import FloatingToolbar from '@/components/editor/FloatingToolbar.vue'
import { showSuccess, showError } from '@/utils/toast-service'

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
const currentCompletion = ref('')

// UI 面板控制 - 默认打开AI聊天和引用管理
const showChatPanel = ref(true) // AI聊天面板默认显示
const showTemplatesPanel = ref(false) // 模板面板显示状态  
const showResearchPanel = ref(false) // 研究面板显示状态
const showCitationManager = ref(true) // 引用管理面板默认显示
const showExportPanel = ref(false) // 导出面板显示状态
const showVersionHistory = ref(false) // 版本历史面板显示状态

// 大纲生成器状态
const showOutlineGenerator = ref(false) // 默认不显示大纲生成器
const outlineTopicInput = ref('')
const selectedDocumentType = ref('essay')
const isGeneratingOutline = ref(false) // 添加大纲生成loading状态

// 浮动工具条状态
const showFloatingMenu = ref(false)
const floatingMenuPosition = ref({ top: 0, left: 0 })
const selectedText = ref('')
const currentSelection = ref({ from: 0, to: 0 })

// AI操作loading状态
const isAiProcessing = ref(false)
const aiProcessingType = ref('') // 记录当前处理的类型

// 大纲状态
const outline = ref([])
const newOutlineItem = ref({
  title: '',
  level: 1
})

// 参考文献状态
const citationStyle = ref('apa')
const references = ref([])
const newReference = ref({
  author: '',
  title: '',
  publisher: '',
  year: ''
})
const canAddReference = computed(() => {
  return newReference.value.author && 
         newReference.value.title && 
         newReference.value.publisher && 
         newReference.value.year
})

// 学术结构状态
const paperType = ref('research')
const discipline = ref('science')
const academicTitle = ref('')
const structure = ref(null)
const formattedStructure = computed(() => {
  if (!structure.value) return ''
  
  // 将结构转换为HTML
  let html = `<h3 class="text-sm font-bold mb-2">${structure.value.title}</h3>`
  
  // 添加摘要
  if (structure.value.abstract) {
    html += `<div class="mb-3">
      <h4 class="text-xs font-semibold mb-1">摘要</h4>
      <p class="text-xs text-gray-700">${structure.value.abstract}</p>
    </div>`
  }
  
  // 添加章节
  if (structure.value.sections && structure.value.sections.length > 0) {
    html += `<div class="mb-3">
      <h4 class="text-xs font-semibold mb-1">章节结构</h4>
      <ul class="list-disc pl-4 space-y-1 text-xs">`
    
    structure.value.sections.forEach(section => {
      html += `<li>
        <div class="font-medium">${section.title}</div>`
      
      if (section.description) {
        html += `<div class="text-xs text-gray-600">${section.description}</div>`
      }
      
      if (section.subsections && section.subsections.length > 0) {
        html += `<ul class="list-circle pl-4 mt-1 space-y-1">`
        section.subsections.forEach(subsection => {
          html += `<li>
            <div class="font-medium">${subsection.title}</div>`
          
          if (subsection.description) {
            html += `<div class="text-xs text-gray-600">${subsection.description}</div>`
          }
          
          html += `</li>`
        })
        html += `</ul>`
      }
      
      html += `</li>`
    })
    
    html += `</ul></div>`
  }
  
  return html
})

// 样式调整状态已移除

// 计算属性
const wordCount = computed(() => {
  // 从编辑器内容中提取纯文本并计算字数
  if (textEditorRef.value && textEditorRef.value.editor) {
    const text = textEditorRef.value.editor.getText()
    return text.replace(/\s+/g, '').length
  }
  return editorStore.wordCount || 0
})



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
  
  // 如果补全完成，清除auto-complete的loading状态
  if (newValue && aiProcessingType.value === 'auto-complete') {
    isAiProcessing.value = false
    aiProcessingType.value = ''
  }
})

// 监听编辑器状态管理中的补全文本变化
watch(() => editorStore.completionText, (newValue) => {
  // 更新当前补全内容
  currentCompletion.value = newValue
})

// 处理自动完成请求
const handleRequestCompletion = (data) => {
  // 检查AI连接状态
  if (!isConnected.value) {
    console.warn('AI服务未连接，跳过自动完成请求')
    return
  }
  
  // 检查是否已经在处理中
  if (completion.isGenerating.value || aiStatus.value === 'processing') {
    console.log('正在处理其他AI请求，跳过自动完成')
    return
  }
  
  // 检查文本内容长度
  if (!data.text || data.text.length < 10) {
    console.log('文本内容过短，跳过自动完成')
    return
  }
  
  // 使用completion组合式函数请求自动完成
  const success = completion.requestCompletion(
    data.text,
    data.contextBefore,
    data.contextAfter,
    data.cursorPosition
  )
  
  if (!success) {
    console.warn('自动完成请求失败')
  }
}

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

//処理补全拒绝
const handleCompletionRejected = () => {
  // 通知编辑器状态管理补全已拒绝
  editorStore.rejectCompletion()
}

// 处理AI聊天面板插入文本
const handleChatInsertText = (text) => {
  const editor = textEditorRef.value?.editor
  if (!editor || !text) return
  
  // 在当前光标位置插入文本
  editor.chain().focus().insertContent(text).run()
  showSuccess('文本已插入')
}

// 处理使用模板
const handleUseTemplate = (template) => {
  const editor = textEditorRef.value?.editor
  if (!editor || !template?.content) return
  
  // 设置编辑器内容为模板内容
  editor.commands.setContent(template.content)
  editorContent.value = template.content
  
  // 关闭模板面板
  showTemplatesPanel.value = false
  
  showSuccess(`已应用模板: ${template.name}`)
}

// 处理添加引用
const handleAddReference = (reference) => {
  if (!reference) return
  
  // 添加到引用列表
  references.value.push(reference)
  
  showSuccess(`已添加引用: ${reference.title}`)
}

// 处理更新引用
const handleUpdateReference = (index, reference) => {
  if (index >= 0 && index < references.value.length) {
    references.value[index] = reference
    showSuccess('引用已更新')
  }
}

// 处理删除引用
const handleDeleteReference = (index) => {
  if (index >= 0 && index < references.value.length) {
    references.value.splice(index, 1)
    showSuccess('引用已删除')
  }
}

// 处理版本恢复
const handleRestoreVersion = (content) => {
  const editor = textEditorRef.value?.editor
  if (!editor || !content) return
  
  // 设置编辑器内容为恢复的版本
  editor.commands.setContent(content)
  editorContent.value = content
  
  // 关闭版本历史面板
  showVersionHistory.value = false
  
  showSuccess('版本已恢复')
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

// 获取增强的上下文窗口内容 - 更智能的上下文提取
const getEnhancedContextWindow = (editor, cursorPosition) => {
  if (!editor) return { before: '', after: '' }
  
  const { state } = editor
  const text = state.doc.toString()
  
  // 设置上下文窗口大小（字符数）
  const beforeWindowSize = 1500  // 前文1500字符
  const afterWindowSize = 300    // 后文300字符
  
  // 计算前文开始位置
  const beforeStart = Math.max(0, cursorPosition - beforeWindowSize)
  let beforeText = text.substring(beforeStart, cursorPosition)
  
  // 如果前文被截断，尽量从完整的句子开始
  if (beforeStart > 0) {
    const sentenceStart = beforeText.search(/[。！？\n]\s*/)
    if (sentenceStart !== -1) {
      beforeText = beforeText.substring(sentenceStart + 1)
    }
  }
  
  // 计算后文结束位置
  const afterEnd = Math.min(text.length, cursorPosition + afterWindowSize)
  let afterText = text.substring(cursorPosition, afterEnd)
  
  // 如果后文被截断，尽量在完整的句子结束
  if (afterEnd < text.length) {
    const sentenceEnd = afterText.search(/[。！？\n]/)
    if (sentenceEnd !== -1) {
      afterText = afterText.substring(0, sentenceEnd + 1)
    }
  }
  
  return {
    before: beforeText.trim(),
    after: afterText.trim()
  }
}

// AI辅助功能处理方法
const handleAutoComplete = async () => {
  const editor = textEditorRef.value.editor
  if (!editor) return
  
  // 检查AI连接状态
  if (!isConnected.value) {
    showError('AI服务未连接，无法使用自动完成功能')
    return
  }
  
  // 获取当前编辑器内容和光标位置
  const currentText = editor.getText()
  const { from } = editor.state.selection
  
  // 检查是否有足够的文本内容
  if (!currentText.trim() || currentText.trim().length < 10) {
    showError('请输入更多文本内容以使用智能续写功能')
    return
  }
  
  // 设置loading状态
  isAiProcessing.value = true
  aiProcessingType.value = 'auto-complete'
  
  try {
    // 获取上下文窗口 - 改进版本，获取更智能的上下文
    const contextWindow = getEnhancedContextWindow(editor, from)
    const { before, after } = contextWindow
    
    // 显示加载状态
    editorStore.updateAiStatus('智能续写中...')
    
    // 请求文本补全，传递更详细的上下文信息
    completion.requestCompletion(currentText, before, after, from)
  } catch (error) {
    console.error('智能续写失败:', error)
    showError('智能续写失败，请重试')
  } finally {
    // 清除loading状态
    isAiProcessing.value = false
    aiProcessingType.value = ''
  }
}

const handleSimplify = async () => {
  const editor = textEditorRef.value.editor
  if (!editor) return
  
  // 检查是否有选中文本
  const { from, to } = editor.state.selection
  if (from === to || !selectedText.value.trim()) {
    showError('请先选择要简化的文本')
    return
  }
  
  // 检查AI连接状态
  if (!isConnected.value) {
    showError('AI服务未连接，无法使用简化功能')
    return
  }
  
  // 设置loading状态
  isAiProcessing.value = true
  aiProcessingType.value = 'simplify'
  
  try {
    // 调用后端API进行文本简化
    const response = await fetch('/api/v1/completion/optimize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: selectedText.value,
        action: 'simplify',
        context_before: editor.state.doc.textBetween(0, from),
        context_after: editor.state.doc.textBetween(to, editor.state.doc.content.size)
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    
    if (data.completion) {
      // 替换选中的文本
      editor.chain().focus().deleteSelection().insertContent(data.completion).run()
      showSuccess('文本简化完成')
    } else {
      throw new Error('未收到简化结果')
    }
  } catch (error) {
    console.error('简化失败:', error)
    showError('简化失败，请重试')
  } finally {
    // 清除loading状态
    isAiProcessing.value = false
    aiProcessingType.value = ''
  }
}

const handleRewrite = async () => {
  const editor = textEditorRef.value.editor
  if (!editor) return
  
  // 检查是否有选中文本
  const { from, to } = editor.state.selection
  if (from === to || !selectedText.value.trim()) {
    showError('请先选择要改写的文本')
    return
  }
  
  // 检查AI连接状态
  if (!isConnected.value) {
    showError('AI服务未连接，无法使用改写功能')
    return
  }
  
  // 设置loading状态
  isAiProcessing.value = true
  aiProcessingType.value = 'rewrite'
  
  try {
    // 调用后端API进行文本改写
    const response = await fetch('/api/v1/completion/optimize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: selectedText.value,
        action: 'rewrite',
        context_before: editor.state.doc.textBetween(0, from),
        context_after: editor.state.doc.textBetween(to, editor.state.doc.content.size)
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    
    if (data.completion) {
      // 替换选中的文本
      editor.chain().focus().deleteSelection().insertContent(data.completion).run()
      showSuccess('文本改写完成')
    } else {
      throw new Error('未收到改写结果')
    }
  } catch (error) {
    console.error('改写失败:', error)
    showError('改写失败，请重试')
  } finally {
    // 清除loading状态
    isAiProcessing.value = false
    aiProcessingType.value = ''
  }
}

const handleExpand = async () => {
  const editor = textEditorRef.value.editor
  if (!editor) return
  
  // 检查是否有选中文本
  const { from, to } = editor.state.selection
  if (from === to || !selectedText.value.trim()) {
    showError('请先选择要扩写的文本')
    return
  }
  
  // 检查AI连接状态
  if (!isConnected.value) {
    showError('AI服务未连接，无法使用扩写功能')
    return
  }
  
  // 设置loading状态
  isAiProcessing.value = true
  aiProcessingType.value = 'expand'
  
  try {
    // 调用后端API进行文本扩写
    const response = await fetch('/api/v1/completion/optimize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: selectedText.value,
        action: 'expand',
        context_before: editor.state.doc.textBetween(0, from),
        context_after: editor.state.doc.textBetween(to, editor.state.doc.content.size)
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    
    if (data.completion) {
      // 替换选中的文本
      editor.chain().focus().deleteSelection().insertContent(data.completion).run()
      showSuccess('文本扩写完成')
    } else {
      throw new Error('未收到扩写结果')
    }
  } catch (error) {
    console.error('扩写失败:', error)
    showError('扩写失败，请重试')
  } finally {
    // 清除loading状态
    isAiProcessing.value = false
    aiProcessingType.value = ''
  }
}

const handleTranslate = async () => {
  const editor = textEditorRef.value.editor
  if (!editor) return
  
  // 调试信息
  console.log('=== 翻译功能被调用 ===')
  console.log('Selected text:', selectedText.value)
  
  // 检查是否有选中文本
  const { from, to } = editor.state.selection
  if (from === to || !selectedText.value.trim()) {
    showError('请先选择要翻译的文本')
    return
  }
  
  // 检查AI连接状态
  if (!isConnected.value) {
    showError('AI服务未连接，无法使用翻译功能')
    return
  }
  
  // 设置loading状态
  isAiProcessing.value = true
  aiProcessingType.value = 'translate'
  
  try {
    // 调用后端API进行文本翻译
    console.log('=== 发送翻译请求到后端 ===')
    console.log('Request body:', {
      text: selectedText.value,
      action: 'translate',
      context_before: editor.state.doc.textBetween(0, from),
      context_after: editor.state.doc.textBetween(to, editor.state.doc.content.size)
    })
    
    const response = await fetch('/api/v1/completion/optimize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: selectedText.value,
        action: 'translate',
        context_before: editor.state.doc.textBetween(0, from),
        context_after: editor.state.doc.textBetween(to, editor.state.doc.content.size)
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('=== 收到翻译响应 ===')
    console.log('Response data:', data)
    
    if (data.completion) {
      // 替换选中的文本
      editor.chain().focus().deleteSelection().insertContent(data.completion).run()
      showSuccess('文本翻译完成')
    } else {
      throw new Error('未收到翻译结果')
    }
  } catch (error) {
    console.error('翻译失败:', error)
    showError('翻译失败，请重试')
  } finally {
    // 清除loading状态
    isAiProcessing.value = false
    aiProcessingType.value = ''
  }
}

// 大纲功能方法
const hasChildren = (index) => {
  if (index >= outline.value.length - 1) return false
  return outline.value[index + 1].level > outline.value[index].level
}

const toggleExpand = (index) => {
  outline.value[index].expanded = !outline.value[index].expanded
}

const addOutlineItem = () => {
  if (!newOutlineItem.value.title.trim()) {
    showError('标题不能为空')
    return
  }
  
  outline.value.push({
    title: newOutlineItem.value.title,
    level: newOutlineItem.value.level,
    expanded: true
  })
  
  newOutlineItem.value.title = ''
  showSuccess('条目已添加')
}

const editOutlineItem = (index) => {
  newOutlineItem.value.title = outline.value[index].title
  newOutlineItem.value.level = outline.value[index].level
  
  // 删除原条目
  outline.value.splice(index, 1)
}

const deleteOutlineItem = (index) => {
  outline.value.splice(index, 1)
  showSuccess('条目已删除')
}

/**
 * 根据主题生成大纲 - 改进版
 */
const generateOutlineFromTopic = async () => {
  if (!outlineTopicInput.value.trim()) {
    showError('请输入文章主题')
    return
  }
  
  if (isGeneratingOutline.value) {
    return // 防止重复请求
  }
  
  try {
    // 开始loading状态
    isGeneratingOutline.value = true
    
    // 准备请求数据
    const requestData = {
      topic: outlineTopicInput.value.trim(),
      paper_type: selectedDocumentType.value || 'essay',
      discipline: 'general'  // 可以根据用户选择调整
    }
    
    console.log('发送大纲生成请求:', requestData)
    
    // 调用后端API生成大纲
    const response = await fetch('/api/v1/academic/outline', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData)
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    console.log('收到大纲数据:', data)
    
    // 验证返回的数据格式
    if (!data.outline || !Array.isArray(data.outline)) {
      throw new Error('返回的大纲数据格式不正确')
    }
    
    // 转换API响应为前端格式
    outline.value = data.outline.map((item, index) => ({
      title: item.title || `章节 ${index + 1}`,
      level: item.level || 1,
      description: item.description || '',
      expanded: true
    }))
    
    // 关闭生成对话框
    showOutlineGenerator.value = false
    showSuccess('大纲生成完成！正在应用到文档...')
    
    // 延迟一下再应用大纲到文档，给用户时间看到成功信息
    setTimeout(() => {
      applyOutlineToDocument()
    }, 500)
    
  } catch (error) {
    console.error('生成大纲失败:', error)
    showError(`生成大纲失败: ${error.message}`)
  } finally {
    // 结束loading状态
    isGeneratingOutline.value = false
  }
}

/**
 * 跳过大纲生成
 */
const skipOutlineGeneration = () => {
  showOutlineGenerator.value = false
  showSuccess('已跳过大纲生成，可随时在侧边栏重新生成')
}

/**
 * 处理工具条AI操作
 */
const handleToolbarAiAction = (action) => {
  switch (action) {
    case 'auto-complete':
      handleAutoComplete()
      break
    case 'rewrite':
      handleRewrite()
      break
    case 'expand':
      handleExpand()
      break
    case 'simplify':
      handleSimplify()
      break
    default:
      console.warn('未知的AI操作:', action)
  }
}

/**
 * 处理工具条参考文献操作
 */
const handleToolbarReferenceAction = (action) => {
  switch (action) {
    case 'add':
      // 显示添加引用提示
      showSuccess('请添加引用信息')
      break
    case 'insert':
      // 插入已有的引用
      if (references.value.length === 0) {
        showError('暂无可插入的引用，请先添加引用')
        return
      }
      // 插入第一个引用作为示例，实际应该让用户选择
      insertCitation(references.value[0])
      break
    case 'format':
      // 格式化所有引用
      showSuccess('引用格式已更新')
      break
    default:
      console.warn('未知的参考文献操作:', action)
  }
}

const generateOutlineFromDocument = () => {
  const editor = textEditorRef.value.editor
  if (!editor) return
  
  const content = editor.getText()
  
  // 这里可以调用后端API来生成大纲
  // 模拟生成大纲
  setTimeout(() => {
    // 假设这是从API返回的大纲
    outline.value = [
      { title: '引言', level: 1, expanded: true },
      { title: '研究背景', level: 2, expanded: true },
      { title: '研究意义', level: 2, expanded: true },
      { title: '文献综述', level: 1, expanded: true },
      { title: '研究方法', level: 1, expanded: true },
      { title: '数据收集', level: 2, expanded: true },
      { title: '数据分析', level: 2, expanded: true },
      { title: '研究结果', level: 1, expanded: true },
      { title: '讨论', level: 1, expanded: true },
      { title: '结论与展望', level: 1, expanded: true }
    ]
    
    showSuccess('已从文档生成大纲')
  }, 1000)
}

// 处理文本选择变化
const handleSelectionChange = (selection) => {
  selectedText.value = selection.text
  currentSelection.value = { from: selection.from, to: selection.to }
}

// 显示浮动工具条
const showFloatingToolbar = (data) => {
  showFloatingMenu.value = true
  floatingMenuPosition.value = data.position
  selectedText.value = data.selectedText
  currentSelection.value = data.selectionRange
}

// 隐藏浮动工具条
const hideFloatingToolbar = () => {
  showFloatingMenu.value = false
  selectedText.value = ''
}

// 处理浮动工具条操作
const handleFloatingAction = (action) => {
  const editor = textEditorRef.value?.editor
  if (!editor || !selectedText.value) return
  
  switch (action) {
    case 'auto-complete':
      handleAutoComplete()
      break
    case 'rewrite':
      handleRewrite()
      break
    case 'expand':
      handleExpand()
      break
    case 'simplify':
      handleSimplify()
      break
    case 'translate':
      handleTranslate()
      break
    case 'insert-reference':
      if (references.value.length > 0) {
        insertCitation(references.value[0])
      } else {
        showError('暂无可插入的引用，请先添加引用')
      }
      break
    default:
      console.warn('未知的浮动工具条操作:', action)
  }
  
  // 隐藏浮动工具条
  hideFloatingToolbar()
}

// 从选中文本生成大纲
const generateOutlineFromText = (text) => {
  // 这里可以调用后端API来生成大纲
  console.log('正在从选中文本生成大纲:', text)
  showSuccess('正在生成大纲...')
}

const applyOutlineToDocument = () => {
  const editor = textEditorRef.value?.editor
  if (!editor || outline.value.length === 0) return
  
  try {
    // 生成结构化的大纲HTML
    let outlineHtml = ''
    
    outline.value.forEach(item => {
      const level = Math.min(Math.max(item.level, 1), 6) // 确保level在1-6之间
      const tagName = `h${level}`
      
      // 添加标题
      outlineHtml += `<${tagName}>${item.title}</${tagName}>`
      
      // 如果有描述，添加描述段落
      if (item.description && item.description.trim()) {
        outlineHtml += `<p style="color: #666; font-style: italic; margin-bottom: 10px;">${item.description}</p>`
      }
      
      // 为每个章节添加内容占位符
      if (level <= 2) {
        outlineHtml += `<p>请在此处展开"${item.title}"的具体内容...</p>`
      }
      
      // 添加适当的空行
      outlineHtml += `<p><br></p>`
    })
    
    // 如果没有生成任何HTML，创建默认内容
    if (!outlineHtml.trim()) {
      outlineHtml = '<h1>欢迎使用墨井智能写作助手</h1><p>请开始您的写作之旅...</p>'
    }
    
    // 设置编辑器内容
    editor.commands.setContent(outlineHtml)
    
    // 更新内容状态
    editorContent.value = outlineHtml
    
    showSuccess('大纲已成功应用到文档，您可以开始基于大纲进行写作了！')
    
  } catch (error) {
    console.error('应用大纲到文档失败:', error)
    showError('应用大纲到文档失败，请重试')
  }
}

// 参考文献功能方法
const addReference = () => {
  if (!canAddReference.value) {
    showError('请填写完整的引用信息')
    return
  }
  
  references.value.push({...newReference.value})
  
  // 清空表单
  newReference.value = {
    author: '',
    title: '',
    publisher: '',
    year: ''
  }
  
  showSuccess('引用已添加')
}

const deleteReference = (index) => {
  references.value.splice(index, 1)
  showSuccess('引用已删除')
}

const formatCitation = (reference) => {
  // 根据选择的引用样式格式化引用
  switch (citationStyle.value) {
    case 'apa':
      return `${reference.author}. (${reference.year}). ${reference.title}. ${reference.publisher}.`
    case 'mla':
      return `${reference.author}. "${reference.title}." ${reference.publisher}, ${reference.year}.`
    case 'chicago':
      return `${reference.author}, "${reference.title}," ${reference.publisher}, ${reference.year}.`
    case 'harvard':
      return `${reference.author} (${reference.year}) ${reference.title}. ${reference.publisher}.`
    default:
      return `${reference.author} (${reference.year}). ${reference.title}. ${reference.publisher}.`
  }
}

const insertCitation = (reference) => {
  const editor = textEditorRef.value.editor
  if (!editor) return
  
  // 根据引用样式生成内联引用
  let citationText = ''
  switch (citationStyle.value) {
    case 'apa':
      citationText = `(${reference.author}, ${reference.year})`
      break
    case 'mla':
      citationText = `(${reference.author} ${reference.year})`
      break
    case 'chicago':
      citationText = `(${reference.author} ${reference.year})`
      break
    case 'harvard':
      citationText = `(${reference.author}, ${reference.year})`
      break
    default:
      citationText = `(${reference.author}, ${reference.year})`
  }
  
  // 插入到编辑器当前位置
  editor.commands.insertContent(citationText)
  showSuccess('引用已插入')
}

/**
 * 生成学术结构
 */
const generateStructure = async () => {
  if (!academicTitle.value) {
    showError('请输入论文标题')
    return
  }
  
  try {
    showSuccess('正在生成论文结构...')
    
    // 调用后端API生成学术结构
    const response = await fetch('/api/v1/academic/structure', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: academicTitle.value,
        paper_type: paperType.value || 'research',
        discipline: discipline.value || 'science',
        citation_style: citationStyle.value || 'apa'
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    structure.value = data
    
    showSuccess('论文结构生成完成！')
  } catch (error) {
    console.error('生成论文结构失败:', error)
    showError('生成论文结构失败，请重试')
  }
}

const applyStructureToDocument = () => {
  const editor = textEditorRef.value.editor
  if (!editor || !structure.value) return
  
  // 生成结构HTML
  let structureHtml = `<h1>${structure.value.title}</h1>\n`
  structureHtml += `<h2>摘要</h2>\n<p>${structure.value.abstract}</p>\n`
  
  // 添加章节
  structure.value.sections.forEach(section => {
    structureHtml += `<h2>${section.title}</h2>\n`
    structureHtml += `<p>${section.description}</p>\n`
    
    if (section.subsections && section.subsections.length > 0) {
      section.subsections.forEach(subsection => {
        structureHtml += `<h3>${subsection.title}</h3>\n`
        structureHtml += `<p>${subsection.description}</p>\n`
      })
    }
  })
  
  // 插入到编辑器
  editor.commands.setContent(structureHtml)
  showSuccess('已应用论文结构到文档')
}

// 样式调整功能方法已移除

/**
 * 处理大纲生成事件
 */
const handleOutlineGenerate = (topic) => {
  generateOutlineFromTopic(topic)
}



/**
 * 处理格式化事件
 */
const handleFormat = (formatType) => {
  const editor = textEditorRef.value?.editor
  if (!editor) return
  
  switch (formatType) {
    case 'heading1':
      editor.chain().focus().toggleHeading({ level: 1 }).run()
      break
    case 'heading2':
      editor.chain().focus().toggleHeading({ level: 2 }).run()
      break
    case 'heading3':
      editor.chain().focus().toggleHeading({ level: 3 }).run()
      break
    case 'bold':
      editor.chain().focus().toggleBold().run()
      break
    case 'italic':
      editor.chain().focus().toggleItalic().run()
      break
    case 'underline':
      editor.chain().focus().toggleUnderline().run()
      break
    case 'strike':
      editor.chain().focus().toggleStrike().run()
      break
    case 'bulletList':
      editor.chain().focus().toggleBulletList().run()
      break
    case 'orderedList':
      editor.chain().focus().toggleOrderedList().run()
      break
    case 'blockquote':
      editor.chain().focus().toggleBlockquote().run()
      break
    case 'codeBlock':
      editor.chain().focus().toggleCodeBlock().run()
      break
    case 'alignLeft':
      editor.chain().focus().setTextAlign('left').run()
      break
    case 'alignCenter':
      editor.chain().focus().setTextAlign('center').run()
      break
    case 'alignRight':
      editor.chain().focus().setTextAlign('right').run()
      break
    case 'horizontalRule':
      editor.chain().focus().setHorizontalRule().run()
      break
    default:
      console.warn('未知的格式化类型:', formatType)
  }
}

/**
 * 处理AI操作
 */
const handleAiAction = (action) => {
  if (action.type === 'outline-generate') {
    outlineTopicInput.value = action.topic
    generateOutlineFromTopic()
  } else {
    console.warn('未知的AI操作:', action)
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

<style scoped>
.outline-tree {
  max-height: 300px; /* 增加大纲树的高度 */
  overflow-y: auto;
}

.outline-item {
  border-bottom: 1px solid #eee;
}

.references-list {
  max-height: 300px; /* 增加参考文献列表的高度 */
  overflow-y: auto;
}

:deep(.ProseMirror) {
  min-height: 600px; /* 增加编辑器的最小高度 */
  padding: 1rem;
}

/* 确保编辑器区域占据更多空间 */
.min-h-screen {
  min-height: 100vh;
}
</style>
