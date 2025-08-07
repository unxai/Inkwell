<template>
  <div class="citation-manager h-full flex flex-col bg-white">
    <!-- Header -->
    <div class="flex items-center justify-between p-4 border-b border-gray-200 bg-gradient-to-r from-emerald-50 to-teal-50">
      <div class="flex items-center space-x-2">
        <div class="w-3 h-3 rounded-full bg-emerald-500"></div>
        <h3 class="text-lg font-semibold text-gray-800">引用管理</h3>
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

    <!-- Citation Style Selection -->
    <div class="p-4 border-b border-gray-100">
      <label class="block text-sm font-medium text-gray-700 mb-2">引用格式</label>
      <select
        v-model="selectedStyle"
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm"
      >
        <option value="apa">APA 格式</option>
        <option value="mla">MLA 格式</option>
        <option value="chicago">芝加哥格式</option>
        <option value="harvard">哈佛格式</option>
        <option value="ieee">IEEE 格式</option>
        <option value="gb7714">国标 GB/T 7714</option>
      </select>
    </div>

    <!-- Add Reference Form -->
    <div class="p-4 border-b border-gray-100">
      <button
        @click="showAddForm = !showAddForm"
        class="w-full px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors text-sm font-medium mb-3"
      >
        ➕ {{ showAddForm ? '收起' : '添加新引用' }}
      </button>

      <div v-if="showAddForm" class="space-y-3 bg-gray-50 p-4 rounded-lg">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">引用类型</label>
          <select
            v-model="newReference.type"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm"
          >
            <option value="journal">期刊论文</option>
            <option value="book">书籍</option>
            <option value="conference">会议论文</option>
            <option value="webpage">网页</option>
            <option value="thesis">学位论文</option>
            <option value="report">研究报告</option>
          </select>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">作者</label>
            <input
              v-model="newReference.author"
              type="text"
              placeholder="Zhang, L."
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm"
            />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">年份</label>
            <input
              v-model="newReference.year"
              type="text"
              placeholder="2024"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm"
            />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">标题</label>
          <input
            v-model="newReference.title"
            type="text"
            placeholder="文章或书籍标题"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm"
          />
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">期刊/出版社</label>
            <input
              v-model="newReference.publisher"
              type="text"
              placeholder="期刊名称或出版社"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm"
            />
          </div>
          <div v-if="newReference.type === 'journal'">
            <label class="block text-sm font-medium text-gray-700 mb-1">卷期号</label>
            <input
              v-model="newReference.volume"
              type="text"
              placeholder="Vol. 1, No. 1"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm"
            />
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">页码</label>
            <input
              v-model="newReference.pages"
              type="text"
              placeholder="1-10"
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm"
            />
          </div>
          <div v-if="newReference.type === 'webpage'">
            <label class="block text-sm font-medium text-gray-700 mb-1">URL</label>
            <input
              v-model="newReference.url"
              type="url"
              placeholder="https://..."
              class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm"
            />
          </div>
        </div>

        <div v-if="newReference.type === 'webpage'">
          <label class="block text-sm font-medium text-gray-700 mb-1">访问日期</label>
          <input
            v-model="newReference.accessDate"
            type="date"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm"
          />
        </div>

        <button
          @click="addReference"
          :disabled="!canAddReference"
          class="w-full bg-emerald-600 text-white py-2 px-4 rounded-lg hover:bg-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm font-medium"
        >
          添加引用
        </button>
      </div>
    </div>

    <!-- References List -->
    <div class="flex-1 overflow-y-auto p-4">
      <div class="flex items-center justify-between mb-4">
        <h4 class="font-medium text-gray-800">引用列表 ({{ references.length }})</h4>
        <div class="flex space-x-2">
          <button
            @click="exportReferences"
            :disabled="references.length === 0"
            class="px-3 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            导出
          </button>
          <button
            @click="clearAllReferences"
            :disabled="references.length === 0"
            class="px-3 py-1 text-xs bg-red-600 text-white rounded hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            清空
          </button>
        </div>
      </div>

      <div v-if="references.length === 0" class="text-center py-8">
        <div class="text-4xl mb-2">📚</div>
        <p class="text-gray-500 text-sm">还没有添加任何引用</p>
      </div>

      <div class="space-y-3">
        <div
          v-for="(reference, index) in references"
          :key="reference.id || index"
          class="reference-card p-4 border border-gray-200 rounded-lg hover:border-emerald-300 hover:shadow-md transition-all"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="flex-1">
              <div class="flex items-center space-x-2 mb-2">
                <span class="px-2 py-0.5 bg-emerald-100 text-emerald-700 text-xs rounded-full">
                  {{ getReferenceTypeLabel(reference.type) }}
                </span>
                <span class="text-xs text-gray-500">{{ reference.year }}</span>
              </div>
              <h5 class="font-medium text-gray-800 text-sm mb-1 line-clamp-2">
                {{ reference.title }}
              </h5>
              <p class="text-xs text-gray-600 mb-2">
                {{ reference.author }}
              </p>
            </div>
            <div class="flex space-x-1 ml-3">
              <button
                @click="editReference(index)"
                class="p-1 text-gray-400 hover:text-blue-500 transition-colors"
                title="编辑"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                </svg>
              </button>
              <button
                @click="deleteReference(index)"
                class="p-1 text-gray-400 hover:text-red-500 transition-colors"
                title="删除"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
              </button>
            </div>
          </div>

          <!-- Formatted Reference -->
          <div class="text-xs text-gray-700 bg-gray-50 p-3 rounded border-l-4 border-emerald-400 mb-3">
            <div v-html="formatReference(reference)"></div>
          </div>

          <!-- Actions -->
          <div class="flex space-x-2">
            <button
              @click="insertInlineCitation(reference)"
              class="text-xs px-3 py-1 bg-emerald-600 text-white rounded hover:bg-emerald-700 transition-colors"
            >
              插入内文引用
            </button>
            <button
              @click="insertFullCitation(reference)"
              class="text-xs px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
            >
              插入完整引用
            </button>
            <button
              @click="copyReference(reference)"
              class="text-xs px-3 py-1 bg-gray-600 text-white rounded hover:bg-gray-700 transition-colors"
            >
              复制
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Generate Bibliography Button -->
    <div v-if="references.length > 0" class="p-4 border-t border-gray-200">
      <button
        @click="generateBibliography"
        class="w-full px-4 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium"
      >
        📋 生成参考文献列表
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { showSuccess, showError } from '@/utils/toast-service'

const props = defineProps({
  references: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['toggle-panel', 'add-reference', 'update-reference', 'delete-reference', 'insert-text'])

// State
const selectedStyle = ref('apa')
const showAddForm = ref(false)

const newReference = reactive({
  type: 'journal',
  author: '',
  year: '',
  title: '',
  publisher: '',
  volume: '',
  pages: '',
  url: '',
  accessDate: ''
})

// Computed
const canAddReference = computed(() => {
  return newReference.author.trim() && 
         newReference.title.trim() && 
         newReference.year.trim()
})

// Methods
const getReferenceTypeLabel = (type) => {
  const labels = {
    journal: '期刊',
    book: '书籍',
    conference: '会议',
    webpage: '网页',
    thesis: '学位论文',
    report: '报告'
  }
  return labels[type] || '其他'
}

const formatReference = (reference) => {
  const style = selectedStyle.value
  
  switch (style) {
    case 'apa':
      return formatAPA(reference)
    case 'mla':
      return formatMLA(reference)
    case 'chicago':
      return formatChicago(reference)
    case 'harvard':
      return formatHarvard(reference)
    case 'ieee':
      return formatIEEE(reference)
    case 'gb7714':
      return formatGB7714(reference)
    default:
      return formatAPA(reference)
  }
}

const formatAPA = (ref) => {
  let citation = `${ref.author} (${ref.year}). <em>${ref.title}</em>.`
  
  if (ref.type === 'journal') {
    citation += ` <em>${ref.publisher}</em>`
    if (ref.volume) citation += `, ${ref.volume}`
    if (ref.pages) citation += `, ${ref.pages}`
  } else if (ref.type === 'book') {
    citation += ` ${ref.publisher}.`
  } else if (ref.type === 'webpage') {
    citation += ` Retrieved from ${ref.url}`
    if (ref.accessDate) citation += ` (accessed ${ref.accessDate})`
  }
  
  return citation + '.'
}

const formatMLA = (ref) => {
  let citation = `${ref.author}. "${ref.title}."`
  
  if (ref.type === 'journal') {
    citation += ` <em>${ref.publisher}</em>`
    if (ref.volume) citation += `, vol. ${ref.volume}`
    citation += `, ${ref.year}`
    if (ref.pages) citation += `, pp. ${ref.pages}`
  } else if (ref.type === 'book') {
    citation += ` ${ref.publisher}, ${ref.year}.`
  }
  
  return citation + '.'
}

const formatChicago = (ref) => {
  let citation = `${ref.author}. "${ref.title}."`
  
  if (ref.type === 'journal') {
    citation += ` <em>${ref.publisher}</em>`
    if (ref.volume) citation += ` ${ref.volume}`
    citation += ` (${ref.year})`
    if (ref.pages) citation += `: ${ref.pages}`
  }
  
  return citation + '.'
}

const formatHarvard = (ref) => {
  return `${ref.author} (${ref.year}) '${ref.title}', <em>${ref.publisher}</em>${ref.pages ? `, pp. ${ref.pages}` : ''}.`
}

const formatIEEE = (ref) => {
  return `${ref.author}, "${ref.title}," <em>${ref.publisher}</em>${ref.volume ? `, vol. ${ref.volume}` : ''}${ref.pages ? `, pp. ${ref.pages}` : ''}, ${ref.year}.`
}

const formatGB7714 = (ref) => {
  return `${ref.author}. ${ref.title}[J]. ${ref.publisher}, ${ref.year}${ref.volume ? `, ${ref.volume}` : ''}${ref.pages ? `: ${ref.pages}` : ''}.`
}

const addReference = () => {
  if (!canAddReference.value) return
  
  const reference = {
    id: Date.now(),
    ...newReference
  }
  
  emit('add-reference', reference)
  
  // Reset form
  Object.assign(newReference, {
    type: 'journal',
    author: '',
    year: '',
    title: '',
    publisher: '',
    volume: '',
    pages: '',
    url: '',
    accessDate: ''
  })
  
  showAddForm.value = false
  showSuccess('引用已添加')
}

const editReference = (index) => {
  // TODO: Implement edit functionality
  showError('编辑功能开发中')
}

const deleteReference = (index) => {
  emit('delete-reference', index)
  showSuccess('引用已删除')
}

const insertInlineCitation = (reference) => {
  let citation = ''
  
  switch (selectedStyle.value) {
    case 'apa':
    case 'harvard':
      citation = `(${reference.author}, ${reference.year})`
      break
    case 'mla':
      citation = `(${reference.author} ${reference.year})`
      break
    case 'chicago':
      citation = `(${reference.author} ${reference.year})`
      break
    case 'ieee':
      citation = `[${props.references.indexOf(reference) + 1}]`
      break
    case 'gb7714':
      citation = `[${props.references.indexOf(reference) + 1}]`
      break
  }
  
  emit('insert-text', citation)
  showSuccess('内文引用已插入')
}

const insertFullCitation = (reference) => {
  const citation = formatReference(reference)
  emit('insert-text', `\n\n${citation}\n\n`)
  showSuccess('完整引用已插入')
}

const copyReference = async (reference) => {
  try {
    const citation = formatReference(reference)
    // Remove HTML tags for clipboard
    const plainText = citation.replace(/<[^>]*>/g, '')
    await navigator.clipboard.writeText(plainText)
    showSuccess('引用已复制到剪贴板')
  } catch (error) {
    showError('复制失败')
  }
}

const generateBibliography = () => {
  let bibliography = '\n\n<h2>参考文献</h2>\n\n'
  
  props.references.forEach((ref, index) => {
    if (selectedStyle.value === 'ieee' || selectedStyle.value === 'gb7714') {
      bibliography += `<p>[${index + 1}] ${formatReference(ref)}</p>\n`
    } else {
      bibliography += `<p>${formatReference(ref)}</p>\n`
    }
  })
  
  bibliography += '\n'
  
  emit('insert-text', bibliography)
  showSuccess('参考文献列表已插入')
}

const exportReferences = () => {
  // Generate exportable bibliography
  let exportText = `参考文献 (${selectedStyle.value.toUpperCase()} 格式)\n\n`
  
  props.references.forEach((ref, index) => {
    const plainText = formatReference(ref).replace(/<[^>]*>/g, '')
    if (selectedStyle.value === 'ieee' || selectedStyle.value === 'gb7714') {
      exportText += `[${index + 1}] ${plainText}\n\n`
    } else {
      exportText += `${plainText}\n\n`
    }
  })
  
  // Create downloadable file
  const blob = new Blob([exportText], { type: 'text/plain' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `references_${selectedStyle.value}_${new Date().toISOString().split('T')[0]}.txt`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  
  showSuccess('参考文献已导出')
}

const clearAllReferences = () => {
  if (confirm('确定要清空所有引用吗？此操作不可撤销。')) {
    // Clear all references through parent component
    for (let i = props.references.length - 1; i >= 0; i--) {
      emit('delete-reference', i)
    }
    showSuccess('所有引用已清空')
  }
}
</script>

<style scoped>
.citation-manager {
  min-height: 400px;
  max-height: 100vh;
}

.reference-card {
  transition: all 0.2s ease;
}

.reference-card:hover {
  transform: translateY(-1px);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
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