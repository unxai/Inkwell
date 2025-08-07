<template>
  <div class="research-panel h-full flex flex-col bg-white">
    <!-- Header -->
    <div class="flex items-center justify-between p-4 border-b border-gray-200 bg-gradient-to-r from-green-50 to-emerald-50">
      <div class="flex items-center space-x-2">
        <div class="w-3 h-3 rounded-full bg-green-500"></div>
        <h3 class="text-lg font-semibold text-gray-800">研究助手</h3>
      </div>
      <button
        @click="$emit('toggle-panel')"
        class="p-1 text-gray-400 hover:text-gray-600 transition-colors"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
        </svg>
      </button>
    </div>

    <!-- Search Tab Navigation -->
    <div class="flex border-b border-gray-100">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        @click="activeTab = tab.key"
        :class="activeTab === tab.key 
          ? 'border-b-2 border-green-500 text-green-600 bg-green-50' 
          : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'"
        class="flex-1 py-3 px-4 text-sm font-medium transition-colors"
      >
        {{ tab.name }}
      </button>
    </div>

    <!-- Web Search Tab -->
    <div v-if="activeTab === 'web'" class="flex-1 flex flex-col">
      <!-- Search Input -->
      <div class="p-4 border-b border-gray-100">
        <div class="relative">
          <input
            v-model="webSearchQuery"
            type="text"
            placeholder="搜索网页资源..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent text-sm"
            @keyup.enter="searchWeb"
          />
          <svg class="w-5 h-5 absolute left-3 top-2.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
        </div>
        <button
          @click="searchWeb"
          :disabled="!webSearchQuery.trim() || isSearching"
          class="w-full mt-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm font-medium"
        >
          <span v-if="!isSearching">🔍 搜索网页</span>
          <span v-else>🔄 搜索中...</span>
        </button>
      </div>

      <!-- Search Results -->
      <div class="flex-1 overflow-y-auto p-4 space-y-3">
        <div v-if="webResults.length === 0 && !hasSearched" class="text-center py-8">
          <div class="text-4xl mb-2">🌐</div>
          <p class="text-gray-500 text-sm">输入关键词搜索网页资源</p>
        </div>

        <div v-if="hasSearched && webResults.length === 0 && !isSearching" class="text-center py-8">
          <div class="text-4xl mb-2">🚫</div>
          <p class="text-gray-500 text-sm">未找到相关结果</p>
        </div>

        <div
          v-for="result in webResults"
          :key="result.id"
          class="result-card p-3 border border-gray-200 rounded-lg hover:border-green-300 hover:shadow-md transition-all"
        >
          <div class="flex items-start space-x-3">
            <div class="flex-shrink-0 w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.102m0-12.728l4-4a4 4 0 015.656 5.656l-1.102 1.102m-8.486 8.485l4-4"></path>
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <h4 class="font-medium text-gray-800 text-sm line-clamp-2 mb-1">
                {{ result.title }}
              </h4>
              <p class="text-xs text-gray-600 mb-2 line-clamp-3">
                {{ result.summary }}
              </p>
              <div class="flex items-center justify-between text-xs">
                <span class="text-gray-500">{{ result.url }}</span>
                <div class="flex space-x-2">
                  <button
                    @click="addToReferences(result)"
                    class="px-2 py-1 bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
                  >
                    添加引用
                  </button>
                  <button
                    @click="insertSummary(result)"
                    class="px-2 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
                  >
                    插入摘要
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Academic Search Tab -->
    <div v-if="activeTab === 'academic'" class="flex-1 flex flex-col">
      <!-- Search Input -->
      <div class="p-4 border-b border-gray-100">
        <div class="relative">
          <input
            v-model="academicSearchQuery"
            type="text"
            placeholder="搜索学术论文..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent text-sm"
            @keyup.enter="searchAcademic"
          />
          <svg class="w-5 h-5 absolute left-3 top-2.5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
          </svg>
        </div>
        <button
          @click="searchAcademic"
          :disabled="!academicSearchQuery.trim() || isSearchingAcademic"
          class="w-full mt-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm font-medium"
        >
          <span v-if="!isSearchingAcademic">📚 搜索学术论文</span>
          <span v-else>🔄 搜索中...</span>
        </button>
      </div>

      <!-- Academic Results -->
      <div class="flex-1 overflow-y-auto p-4 space-y-3">
        <div v-if="academicResults.length === 0 && !hasSearchedAcademic" class="text-center py-8">
          <div class="text-4xl mb-2">📚</div>
          <p class="text-gray-500 text-sm">搜索相关学术论文和资源</p>
        </div>

        <div
          v-for="result in academicResults"
          :key="result.id"
          class="result-card p-3 border border-gray-200 rounded-lg hover:border-green-300 hover:shadow-md transition-all"
        >
          <div class="flex items-start space-x-3">
            <div class="flex-shrink-0 w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <h4 class="font-medium text-gray-800 text-sm line-clamp-2 mb-1">
                {{ result.title }}
              </h4>
              <p class="text-xs text-gray-600 mb-1">
                {{ result.authors }} ({{ result.year }})
              </p>
              <p class="text-xs text-gray-600 mb-2 line-clamp-2">
                {{ result.abstract }}
              </p>
              <div class="flex items-center justify-between text-xs">
                <span class="text-gray-500">{{ result.journal }}</span>
                <div class="flex space-x-2">
                  <button
                    @click="addToReferences(result)"
                    class="px-2 py-1 bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
                  >
                    添加引用
                  </button>
                  <button
                    @click="insertSummary(result)"
                    class="px-2 py-1 bg-blue-600 text-white rounded hover:blue-green-700 transition-colors"
                  >
                    插入摘要
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- My Sources Tab -->
    <div v-if="activeTab === 'sources'" class="flex-1 flex flex-col">
      <!-- Add Source -->
      <div class="p-4 border-b border-gray-100">
        <button
          @click="showAddSourceModal = true"
          class="w-full px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm font-medium"
        >
          ➕ 添加资源
        </button>
      </div>

      <!-- Sources List -->
      <div class="flex-1 overflow-y-auto p-4 space-y-3">
        <div v-if="mySources.length === 0" class="text-center py-8">
          <div class="text-4xl mb-2">📁</div>
          <p class="text-gray-500 text-sm">还没有保存的资源</p>
        </div>

        <div
          v-for="source in mySources"
          :key="source.id"
          class="source-card p-3 border border-gray-200 rounded-lg hover:border-green-300 hover:shadow-md transition-all"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1 min-w-0">
              <h4 class="font-medium text-gray-800 text-sm line-clamp-2 mb-1">
                {{ source.title }}
              </h4>
              <p class="text-xs text-gray-600 mb-2">
                {{ source.type }} · {{ formatDate(source.dateAdded) }}
              </p>
              <p class="text-xs text-gray-600 line-clamp-2">
                {{ source.summary || source.description }}
              </p>
            </div>
            <button
              @click="removeSource(source.id)"
              class="ml-2 text-gray-400 hover:text-red-500 transition-colors"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
            </button>
          </div>
          <div class="mt-2 pt-2 border-t border-gray-100 flex space-x-2">
            <button
              @click="insertSummary(source)"
              class="text-xs px-2 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
            >
              插入摘要
            </button>
            <button
              @click="addToReferences(source)"
              class="text-xs px-2 py-1 bg-green-600 text-white rounded hover:bg-green-700 transition-colors"
            >
              添加引用
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Source Modal -->
    <div v-if="showAddSourceModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="showAddSourceModal = false">
      <div class="bg-white rounded-lg max-w-md w-full mx-4" @click.stop>
        <div class="p-4 border-b border-gray-200">
          <h3 class="text-lg font-semibold">添加资源</h3>
        </div>
        <div class="p-4 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">标题</label>
            <input
              v-model="newSource.title"
              type="text"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm"
              placeholder="输入资源标题"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">类型</label>
            <select
              v-model="newSource.type"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm"
            >
              <option value="网页">网页</option>
              <option value="论文">论文</option>
              <option value="书籍">书籍</option>
              <option value="其他">其他</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">URL (可选)</label>
            <input
              v-model="newSource.url"
              type="url"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm"
              placeholder="https://..."
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">描述</label>
            <textarea
              v-model="newSource.description"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm"
              rows="3"
              placeholder="简要描述..."
            ></textarea>
          </div>
        </div>
        <div class="p-4 border-t border-gray-200 flex justify-end space-x-3">
          <button
            @click="showAddSourceModal = false"
            class="px-4 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            取消
          </button>
          <button
            @click="addSource"
            :disabled="!newSource.title.trim()"
            class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            添加
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { showSuccess, showError } from '@/utils/toast-service'

const emit = defineEmits(['toggle-panel', 'add-reference', 'insert-text'])

// UI State
const activeTab = ref('web')
const isSearching = ref(false)
const isSearchingAcademic = ref(false)
const hasSearched = ref(false)
const hasSearchedAcademic = ref(false)
const showAddSourceModal = ref(false)

// Search queries
const webSearchQuery = ref('')
const academicSearchQuery = ref('')

// Results
const webResults = reactive([])
const academicResults = reactive([])
const mySources = reactive([])

// New source form
const newSource = reactive({
  title: '',
  type: '网页',
  url: '',
  description: ''
})

// Tab definitions
const tabs = [
  { key: 'web', name: '网页搜索' },
  { key: 'academic', name: '学术搜索' },
  { key: 'sources', name: '我的资源' }
]

// Methods
const searchWeb = async () => {
  if (!webSearchQuery.value.trim()) return
  
  isSearching.value = true
  hasSearched.value = true
  
  try {
    // Mock web search results - in real app, call search API
    await new Promise(resolve => setTimeout(resolve, 1500)) // Simulate API delay
    
    const mockResults = [
      {
        id: 1,
        title: '人工智能在教育中的应用与发展前景',
        summary: '本文探讨了人工智能技术在现代教育系统中的应用，包括个性化学习、智能辅导、自动评估等方面。',
        url: 'https://example.com/ai-education',
        type: 'web'
      },
      {
        id: 2,
        title: '机器学习算法在医疗诊断中的创新应用',
        summary: '研究分析了深度学习、神经网络等机器学习技术在医疗影像诊断、疾病预测等领域的突破性应用。',
        url: 'https://example.com/ml-healthcare',
        type: 'web'
      }
    ]
    
    // Filter results based on search query (mock)
    webResults.splice(0, webResults.length, ...mockResults)
    
  } catch (error) {
    console.error('Web search error:', error)
    showError('搜索失败，请重试')
  } finally {
    isSearching.value = false
  }
}

const searchAcademic = async () => {
  if (!academicSearchQuery.value.trim()) return
  
  isSearchingAcademic.value = true
  hasSearchedAcademic.value = true
  
  try {
    // Mock academic search results - in real app, call academic search API
    await new Promise(resolve => setTimeout(resolve, 2000)) // Simulate API delay
    
    const mockResults = [
      {
        id: 1,
        title: 'Artificial Intelligence in Educational Technology: A Systematic Review',
        authors: 'Zhang, L., Wang, M., Li, H.',
        year: 2023,
        journal: 'Journal of Educational Technology',
        abstract: 'This systematic review examines the current state of AI applications in educational technology, analyzing 150 peer-reviewed articles...',
        type: 'academic'
      },
      {
        id: 2,
        title: 'Deep Learning Approaches for Personalized Learning Systems',
        authors: 'Chen, Y., Liu, X., Brown, A.',
        year: 2024,
        journal: 'Computers & Education',
        abstract: 'We present novel deep learning architectures for creating personalized learning experiences that adapt to individual student needs...',
        type: 'academic'
      }
    ]
    
    academicResults.splice(0, academicResults.length, ...mockResults)
    
  } catch (error) {
    console.error('Academic search error:', error)
    showError('学术搜索失败，请重试')
  } finally {
    isSearchingAcademic.value = false
  }
}

const addToReferences = (source) => {
  // Transform source to reference format
  const reference = {
    author: source.authors || '未知作者',
    title: source.title,
    publisher: source.journal || source.url || '未知出版方',
    year: source.year || new Date().getFullYear().toString(),
    url: source.url || ''
  }
  
  emit('add-reference', reference)
  showSuccess('已添加到引用列表')
}

const insertSummary = (source) => {
  const summary = source.summary || source.abstract || source.description || '暂无摘要'
  emit('insert-text', `\n\n根据"${source.title}"的内容，${summary}\n\n`)
  showSuccess('摘要已插入到文档')
}

const addSource = () => {
  if (!newSource.title.trim()) return
  
  const source = {
    id: Date.now(),
    title: newSource.title,
    type: newSource.type,
    url: newSource.url,
    description: newSource.description,
    dateAdded: new Date()
  }
  
  mySources.push(source)
  
  // Reset form
  Object.assign(newSource, {
    title: '',
    type: '网页',
    url: '',
    description: ''
  })
  
  showAddSourceModal.value = false
  showSuccess('资源已添加')
}

const removeSource = (sourceId) => {
  const index = mySources.findIndex(s => s.id === sourceId)
  if (index > -1) {
    mySources.splice(index, 1)
    showSuccess('资源已删除')
  }
}

const formatDate = (date) => {
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  }).format(new Date(date))
}
</script>

<style scoped>
.research-panel {
  min-height: 400px;
  max-height: 100vh;
}

.result-card {
  transition: all 0.2s ease;
}

.result-card:hover {
  transform: translateY(-1px);
}

.source-card {
  transition: all 0.2s ease;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>