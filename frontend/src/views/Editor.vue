<template>
  <div class="min-h-screen bg-white flex flex-col">
    <!-- 编辑器顶部工具栏 -->
    <div class="border-b border-gray-200 px-4 py-2 flex flex-wrap items-center justify-between gap-4 bg-white shadow-sm">
      <div class="flex items-center space-x-4">
        <h1 class="text-xl font-semibold text-[#1A365D]">墨井</h1>
        <div class="flex items-center">
          <span 
            class="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium"
            :class="isConnected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
          >
            <span 
              class="w-2 h-2 mr-1 rounded-full"
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
          class="inline-flex items-center px-2 py-1 border border-gray-300 text-sm leading-5 font-medium rounded-md text-gray-700 bg-white hover:text-[#4FD1C5] focus:outline-none focus:border-[#4FD1C5] focus:shadow-outline-blue transition ease-in-out duration-150"
        >
          <svg class="h-4 w-4 mr-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path v-if="!isSidebarOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          {{ isSidebarOpen ? '隐藏' : 'AI 功能' }}
        </button>
      </div>
    </div>
    
    <div class="flex flex-grow h-full">
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
          class="w-64 bg-white border-r border-gray-200 p-4 h-full overflow-y-auto shadow-md"
        >
                  <!-- 侧边栏标签页 -->
          <div class="mb-4">
            <div class="flex border-b border-gray-200">
              <button 
                v-for="tab in sidebarTabs" 
                :key="tab.id"
                @click="activeSidebarTab = tab.id"
                :class="[
                  'px-4 py-2 text-sm font-medium border-b-2 -mb-px',
                  activeSidebarTab === tab.id
                    ? 'border-[#4FD1C5] text-[#4FD1C5]'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                ]"
              >
                {{ tab.name }}
              </button>
            </div>
          </div>
          
          <!-- AI 辅助面板 -->
          <div v-show="activeSidebarTab === 'ai'">
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
          
          <!-- 大纲面板 -->
          <div v-show="activeSidebarTab === 'outline'" class="space-y-4">
            <h3 class="font-medium text-gray-700">文档结构</h3>
            
            <div class="mb-4">
              <div class="flex space-x-2 mb-2">
                <button 
                  @click="outlineMode = 'outline'"
                  :class="[
                    'flex-1 px-2 py-1 text-xs rounded-md',
                    outlineMode === 'outline' 
                      ? 'bg-[#4FD1C5] text-white' 
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  ]"
                >
                  大纲视图
                </button>
                <button 
                  @click="outlineMode = 'academic'"
                  :class="[
                    'flex-1 px-2 py-1 text-xs rounded-md',
                    outlineMode === 'academic' 
                      ? 'bg-[#4FD1C5] text-white' 
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  ]"
                >
                  学术结构
                </button>
              </div>
            </div>
            
            <!-- 大纲视图 -->
            <div v-if="outlineMode === 'outline'">
              <div class="outline-tree">
                <div v-for="(item, index) in outline" :key="index" class="outline-item" :style="{ paddingLeft: `${item.level * 12}px` }">
                  <div class="flex items-center py-1">
                    <button @click="toggleExpand(index)" v-if="hasChildren(index)" class="mr-1 w-4 h-4 flex items-center justify-center text-xs">
                      <span v-if="!item.expanded">▶</span>
                      <span v-else>▼</span>
                    </button>
                    <span v-else class="mr-1 w-4"></span>
                    <span class="outline-title text-sm">{{ item.title }}</span>
                    <div class="ml-auto flex space-x-1">
                      <button @click="editOutlineItem(index)" class="text-xs text-blue-500 hover:text-blue-700">
                        编辑
                      </button>
                      <button @click="deleteOutlineItem(index)" class="text-xs text-red-500 hover:text-red-700">
                        删除
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="mt-2">
                <div class="flex space-x-2">
                  <input 
                    type="text" 
                    v-model="newOutlineItem.title" 
                    class="flex-1 px-2 py-1 text-sm border border-gray-300 rounded-md"
                    placeholder="新条目标题"
                  />
                  <select 
                    v-model="newOutlineItem.level" 
                    class="w-16 px-1 py-1 text-sm border border-gray-300 rounded-md"
                  >
                    <option :value="1">1级</option>
                    <option :value="2">2级</option>
                    <option :value="3">3级</option>
                  </select>
                </div>
                <button 
                  @click="addOutlineItem" 
                  class="mt-2 w-full px-2 py-1 text-sm bg-[#4FD1C5] text-white rounded-md hover:bg-[#3DB9B0]"
                >
                  添加条目
                </button>
              </div>
              
              <div class="flex space-x-2 mt-4">
                <button 
                  @click="generateOutlineFromDocument" 
                  class="flex-1 px-2 py-1 text-xs bg-blue-500 text-white rounded-md hover:bg-blue-600"
                >
                  从文档生成
                </button>
                <button 
                  @click="applyOutlineToDocument" 
                  class="flex-1 px-2 py-1 text-xs bg-green-500 text-white rounded-md hover:bg-green-600"
                >
                  应用到文档
                </button>
              </div>
            </div>
            
            <!-- 学术结构视图 -->
            <div v-if="outlineMode === 'academic'" class="space-y-4">
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">论文类型</label>
                <select 
                  v-model="paperType" 
                  class="w-full px-2 py-1 text-sm border border-gray-300 rounded-md"
                >
                  <option value="research">研究论文</option>
                  <option value="review">综述论文</option>
                  <option value="case-study">案例研究</option>
                  <option value="thesis">学位论文</option>
                </select>
              </div>
              
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">学科领域</label>
                <select 
                  v-model="discipline" 
                  class="w-full px-2 py-1 text-sm border border-gray-300 rounded-md"
                >
                  <option value="science">自然科学</option>
                  <option value="social">社会科学</option>
                  <option value="humanities">人文学科</option>
                  <option value="engineering">工程技术</option>
                </select>
              </div>
              
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">论文标题</label>
                <input 
                  type="text" 
                  v-model="academicTitle" 
                  class="w-full px-2 py-1 text-sm border border-gray-300 rounded-md"
                  placeholder="输入论文标题"
                />
              </div>
              
              <button 
                @click="generateStructure" 
                class="w-full px-2 py-1 text-sm bg-[#4FD1C5] text-white rounded-md hover:bg-[#3DB9B0]"
              >
                生成论文结构
              </button>
              
              <div v-if="structure" class="mt-4 p-2 border border-gray-200 rounded-md text-xs max-h-60 overflow-y-auto">
                <div v-html="formattedStructure"></div>
                <button 
                  @click="applyStructureToDocument" 
                  class="mt-2 w-full px-2 py-1 text-xs bg-blue-500 text-white rounded-md hover:bg-blue-600"
                >
                  应用到文档
                </button>
              </div>
            </div>
          </div>
          
          <!-- 参考文献面板 -->
          <div v-show="activeSidebarTab === 'reference'" class="space-y-4">
            <h3 class="font-medium text-gray-700">参考文献</h3>
            
            <div>
              <label class="block text-xs font-medium text-gray-700 mb-1">引用格式</label>
              <select 
                v-model="citationStyle" 
                class="w-full px-2 py-1 text-sm border border-gray-300 rounded-md"
              >
                <option value="apa">APA</option>
                <option value="mla">MLA</option>
                <option value="chicago">Chicago</option>
                <option value="harvard">Harvard</option>
              </select>
            </div>
            
            <div class="space-y-2">
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">作者</label>
                <input 
                  type="text" 
                  v-model="newReference.author" 
                  class="w-full px-2 py-1 text-sm border border-gray-300 rounded-md"
                  placeholder="作者姓名"
                />
              </div>
              
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">标题</label>
                <input 
                  type="text" 
                  v-model="newReference.title" 
                  class="w-full px-2 py-1 text-sm border border-gray-300 rounded-md"
                  placeholder="作品标题"
                />
              </div>
              
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">出版商/期刊</label>
                <input 
                  type="text" 
                  v-model="newReference.publisher" 
                  class="w-full px-2 py-1 text-sm border border-gray-300 rounded-md"
                  placeholder="出版商或期刊名称"
                />
              </div>
              
              <div>
                <label class="block text-xs font-medium text-gray-700 mb-1">年份</label>
                <input 
                  type="text" 
                  v-model="newReference.year" 
                  class="w-full px-2 py-1 text-sm border border-gray-300 rounded-md"
                  placeholder="出版年份"
                />
              </div>
              
              <button 
                @click="addReference" 
                class="w-full px-2 py-1 text-sm bg-[#4FD1C5] text-white rounded-md hover:bg-[#3DB9B0]"
                :disabled="!canAddReference"
              >
                添加引用
              </button>
            </div>
            
            <div class="references-list max-h-60 overflow-y-auto">
              <div 
                v-for="(reference, index) in references" 
                :key="index"
                class="p-2 mb-2 border border-gray-200 rounded-md text-xs"
              >
                <div class="flex justify-between items-start">
                  <div class="font-medium">{{ reference.title }}</div>
                  <button @click="deleteReference(index)" class="text-red-500 hover:text-red-700">×</button>
                </div>
                <div class="text-gray-600">{{ reference.author }} ({{ reference.year }})</div>
                <div class="mt-1 p-1 bg-gray-50 rounded text-xs">
                  {{ formatCitation(reference) }}
                </div>
                <button 
                  @click="insertCitation(reference)" 
                  class="mt-1 w-full px-2 py-1 text-xs bg-blue-500 text-white rounded-md hover:bg-blue-600"
                >
                  插入引用
                </button>
              </div>
            </div>
          </div>
          
          <!-- 样式调整面板已移除 -->
        </div>
      </transition>
      
      <!-- 主编辑区域 -->
      <div class="flex-1 flex flex-col h-full overflow-hidden">
        <div class="flex-1 bg-white overflow-hidden">
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
        <div class="border-t border-gray-200 py-1.5 px-4 flex items-center justify-between text-xs text-gray-500 bg-gray-50 sticky bottom-0">
          <div class="flex items-center space-x-4">
            <span>{{ aiStatus === 'idle' ? 'AI 就绪' : aiStatus === 'processing' ? 'AI 思考中...' : 'AI 空闲' }}</span>
          </div>
          <div>
            <span>Tab: 接受建议 | Esc: 拒绝建议</span>
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
const contextWindowBefore = computed(() => completion.contextWindowBefore)
const contextWindowAfter = computed(() => completion.contextWindowAfter)
const currentCompletion = ref('')
const isSidebarOpen = ref(true) // 侧边栏默认打开

// 侧边栏标签页
const sidebarTabs = [
  { id: 'ai', name: '辅助' },
  { id: 'outline', name: '大纲' },
  { id: 'reference', name: '参考文献' }
]
const activeSidebarTab = ref('ai')
const outlineMode = ref('outline')

// 大纲状态
const outline = ref([
  { title: '引言', level: 1, expanded: true },
  { title: '研究背景', level: 2, expanded: true },
  { title: '研究意义', level: 2, expanded: true },
  { title: '文献综述', level: 1, expanded: true },
  { title: '研究方法', level: 1, expanded: true },
  { title: '研究结果', level: 1, expanded: true },
  { title: '结论与展望', level: 1, expanded: true }
])
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
    showError('请先选择要改写的文本')
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
        showError('改写失败，请重试')
      })
  }
}

const handleExpand = () => {
  const editor = textEditorRef.value.editor
  if (!editor) return
  
  // 获取选中的文本
  const { from, to } = editor.state.selection
  if (from === to) {
    showError('请先选择要扩写的文本')
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
        showError('扩写失败，请重试')
      })
  }
}

const handleSimplify = () => {
  const editor = textEditorRef.value.editor
  if (!editor) return
  
  // 获取选中的文本
  const { from, to } = editor.state.selection
  if (from === to) {
    showError('请先选择要简化的文本')
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
        showError('简化失败，请重试')
      })
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

const applyOutlineToDocument = () => {
  const editor = textEditorRef.value.editor
  if (!editor) return
  
  // 生成大纲HTML
  let outlineHtml = ''
  
  outline.value.forEach(item => {
    const tagName = `h${item.level}`
    outlineHtml += `<${tagName}>${item.title}</${tagName}>\n<p>在此处添加内容...</p>\n`
  })
  
  // 插入到编辑器
  editor.commands.setContent(outlineHtml)
  showSuccess('已应用大纲到文档')
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

// 学术结构功能方法
const generateStructure = () => {
  if (!academicTitle.value) {
    showError('请输入论文标题')
    return
  }
  
  // 这里可以调用后端API来生成学术结构
  // 模拟生成结构
  setTimeout(() => {
    // 假设这是从API返回的结构
    structure.value = {
      title: academicTitle.value,
      abstract: '本研究旨在探讨...[摘要内容将根据研究问题生成]',
      sections: [
        {
          title: '1. 引言',
          description: '介绍研究背景、问题陈述和研究目的',
          subsections: [
            { title: '1.1 研究背景', description: '概述研究领域的当前状态和重要性' },
            { title: '1.2 问题陈述', description: '明确定义待解决的研究问题' },
            { title: '1.3 研究目的和目标', description: '阐述研究的具体目标和预期成果' }
          ]
        },
        {
          title: '2. 文献综述',
          description: '回顾和评价相关研究文献',
          subsections: [
            { title: '2.1 理论框架', description: '讨论支持研究的理论基础' },
            { title: '2.2 相关研究', description: '分析与研究问题相关的现有研究' },
            { title: '2.3 研究差距', description: '确定现有研究中的不足之处' }
          ]
        },
        {
          title: '3. 研究方法',
          description: '详细说明研究设计和方法',
          subsections: [
            { title: '3.1 研究设计', description: '描述研究的整体方法和设计' },
            { title: '3.2 数据收集', description: '解释数据收集的方法和工具' },
            { title: '3.3 数据分析', description: '详述数据分析的技术和程序' }
          ]
        },
        {
          title: '4. 结果',
          description: '呈现研究发现',
          subsections: [
            { title: '4.1 主要发现', description: '展示与研究问题直接相关的结果' },
            { title: '4.2 数据分析', description: '提供详细的数据分析和统计结果' }
          ]
        },
        {
          title: '5. 讨论',
          description: '解释和评价研究结果',
          subsections: [
            { title: '5.1 结果解释', description: '解释研究发现的意义' },
            { title: '5.2 与现有研究的比较', description: '将结果与现有文献进行比较' },
            { title: '5.3 研究局限性', description: '讨论研究的局限性和不足' }
          ]
        },
        {
          title: '6. 结论',
          description: '总结研究的主要发现和贡献',
          subsections: [
            { title: '6.1 研究总结', description: '概述研究的主要发现和结论' },
            { title: '6.2 理论和实践意义', description: '讨论研究对理论和实践的贡献' },
            { title: '6.3 未来研究方向', description: '提出未来研究的建议' }
          ]
        }
      ]
    }
    
    showSuccess('已生成论文结构')
  }, 1000)
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
