<template>
  <div class="bottom-toolbar bg-white border-t border-gray-200 p-3">
    <div class="flex items-center justify-between">
      <!-- 左侧：基础编辑工具 -->
      <div class="flex items-center space-x-2">
        <!-- 文本格式化工具组 -->
        <div class="flex items-center space-x-1 bg-gray-50 rounded-lg p-1">
          <button
            @click="handleFormat('heading1')"
            class="px-2 py-1 text-xs text-gray-700 rounded hover:bg-white hover:shadow-sm transition-all"
            title="标题1"
          >
            H1
          </button>
          <button
            @click="handleFormat('heading2')"
            class="px-2 py-1 text-xs text-gray-700 rounded hover:bg-white hover:shadow-sm transition-all"
            title="标题2"
          >
            H2
          </button>
          <button
            @click="handleFormat('heading3')"
            class="px-2 py-1 text-xs text-gray-700 rounded hover:bg-white hover:shadow-sm transition-all"
            title="标题3"
          >
            H3
          </button>
          <button
            @click="handleFormat('bold')"
            class="px-2 py-1 text-xs text-gray-700 rounded hover:bg-white hover:shadow-sm transition-all font-bold"
            title="粗体"
          >
            B
          </button>
          <button
            @click="handleFormat('italic')"
            class="px-2 py-1 text-xs text-gray-700 rounded hover:bg-white hover:shadow-sm transition-all italic"
            title="斜体"
          >
            I
          </button>
          <button
            @click="handleFormat('underline')"
            class="px-2 py-1 text-xs text-gray-700 rounded hover:bg-white hover:shadow-sm transition-all underline"
            title="下划线"
          >
            U
          </button>
          <button
            @click="handleFormat('strike')"
            class="px-2 py-1 text-xs text-gray-700 rounded hover:bg-white hover:shadow-sm transition-all line-through"
            title="删除线"
          >
            S
          </button>
        </div>
        
        <!-- 列表和引用工具组 -->
        <div class="flex items-center space-x-1 bg-green-50 rounded-lg p-1">
          <button
            @click="handleFormat('bulletList')"
            class="px-2 py-1 text-xs text-green-700 rounded hover:bg-white hover:shadow-sm transition-all"
            title="无序列表"
          >
            •
          </button>
          <button
            @click="handleFormat('orderedList')"
            class="px-2 py-1 text-xs text-green-700 rounded hover:bg-white hover:shadow-sm transition-all"
            title="有序列表"
          >
            1.
          </button>
          <button
            @click="handleFormat('blockquote')"
            class="px-2 py-1 text-xs text-green-700 rounded hover:bg-white hover:shadow-sm transition-all"
            title="引用块"
          >
            "
          </button>
          <button
            @click="handleFormat('codeBlock')"
            class="px-2 py-1 text-xs text-green-700 rounded hover:bg-white hover:shadow-sm transition-all font-mono"
            title="代码块"
          >
            &lt;&gt;
          </button>
        </div>
        
        <!-- 对齐和其他工具 -->
        <div class="flex items-center space-x-1 bg-purple-50 rounded-lg p-1">
          <button
            @click="handleFormat('alignLeft')"
            class="px-2 py-1 text-xs text-purple-700 rounded hover:bg-white hover:shadow-sm transition-all"
            title="左对齐"
          >
            ⇤
          </button>
          <button
            @click="handleFormat('alignCenter')"
            class="px-2 py-1 text-xs text-purple-700 rounded hover:bg-white hover:shadow-sm transition-all"
            title="居中对齐"
          >
            ⇋
          </button>
          <button
            @click="handleFormat('alignRight')"
            class="px-2 py-1 text-xs text-purple-700 rounded hover:bg-white hover:shadow-sm transition-all"
            title="右对齐"
          >
            ⇥
          </button>
          <button
            @click="handleFormat('horizontalRule')"
            class="px-2 py-1 text-xs text-purple-700 rounded hover:bg-white hover:shadow-sm transition-all"
            title="分割线"
          >
            ―
          </button>
        </div>
      </div>

      <!-- 中间：状态信息 -->
      <div class="flex items-center space-x-4 text-sm text-gray-500">
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
      </div>

      <!-- 右侧：AI状态 -->
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
          {{ getAiStatusText(aiStatus) }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

/**
 * 组件属性定义
 */
const props = defineProps({
  editor: {
    type: Object,
    default: null
  },
  isConnected: {
    type: Boolean,
    default: false
  },
  aiStatus: {
    type: String,
    default: 'idle'
  },
  wordCount: {
    type: Number,
    default: 0
  }
})

/**
 * 组件事件定义
 */
const emit = defineEmits([
  'format'
])

/**
 * 处理格式化操作
 */
const handleFormat = (formatType) => {
  emit('format', formatType)
}

/**
 * 获取AI状态文本
 */
const getAiStatusText = (status) => {
  if (!status) return 'AI 未知状态'
  
  // 如果是字符串，直接使用
  if (typeof status === 'string') {
    switch (status) {
      case 'idle':
      case '空闲':
      case '已连接':
        return 'AI 就绪'
      case 'processing':
      case '生成中...':
      case '改写中...':
      case '扩写中...':
      case '简化中...':
      case '处理中...':
        return 'AI 处理中'
      case '已完成':
        return 'AI 已完成'
      case 'error':
      case '错误':
      case '连接错误':
        return 'AI 错误'
      case '未连接':
        return 'AI 未连接'
      case '已取消':
        return 'AI 已取消'
      default:
        return `AI ${status}`
    }
  }
  
  // 如果是对象，尝试获取其字符串表示
  return 'AI 就绪'
}
</script>

<style scoped>
.bottom-toolbar {
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.95);
}
</style>