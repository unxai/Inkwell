<template>
  <div class="version-panel h-full flex flex-col bg-white">
    <!-- Header -->
    <div class="flex items-center justify-between p-4 border-b border-gray-200 bg-gradient-to-r from-yellow-50 to-amber-50">
      <div class="flex items-center space-x-2">
        <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
        <h3 class="text-lg font-semibold text-gray-800">版本历史</h3>
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

    <!-- Auto-save Status -->
    <div class="p-4 border-b border-gray-100">
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center space-x-2">
          <div :class="autoSaveEnabled ? 'bg-green-500' : 'bg-gray-400'" class="w-2 h-2 rounded-full"></div>
          <span class="text-sm text-gray-700">自动保存</span>
        </div>
        <label class="relative inline-flex items-center cursor-pointer">
          <input
            v-model="autoSaveEnabled"
            type="checkbox"
            class="sr-only peer"
          />
          <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-yellow-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-yellow-500"></div>
        </label>
      </div>
      
      <div v-if="lastSaved" class="text-xs text-gray-500">
        上次保存: {{ formatTime(lastSaved) }}
      </div>
      
      <button
        @click="saveCurrentVersion"
        class="w-full mt-3 px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors text-sm font-medium"
      >
        💾 立即保存版本
      </button>
    </div>

    <!-- Version List -->
    <div class="flex-1 overflow-y-auto p-4">
      <div class="flex items-center justify-between mb-4">
        <h4 class="font-medium text-gray-800">版本历史 ({{ versions.length }})</h4>
        <button
          @click="clearAllVersions"
          :disabled="versions.length === 0"
          class="px-2 py-1 text-xs text-red-600 hover:bg-red-50 rounded disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          清空历史
        </button>
      </div>

      <div v-if="versions.length === 0" class="text-center py-8">
        <div class="text-4xl mb-2">📝</div>
        <p class="text-gray-500 text-sm">还没有保存的版本</p>
        <p class="text-xs text-gray-400 mt-1">文档将自动保存到版本历史中</p>
      </div>

      <div class="space-y-3">
        <div
          v-for="(version, index) in versions"
          :key="version.id"
          class="version-card p-4 border border-gray-200 rounded-lg hover:border-yellow-300 hover:shadow-md transition-all"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="flex-1">
              <div class="flex items-center space-x-2 mb-2">
                <span class="px-2 py-0.5 bg-yellow-100 text-yellow-700 text-xs rounded-full">
                  v{{ versions.length - index }}
                </span>
                <span class="text-xs text-gray-500">{{ formatTime(version.timestamp) }}</span>
                <span v-if="version.isAutoSave" class="px-1.5 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">
                  自动
                </span>
                <span v-else class="px-1.5 py-0.5 bg-blue-100 text-blue-600 text-xs rounded">
                  手动
                </span>
              </div>
              
              <div class="text-sm text-gray-700 mb-2">
                <div class="flex items-center space-x-4 text-xs text-gray-500">
                  <span>{{ version.wordCount }} 字</span>
                  <span>{{ version.changes }} 处变更</span>
                </div>
              </div>
              
              <!-- Version Preview -->
              <div class="text-xs text-gray-600 bg-gray-50 p-2 rounded border-l-4 border-yellow-400 mb-3">
                <div class="line-clamp-3">{{ getTextPreview(version.content) }}</div>
              </div>
              
              <!-- Version Note -->
              <div v-if="version.note" class="text-xs text-gray-600 italic">
                "{{ version.note }}"
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div class="flex justify-between items-center">
            <div class="flex space-x-2">
              <button
                @click="restoreVersion(version)"
                class="text-xs px-3 py-1 bg-yellow-600 text-white rounded hover:bg-yellow-700 transition-colors"
              >
                恢复此版本
              </button>
              <button
                @click="compareWithCurrent(version)"
                class="text-xs px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
              >
                对比差异
              </button>
            </div>
            <div class="flex space-x-1">
              <button
                @click="addVersionNote(index)"
                class="p-1 text-gray-400 hover:text-blue-500 transition-colors"
                title="添加备注"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                </svg>
              </button>
              <button
                @click="deleteVersion(index)"
                class="p-1 text-gray-400 hover:text-red-500 transition-colors"
                title="删除版本"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Compare Modal -->
    <div v-if="showCompareModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="showCompareModal = false">
      <div class="bg-white rounded-lg max-w-4xl w-full mx-4 max-h-[80vh] overflow-hidden" @click.stop>
        <div class="p-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold">版本对比</h3>
            <button @click="showCompareModal = false" class="text-gray-400 hover:text-gray-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
        </div>
        
        <div class="p-6 overflow-y-auto max-h-96">
          <div class="grid grid-cols-2 gap-4">
            <!-- Current Version -->
            <div>
              <h4 class="font-medium text-gray-800 mb-2">当前版本</h4>
              <div class="text-sm text-gray-700 bg-green-50 p-4 rounded border-l-4 border-green-400 max-h-64 overflow-y-auto">
                {{ getTextPreview(currentContent) }}
              </div>
            </div>
            
            <!-- Selected Version -->
            <div>
              <h4 class="font-medium text-gray-800 mb-2">
                历史版本 ({{ formatTime(compareVersion?.timestamp) }})
              </h4>
              <div class="text-sm text-gray-700 bg-yellow-50 p-4 rounded border-l-4 border-yellow-400 max-h-64 overflow-y-auto">
                {{ getTextPreview(compareVersion?.content) }}
              </div>
            </div>
          </div>
        </div>
        
        <div class="p-4 border-t border-gray-200 flex justify-end space-x-3">
          <button 
            @click="showCompareModal = false"
            class="px-4 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            关闭
          </button>
          <button 
            @click="restoreVersion(compareVersion); showCompareModal = false"
            class="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors"
          >
            恢复此版本
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, watch } from 'vue'
import { showSuccess, showError } from '@/utils/toast-service'

const props = defineProps({
  currentContent: {
    type: String,
    default: ''
  },
  wordCount: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['toggle-panel', 'restore-version'])

// State
const autoSaveEnabled = ref(true)
const lastSaved = ref(null)
const versions = reactive([])
const showCompareModal = ref(false)
const compareVersion = ref(null)

let autoSaveInterval = null
let lastContent = ''

// Methods
const formatTime = (timestamp) => {
  const now = new Date()
  const date = new Date(timestamp)
  const diff = now - date
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  
  return new Intl.DateTimeFormat('zh-CN', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

const getTextPreview = (htmlContent) => {
  // Simple HTML to text conversion for preview
  const temp = document.createElement('div')
  temp.innerHTML = htmlContent
  return temp.textContent || temp.innerText || ''
}

const calculateChanges = (newContent, oldContent) => {
  // Simple change detection based on content length difference
  if (!oldContent) return 0
  
  const newText = getTextPreview(newContent)
  const oldText = getTextPreview(oldContent)
  
  const newWords = newText.split(/\s+/).filter(w => w.length > 0)
  const oldWords = oldText.split(/\s+/).filter(w => w.length > 0)
  
  return Math.abs(newWords.length - oldWords.length)
}

const saveCurrentVersion = (isAutoSave = false, note = '') => {
  if (!props.currentContent || props.currentContent.trim().length === 0) {
    if (!isAutoSave) {
      showError('没有内容可保存')
    }
    return
  }
  
  // Skip if content hasn't changed
  if (props.currentContent === lastContent && isAutoSave) {
    return
  }
  
  const previousVersion = versions[versions.length - 1]
  const changes = calculateChanges(props.currentContent, previousVersion?.content)
  
  // Skip auto-save if changes are minimal
  if (isAutoSave && changes < 5 && versions.length > 0) {
    return
  }
  
  const version = {
    id: Date.now(),
    content: props.currentContent,
    timestamp: new Date(),
    wordCount: props.wordCount,
    changes: changes,
    isAutoSave: isAutoSave,
    note: note
  }
  
  versions.push(version)
  lastContent = props.currentContent
  lastSaved.value = new Date()
  
  // Keep only last 50 versions
  if (versions.length > 50) {
    versions.shift()
  }
  
  // Save to localStorage
  saveToLocalStorage()
  
  if (!isAutoSave) {
    showSuccess('版本已保存')
  }
}

const restoreVersion = (version) => {
  if (confirm('确定要恢复到此版本吗？当前的修改将会丢失。')) {
    emit('restore-version', version.content)
    showSuccess('版本已恢复')
  }
}

const compareWithCurrent = (version) => {
  compareVersion.value = version
  showCompareModal.value = true
}

const addVersionNote = (index) => {
  const note = prompt('为此版本添加备注:')
  if (note !== null) {
    versions[index].note = note
    saveToLocalStorage()
    if (note.trim()) {
      showSuccess('备注已添加')
    }
  }
}

const deleteVersion = (index) => {
  if (confirm('确定要删除此版本吗？')) {
    versions.splice(index, 1)
    saveToLocalStorage()
    showSuccess('版本已删除')
  }
}

const clearAllVersions = () => {
  if (confirm('确定要清空所有版本历史吗？此操作不可撤销。')) {
    versions.splice(0, versions.length)
    localStorage.removeItem('inkwell_versions')
    showSuccess('版本历史已清空')
  }
}

const saveToLocalStorage = () => {
  try {
    localStorage.setItem('inkwell_versions', JSON.stringify(versions))
  } catch (error) {
    console.warn('Failed to save versions to localStorage:', error)
  }
}

const loadFromLocalStorage = () => {
  try {
    const saved = localStorage.getItem('inkwell_versions')
    if (saved) {
      const loadedVersions = JSON.parse(saved)
      versions.splice(0, versions.length, ...loadedVersions.map(v => ({
        ...v,
        timestamp: new Date(v.timestamp)
      })))
    }
  } catch (error) {
    console.warn('Failed to load versions from localStorage:', error)
  }
}

// Watch for content changes and auto-save
watch(() => props.currentContent, (newContent) => {
  if (autoSaveEnabled.value && newContent !== lastContent) {
    // Debounce auto-save
    clearTimeout(autoSaveInterval)
    autoSaveInterval = setTimeout(() => {
      saveCurrentVersion(true)
    }, 10000) // Auto-save after 10 seconds of inactivity
  }
}, { deep: true })

// Watch auto-save toggle
watch(autoSaveEnabled, (enabled) => {
  if (enabled) {
    showSuccess('自动保存已开启')
  } else {
    showSuccess('自动保存已关闭')
    if (autoSaveInterval) {
      clearTimeout(autoSaveInterval)
    }
  }
})

// Lifecycle
onMounted(() => {
  loadFromLocalStorage()
  
  // Save current version on first load if content exists
  if (props.currentContent && props.currentContent.trim().length > 0) {
    setTimeout(() => {
      saveCurrentVersion(true)
    }, 2000)
  }
})

onUnmounted(() => {
  if (autoSaveInterval) {
    clearTimeout(autoSaveInterval)
  }
})
</script>

<style scoped>
.version-panel {
  min-height: 400px;
  max-height: 100vh;
}

.version-card {
  transition: all 0.2s ease;
}

.version-card:hover {
  transform: translateY(-1px);
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