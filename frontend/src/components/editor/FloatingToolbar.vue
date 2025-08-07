<template>
  <div 
    v-if="show && selectedText"
    :style="{ top: position.top + 'px', left: position.left + 'px' }"
    class="floating-toolbar fixed z-[9999] animate-fadeIn"
  >
    <div class="toolbar-container bg-white rounded-xl shadow-2xl border border-gray-100 p-2 flex items-center space-x-1">
      <!-- AI 文本处理功能 -->
      <div class="flex items-center space-x-1">
        <button
          @click="$emit('action', 'auto-complete')"
          :disabled="props.isProcessing"
          class="toolbar-btn bg-gradient-to-r from-emerald-500 to-emerald-600 text-white hover:from-emerald-600 hover:to-emerald-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center transition-all duration-200 transform hover:scale-105 active:scale-95"
          title="AI智能续写"
        >
          <div v-if="props.isProcessing && props.processingType === 'auto-complete'" class="animate-spin rounded-full h-3 w-3 border-b border-white mr-1"></div>
          <span v-if="props.isProcessing && props.processingType === 'auto-complete'" class="text-xs">续写中...</span>
          <span v-else class="flex items-center">
            <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
            </svg>
            <span class="text-xs font-medium">续写</span>
          </span>
        </button>
        
        <button
          @click="$emit('action', 'rewrite')"
          :disabled="props.isProcessing"
          class="toolbar-btn bg-gradient-to-r from-blue-500 to-blue-600 text-white hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center transition-all duration-200 transform hover:scale-105 active:scale-95"
          title="AI改写文本"
        >
          <div v-if="props.isProcessing && props.processingType === 'rewrite'" class="animate-spin rounded-full h-3 w-3 border-b border-white mr-1"></div>
          <span v-if="props.isProcessing && props.processingType === 'rewrite'" class="text-xs">改写中...</span>
          <span v-else class="flex items-center">
            <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
            </svg>
            <span class="text-xs font-medium">改写</span>
          </span>
        </button>
        
        <button
          @click="$emit('action', 'expand')"
          :disabled="props.isProcessing"
          class="toolbar-btn bg-gradient-to-r from-purple-500 to-purple-600 text-white hover:from-purple-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center transition-all duration-200 transform hover:scale-105 active:scale-95"
          title="AI扩写文本"
        >
          <div v-if="props.isProcessing && props.processingType === 'expand'" class="animate-spin rounded-full h-3 w-3 border-b border-white mr-1"></div>
          <span v-if="props.isProcessing && props.processingType === 'expand'" class="text-xs">扩写中...</span>
          <span v-else class="flex items-center">
            <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8h16M4 16h16"></path>
            </svg>
            <span class="text-xs font-medium">扩写</span>
          </span>
        </button>
        
        <button
          @click="$emit('action', 'simplify')"
          :disabled="props.isProcessing"
          class="toolbar-btn bg-gradient-to-r from-amber-500 to-amber-600 text-white hover:from-amber-600 hover:to-amber-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center transition-all duration-200 transform hover:scale-105 active:scale-95"
          title="AI简化文本"
        >
          <div v-if="props.isProcessing && props.processingType === 'simplify'" class="animate-spin rounded-full h-3 w-3 border-b border-white mr-1"></div>
          <span v-if="props.isProcessing && props.processingType === 'simplify'" class="text-xs">简化中...</span>
          <span v-else class="flex items-center">
            <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path>
            </svg>
            <span class="text-xs font-medium">简化</span>
          </span>
        </button>
      </div>
      
      <div class="w-px h-6 bg-gray-200 mx-1"></div>
      
      <!-- 其他功能 -->
      <div class="flex items-center space-x-1">
        <button
          @click="$emit('action', 'insert-reference')"
          :disabled="props.isProcessing"
          class="toolbar-btn bg-gradient-to-r from-teal-500 to-teal-600 text-white hover:from-teal-600 hover:to-teal-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center transition-all duration-200 transform hover:scale-105 active:scale-95"
          title="插入引用"
        >
          <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
          </svg>
          <span class="text-xs font-medium">引用</span>
        </button>
        
        <button
          @click="$emit('action', 'translate')"
          :disabled="props.isProcessing"
          class="toolbar-btn bg-gradient-to-r from-indigo-500 to-indigo-600 text-white hover:from-indigo-600 hover:to-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center transition-all duration-200 transform hover:scale-105 active:scale-95"
          title="翻译文本"
        >
          <div v-if="props.isProcessing && props.processingType === 'translate'" class="animate-spin rounded-full h-3 w-3 border-b border-white mr-1"></div>
          <span v-if="props.isProcessing && props.processingType === 'translate'" class="text-xs">翻译中...</span>
          <span v-else class="flex items-center">
            <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"></path>
            </svg>
            <span class="text-xs font-medium">翻译</span>
          </span>
        </button>
      </div>
    </div>
    
    <!-- 添加三角形指示器，指向选中文本的位置 -->
    <div 
      class="toolbar-arrow absolute"
      :style="getArrowPosition()"
    >
      <div class="w-0 h-0 border-l-4 border-r-4 border-t-4 border-l-transparent border-r-transparent border-t-white"></div>
      <div class="w-0 h-0 border-l-[5px] border-r-[5px] border-t-[5px] border-l-transparent border-r-transparent border-t-gray-100 absolute top-[-1px] left-1/2 transform -translate-x-1/2"></div>
    </div>
  </div>
</template>

<script setup>
/**
 * 组件属性定义
 */
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  position: {
    type: Object,
    default: () => ({ top: 0, left: 0 })
  },
  selectedText: {
    type: String,
    default: ''
  },
  isProcessing: {
    type: Boolean,
    default: false
  },
  processingType: {
    type: String,
    default: ''
  }
})

/**
 * 组件事件定义
 */
const emit = defineEmits(['action'])

/**
 * 计算箭头位置 - 优化定位逻辑
 */
const getArrowPosition = () => {
  // 获取当前视口高度的中点
  const viewportMiddle = window.innerHeight / 2
  
  // 判断工具条是在视口上半部分还是下半部分
  const isToolbarInUpperHalf = props.position.top < viewportMiddle
  
  if (isToolbarInUpperHalf) {
    // 工具条在视口上半部分，通常显示在选中文本下方，箭头在工具条顶部
    return {
      top: '-8px',
      left: '50%',
      transform: 'translateX(-50%) rotate(180deg)'
    }
  } else {
    // 工具条在视口下半部分，通常显示在选中文本上方，箭头在工具条底部
    return {
      top: '100%',
      left: '50%',
      transform: 'translateX(-50%)'
    }
  }
}
</script>

<style scoped>
.floating-toolbar {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  pointer-events: auto; /* 确保可以点击 */
}

.toolbar-container {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: 
    0 10px 25px -5px rgba(0, 0, 0, 0.1),
    0 4px 6px -2px rgba(0, 0, 0, 0.05),
    0 0 0 1px rgba(255, 255, 255, 0.05),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  /* 确保工具条有固定宽度 */
  width: 350px;
  max-width: 350px;
}

.toolbar-btn {
  @apply px-3 py-2 rounded-lg text-xs font-medium min-w-0 relative overflow-hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.toolbar-btn:before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s;
}

.toolbar-btn:hover:before {
  left: 100%;
}

.toolbar-btn:disabled:before {
  display: none;
}

/* 按钮激活状态效果 */
.toolbar-btn:active {
  transform: scale(0.95) translateY(1px);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

/* 工具条入场动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 工具条箭头指示器 */
.toolbar-arrow {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
  pointer-events: none; /* 箭头不响应点击 */
}

/* 响应式设计 */
@media (max-width: 640px) {
  .toolbar-container {
    @apply p-1.5;
    width: 300px;
    max-width: 300px;
  }
  
  .toolbar-btn {
    @apply px-2 py-1.5 text-xs;
    min-width: auto;
  }
  
  .toolbar-btn svg {
    @apply w-3 h-3;
  }
  
  .toolbar-btn span {
    @apply hidden;
  }
  
  /* 在小屏幕上只显示图标 */
  .toolbar-btn svg {
    margin-right: 0 !important;
  }
}

/* 高对比度模式支持 */
@media (prefers-contrast: high) {
  .toolbar-container {
    background: white;
    border: 2px solid #000;
    backdrop-filter: none;
    -webkit-backdrop-filter: none;
  }
  
  .toolbar-btn {
    border: 1px solid currentColor;
  }
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .toolbar-container {
    background: rgba(31, 41, 55, 0.95);
    border-color: rgba(75, 85, 99, 0.3);
    color: white;
  }
  
  .toolbar-arrow > div:first-child {
    border-top-color: rgba(31, 41, 55, 0.95);
  }
  
  .toolbar-arrow > div:last-child {
    border-top-color: rgba(75, 85, 99, 0.3);
  }
}

/* 减少动画偏好设置 */
@media (prefers-reduced-motion: reduce) {
  .animate-fadeIn {
    animation: none;
  }
  
  .toolbar-btn {
    transition: none;
  }
  
  .toolbar-btn:before {
    transition: none;
  }
}
</style>