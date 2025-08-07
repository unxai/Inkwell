<template>
  <div class="export-panel h-full flex flex-col bg-white">
    <!-- Header -->
    <div class="flex items-center justify-between p-4 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
      <div class="flex items-center space-x-2">
        <div class="w-3 h-3 rounded-full bg-blue-500"></div>
        <h3 class="text-lg font-semibold text-gray-800">导出文档</h3>
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

    <!-- Document Info -->
    <div class="p-4 border-b border-gray-100">
      <div class="flex items-center space-x-3 mb-3">
        <div class="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
          <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
        </div>
        <div>
          <h4 class="font-medium text-gray-800">当前文档</h4>
          <p class="text-sm text-gray-600">{{ wordCount }} 字 · {{ formatDate(new Date()) }}</p>
        </div>
      </div>
      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">文档标题</label>
        <input
          v-model="documentTitle"
          type="text"
          placeholder="请输入文档标题"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
        />
      </div>
    </div>

    <!-- Export Formats -->
    <div class="flex-1 overflow-y-auto p-4">
      <h4 class="font-medium text-gray-800 mb-4">选择导出格式</h4>
      
      <div class="space-y-3">
        <!-- PDF Export -->
        <div class="export-option p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-md transition-all">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-red-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/>
                <path d="M14 2v6h6M16 13a6 6 0 0 1-6 6c-3 0-6-3-6-6s3-6 6-6 6 3 6 6z"/>
                <circle cx="10" cy="13" r="2"/>
              </svg>
            </div>
            <div class="flex-1">
              <h5 class="font-medium text-gray-800">PDF 格式</h5>
              <p class="text-sm text-gray-600">适合打印和正式分享，保持格式完整</p>
            </div>
            <button
              @click="exportToPDF"
              :disabled="!canExport"
              class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
            >
              导出 PDF
            </button>
          </div>
        </div>

        <!-- Word Export -->
        <div class="export-option p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-md transition-all">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/>
                <path d="M14 2v6h6"/>
              </svg>
            </div>
            <div class="flex-1">
              <h5 class="font-medium text-gray-800">Word 格式</h5>
              <p class="text-sm text-gray-600">便于继续编辑和协作，兼容 Microsoft Word</p>
            </div>
            <button
              @click="exportToWord"
              :disabled="!canExport"
              class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
            >
              导出 Word
            </button>
          </div>
        </div>

        <!-- Markdown Export -->
        <div class="export-option p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-md transition-all">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <div class="flex-1">
              <h5 class="font-medium text-gray-800">Markdown 格式</h5>
              <p class="text-sm text-gray-600">轻量级标记语言，适合技术文档和博客</p>
            </div>
            <button
              @click="exportToMarkdown"
              :disabled="!canExport"
              class="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
            >
              导出 MD
            </button>
          </div>
        </div>

        <!-- HTML Export -->
        <div class="export-option p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-md transition-all">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4"></path>
              </svg>
            </div>
            <div class="flex-1">
              <h5 class="font-medium text-gray-800">HTML 格式</h5>
              <p class="text-sm text-gray-600">网页格式，可直接在浏览器中查看</p>
            </div>
            <button
              @click="exportToHTML"
              :disabled="!canExport"
              class="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
            >
              导出 HTML
            </button>
          </div>
        </div>

        <!-- Plain Text Export -->
        <div class="export-option p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-md transition-all">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <div class="flex-1">
              <h5 class="font-medium text-gray-800">纯文本格式</h5>
              <p class="text-sm text-gray-600">去除所有格式，只保留文本内容</p>
            </div>
            <button
              @click="exportToText"
              :disabled="!canExport"
              class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
            >
              导出 TXT
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Export Options -->
    <div class="p-4 border-t border-gray-200 bg-gray-50">
      <h5 class="font-medium text-gray-800 mb-3">导出选项</h5>
      <div class="space-y-2">
        <label class="flex items-center space-x-2">
          <input
            v-model="includeMetadata"
            type="checkbox"
            class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <span class="text-sm text-gray-700">包含文档元数据（标题、日期等）</span>
        </label>
        <label class="flex items-center space-x-2">
          <input
            v-model="includeReferences"
            type="checkbox"
            class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <span class="text-sm text-gray-700">包含参考文献列表</span>
        </label>
        <label class="flex items-center space-x-2">
          <input
            v-model="preserveFormatting"
            type="checkbox"
            class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
          />
          <span class="text-sm text-gray-700">保留原有格式</span>
        </label>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { showSuccess, showError } from '@/utils/toast-service'

const props = defineProps({
  documentContent: {
    type: String,
    default: ''
  },
  wordCount: {
    type: Number,
    default: 0
  },
  references: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['toggle-panel'])

// State
const documentTitle = ref('未命名文档')
const includeMetadata = ref(true)
const includeReferences = ref(true)
const preserveFormatting = ref(true)

// Computed
const canExport = computed(() => {
  return props.documentContent && props.documentContent.trim().length > 0
})

// Methods
const formatDate = (date) => {
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

const getDocumentMetadata = () => {
  if (!includeMetadata.value) return ''
  
  return `标题: ${documentTitle.value}
导出日期: ${formatDate(new Date())}
字数: ${props.wordCount} 字

---

`
}

const getReferencesText = () => {
  if (!includeReferences.value || props.references.length === 0) return ''
  
  let referencesText = '\n\n---\n\n参考文献\n\n'
  
  props.references.forEach((ref, index) => {
    referencesText += `[${index + 1}] ${ref.author} (${ref.year}). ${ref.title}. ${ref.publisher}.\n`
  })
  
  return referencesText
}

const htmlToText = (html) => {
  // Create a temporary DOM element to parse HTML
  const temp = document.createElement('div')
  temp.innerHTML = html
  return temp.textContent || temp.innerText || ''
}

const htmlToMarkdown = (html) => {
  // Simple HTML to Markdown conversion
  return html
    .replace(/<h1[^>]*>(.*?)<\/h1>/gi, '# $1\n\n')
    .replace(/<h2[^>]*>(.*?)<\/h2>/gi, '## $1\n\n')
    .replace(/<h3[^>]*>(.*?)<\/h3>/gi, '### $1\n\n')
    .replace(/<p[^>]*>(.*?)<\/p>/gi, '$1\n\n')
    .replace(/<strong[^>]*>(.*?)<\/strong>/gi, '**$1**')
    .replace(/<em[^>]*>(.*?)<\/em>/gi, '*$1*')
    .replace(/<ul[^>]*>(.*?)<\/ul>/gis, '$1\n')
    .replace(/<ol[^>]*>(.*?)<\/ol>/gis, '$1\n')
    .replace(/<li[^>]*>(.*?)<\/li>/gi, '- $1\n')
    .replace(/<br[^>]*>/gi, '\n')
    .replace(/<[^>]*>/g, '') // Remove remaining HTML tags
    .replace(/\n{3,}/g, '\n\n') // Clean up extra newlines
}

const downloadFile = (content, filename, type = 'text/plain') => {
  const blob = new Blob([content], { type })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
}

const exportToPDF = async () => {
  try {
    // For PDF export, we'd typically use a library like jsPDF or send to backend
    // This is a simplified version that creates an HTML page for printing to PDF
    const metadata = getDocumentMetadata()
    const references = getReferencesText()
    const content = metadata + props.documentContent + references
    
    const htmlContent = `
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>${documentTitle.value}</title>
    <style>
        body { font-family: 'Times New Roman', serif; line-height: 1.6; margin: 2cm; }
        h1 { font-size: 24px; margin-bottom: 20px; }
        h2 { font-size: 20px; margin-top: 30px; margin-bottom: 15px; }
        h3 { font-size: 16px; margin-top: 20px; margin-bottom: 10px; }
        p { margin-bottom: 12px; text-align: justify; }
        @media print { 
            body { margin: 1cm; }
            @page { margin: 2cm; }
        }
    </style>
</head>
<body>
    ${content}
</body>
</html>`
    
    // Open in new window for printing to PDF
    const printWindow = window.open('', '_blank')
    printWindow.document.write(htmlContent)
    printWindow.document.close()
    
    // Wait a bit then trigger print dialog
    setTimeout(() => {
      printWindow.print()
    }, 500)
    
    showSuccess('PDF 导出窗口已打开，请选择"打印为PDF"')
  } catch (error) {
    console.error('PDF export error:', error)
    showError('PDF 导出失败')
  }
}

const exportToWord = () => {
  try {
    const metadata = getDocumentMetadata()
    const references = getReferencesText()
    const content = metadata + props.documentContent + references
    
    // Create a simple HTML structure that Word can import
    const wordContent = `
<!DOCTYPE html>
<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word">
<head>
    <meta charset="UTF-8">
    <title>${documentTitle.value}</title>
    <!--[if gte mso 9]>
    <xml><w:WordDocument><w:View>Print</w:View><w:Zoom>90</w:Zoom></w:WordDocument></xml>
    <![endif]-->
    <style>
        @page { margin: 2.5cm; }
        body { font-family: 'Times New Roman', serif; line-height: 1.6; }
        h1 { font-size: 16pt; font-weight: bold; }
        h2 { font-size: 14pt; font-weight: bold; }
        h3 { font-size: 12pt; font-weight: bold; }
        p { font-size: 12pt; }
    </style>
</head>
<body>
    ${content}
</body>
</html>`
    
    const filename = `${documentTitle.value || '文档'}.doc`
    downloadFile(wordContent, filename, 'application/msword')
    showSuccess('Word 文档已导出')
  } catch (error) {
    console.error('Word export error:', error)
    showError('Word 导出失败')
  }
}

const exportToMarkdown = () => {
  try {
    const metadata = includeMetadata.value ? `# ${documentTitle.value}\n\n导出日期: ${formatDate(new Date())}\n字数: ${props.wordCount} 字\n\n---\n\n` : ''
    const markdownContent = htmlToMarkdown(props.documentContent)
    const references = getReferencesText()
    
    const content = metadata + markdownContent + references
    const filename = `${documentTitle.value || '文档'}.md`
    
    downloadFile(content, filename, 'text/markdown')
    showSuccess('Markdown 文档已导出')
  } catch (error) {
    console.error('Markdown export error:', error)
    showError('Markdown 导出失败')
  }
}

const exportToHTML = () => {
  try {
    const metadata = getDocumentMetadata()
    const references = getReferencesText()
    
    const htmlContent = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${documentTitle.value}</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            line-height: 1.6; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px; 
            color: #333; 
        }
        h1 { color: #1a365d; border-bottom: 2px solid #4fd1c5; padding-bottom: 10px; }
        h2 { color: #2d3748; margin-top: 30px; }
        h3 { color: #4a5568; }
        p { margin-bottom: 15px; text-align: justify; }
        pre { background: #f7fafc; padding: 15px; border-radius: 8px; overflow-x: auto; }
        code { background: #edf2f7; padding: 2px 4px; border-radius: 4px; }
        blockquote { border-left: 4px solid #4fd1c5; padding-left: 20px; margin-left: 0; font-style: italic; }
    </style>
</head>
<body>
    <pre>${metadata}</pre>
    ${props.documentContent}
    <pre>${references}</pre>
</body>
</html>`
    
    const filename = `${documentTitle.value || '文档'}.html`
    downloadFile(htmlContent, filename, 'text/html')
    showSuccess('HTML 文档已导出')
  } catch (error) {
    console.error('HTML export error:', error)
    showError('HTML 导出失败')
  }
}

const exportToText = () => {
  try {
    const metadata = getDocumentMetadata()
    const textContent = htmlToText(props.documentContent)
    const references = getReferencesText()
    
    const content = metadata + textContent + references
    const filename = `${documentTitle.value || '文档'}.txt`
    
    downloadFile(content, filename, 'text/plain')
    showSuccess('文本文档已导出')
  } catch (error) {
    console.error('Text export error:', error)
    showError('文本导出失败')
  }
}
</script>

<style scoped>
.export-panel {
  min-height: 400px;
  max-height: 100vh;
}

.export-option {
  transition: all 0.2s ease;
}

.export-option:hover {
  transform: translateY(-1px);
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