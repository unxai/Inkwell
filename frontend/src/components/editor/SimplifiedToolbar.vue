<template>
  <div class="immersive-toolbar bg-white border-b border-gray-200 px-6 py-3 shadow-sm relative">
    <div class="flex items-center justify-between max-w-6xl mx-auto">
      <!-- 左侧：基础编辑工具 -->
      <div class="flex items-center space-x-3">
        <div class="flex items-center space-x-1 bg-gray-50 rounded-lg p-1">
          <button
            @click="setHeading(1)"
            class="px-2 py-1 text-sm text-gray-700 rounded hover:bg-white hover:shadow-sm transition-all"
            title="标题1"
          >
            H1
          </button>
          <button
            @click="setHeading(2)"
            class="px-2 py-1 text-sm text-gray-700 rounded hover:bg-white hover:shadow-sm transition-all"
            title="标题2"
          >
            H2
          </button>
          <button
            @click="toggleBold"
            class="px-2 py-1 text-sm text-gray-700 rounded hover:bg-white hover:shadow-sm transition-all font-bold"
            title="粗体"
          >
            B
          </button>
          <button
            @click="toggleItalic"
            class="px-2 py-1 text-sm text-gray-700 rounded hover:bg-white hover:shadow-sm transition-all italic"
            title="斜体"
          >
            I
          </button>
          <button
            @click="toggleBulletList"
            class="px-2 py-1 text-sm text-gray-700 rounded hover:bg-white hover:shadow-sm transition-all"
            title="无序列表"
          >
            •
          </button>
          <button
            @click="toggleOrderedList"
            class="px-2 py-1 text-sm text-gray-700 rounded hover:bg-white hover:shadow-sm transition-all"
            title="有序列表"
          >
            1.
          </button>
        </div>
      </div>

      <!-- 中间：大纲工具 -->
      <div class="flex items-center space-x-3">
        <div class="flex items-center space-x-2">
          <button
            @click="showOutlineDialog = true"
            class="px-3 py-1.5 text-sm bg-indigo-50 text-indigo-700 rounded-lg hover:bg-indigo-100 transition-colors"
            title="生成大纲"
          >
            大纲
          </button>
        </div>
      </div>

      <!-- 右侧：AI 和参考文献工具 -->
      <div class="flex items-center space-x-3">
        <!-- AI 工具组 -->
        <div class="flex items-center space-x-1 bg-blue-50 rounded-lg p-1">
          <button
            @click="handleAiAction('auto-complete')"
            :disabled="!isConnected"
            class="px-2 py-1 text-sm text-blue-700 rounded hover:bg-white hover:shadow-sm disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            title="AI自动完成"
          >
            自动完成
          </button>
          <button
            @click="handleAiAction('rewrite')"
            :disabled="!isConnected"
            class="px-2 py-1 text-sm text-blue-700 rounded hover:bg-white hover:shadow-sm disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            title="AI改写"
          >
            改写
          </button>
          <button
            @click="handleAiAction('expand')"
            :disabled="!isConnected"
            class="px-2 py-1 text-sm text-blue-700 rounded hover:bg-white hover:shadow-sm disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            title="AI扩写"
          >
            扩写
          </button>
          <button
            @click="handleAiAction('simplify')"
            :disabled="!isConnected"
            class="px-2 py-1 text-sm text-blue-700 rounded hover:bg-white hover:shadow-sm disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            title="AI简化"
          >
            简化
          </button>
        </div>

        <!-- 参考文献工具组 -->
        <div class="flex items-center space-x-1 bg-emerald-50 rounded-lg p-1">
          <button
            @click="showReferenceDialog = true"
            class="px-2 py-1 text-sm text-emerald-700 rounded hover:bg-white hover:shadow-sm transition-all"
            title="管理引用"
          >
            管理引用
          </button>
          <button
            @click="handleReferenceAction('insert')"
            class="px-2 py-1 text-sm text-emerald-700 rounded hover:bg-white hover:shadow-sm transition-all"
            title="插入引用"
          >
            插入引用
          </button>
        </div>
      </div>
    </div>

    <!-- 大纲生成对话框 -->
    <div v-if="showOutlineDialog" class="absolute top-full left-1/2 transform -translate-x-1/2 mt-2 z-[9999]" @click.stop>
      <div class="bg-white rounded-lg p-6 w-96 shadow-xl border border-gray-200" @click.stop>
        <h3 class="text-lg font-semibold mb-4">生成文章大纲</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">文章主题</label>
            <input
              v-model="outlineTopicInput"
              type="text"
              placeholder="例如：人工智能在教育中的应用"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              @keyup.enter="generateOutline"
            />
          </div>
          <div class="flex space-x-3">
            <button
              @click="generateOutline"
              :disabled="!outlineTopicInput.trim()"
              class="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
            >
              生成大纲
            </button>
            <button
              @click="showOutlineDialog = false"
              class="flex-1 bg-gray-100 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-200 transition-colors"
            >
              取消
            </button>
          </div>
        </div>
      </div>
    </div>



    <!-- 参考文献管理对话框 -->
    <div v-if="showReferenceDialog" class="absolute top-full right-0 mt-2 z-[9999]" @click.stop>
      <div class="bg-white rounded-lg p-6 w-[500px] max-h-[80vh] overflow-y-auto shadow-xl border border-gray-200" @click.stop>
        <h3 class="text-lg font-semibold mb-4">管理参考文献</h3>
        
        <!-- 添加新引用 -->
        <div class="space-y-3 mb-6 p-4 bg-gray-50 rounded-lg">
          <h4 class="font-medium text-gray-800">添加新引用</h4>
          <div class="grid grid-cols-2 gap-3">
            <input
              v-model="newReference.author"
              type="text"
              placeholder="作者"
              class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm"
            />
            <input
              v-model="newReference.year"
              type="text"
              placeholder="年份"
              class="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm"
            />
          </div>
          <input
            v-model="newReference.title"
            type="text"
            placeholder="标题"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm"
          />
          <input
            v-model="newReference.publisher"
            type="text"
            placeholder="出版商/期刊"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-emerald-500 text-sm"
          />
          <button
            @click="addReference"
            :disabled="!canAddReference"
            class="w-full bg-emerald-600 text-white py-2 px-4 rounded-md hover:bg-emerald-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors text-sm"
          >
            添加引用
          </button>
        </div>

        <!-- 现有引用列表 -->
        <div class="space-y-3">
          <h4 class="font-medium text-gray-800">现有引用</h4>
          <div v-if="references.length === 0" class="text-gray-500 text-center py-4 text-sm">
            暂无参考文献
          </div>
          <div v-else class="space-y-2 max-h-60 overflow-y-auto">
            <div
              v-for="(ref, index) in references"
              :key="index"
              class="p-3 bg-gray-50 rounded-lg text-sm group relative"
            >
              <div class="font-medium text-gray-800">{{ ref.title }}</div>
              <div class="text-gray-600 text-xs mt-1">{{ ref.author }} ({{ ref.year }})</div>
              <div class="flex space-x-2 mt-2">
                <button
                  @click="insertReference(ref)"
                  class="text-xs bg-blue-600 text-white px-2 py-1 rounded hover:bg-blue-700 transition-colors"
                >
                  插入
                </button>
                <button
                  @click="removeReference(index)"
                  class="text-xs bg-red-600 text-white px-2 py-1 rounded hover:bg-red-700 transition-colors"
                >
                  删除
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="flex justify-end mt-6">
          <button
            @click="showReferenceDialog = false"
            class="bg-gray-100 text-gray-700 py-2 px-4 rounded-md hover:bg-gray-200 transition-colors"
          >
            关闭
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

/**
 * 组件属性定义
 */
const props = defineProps({
  isConnected: {
    type: Boolean,
    default: false
  },
  references: {
    type: Array,
    default: () => []
  }
})

/**
 * 组件事件定义
 */
const emit = defineEmits([
  'ai-action',
  'reference-action',
  'outline-generate',
  'format'
])

// 对话框显示状态
const showOutlineDialog = ref(false)
const showReferenceDialog = ref(false)

// 大纲生成相关
const outlineTopicInput = ref('')

// 参考文献相关
const newReference = ref({
  author: '',
  title: '',
  publisher: '',
  year: ''
})

/**
 * 计算属性：是否可以添加引用
 */
const canAddReference = computed(() => {
  return newReference.value.author.trim() && 
         newReference.value.title.trim() && 
         newReference.value.year.trim()
})

/**
 * 设置标题级别
 */
const setHeading = (level) => {
  emit('format', 'heading', { level })
}

/**
 * 切换粗体
 */
const toggleBold = () => {
  emit('format', 'bold')
}

/**
 * 切换斜体
 */
const toggleItalic = () => {
  emit('format', 'italic')
}

/**
 * 切换无序列表
 */
const toggleBulletList = () => {
  emit('format', 'bulletList')
}

/**
 * 切换有序列表
 */
const toggleOrderedList = () => {
  emit('format', 'orderedList')
}

/**
 * 处理AI操作
 */
const handleAiAction = (action) => {
  emit('ai-action', action)
}

/**
 * 处理参考文献操作
 */
const handleReferenceAction = (action) => {
  emit('reference-action', action)
}

/**
 * 生成大纲
 */
const generateOutline = () => {
  if (outlineTopicInput.value.trim()) {
    emit('outline-generate', outlineTopicInput.value.trim())
    showOutlineDialog.value = false
    outlineTopicInput.value = ''
  }
}



/**
 * 添加引用
 */
const addReference = () => {
  if (canAddReference.value) {
    emit('reference-action', 'add', { ...newReference.value })
    // 重置表单
    newReference.value = {
      author: '',
      title: '',
      publisher: '',
      year: ''
    }
  }
}

/**
 * 插入引用
 */
const insertReference = (ref) => {
  emit('reference-action', 'insert', ref)
  showReferenceDialog.value = false
}

/**
 * 删除引用
 */
const removeReference = (index) => {
  emit('reference-action', 'remove', index)
}

/**
 * 处理点击外部区域关闭弹层
 */
const handleClickOutside = (event) => {
  const target = event.target
  const toolbar = document.querySelector('.immersive-toolbar')
  
  if (toolbar && !toolbar.contains(target)) {
    showOutlineDialog.value = false
    showReferenceDialog.value = false
  }
}

// 生命周期钩子
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.immersive-toolbar {
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.95);
}

.toolbar-btn {
  transition: all 0.2s ease;
}

.toolbar-btn:hover {
  transform: translateY(-1px);
}

/* 对话框动画 */
.fixed {
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.bg-white.rounded-lg {
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>