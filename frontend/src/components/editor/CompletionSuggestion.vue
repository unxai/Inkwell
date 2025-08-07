<template>
  <div 
    v-if="visible && suggestion" 
    class="completion-suggestion"
    :style="suggestionStyle"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
  >
    <!-- 建议内容区域 -->
    <div class="suggestion-content">
      <div class="suggestion-header">
        <div class="suggestion-icon">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
        </div>
        <span class="suggestion-label">AI 建议</span>
      </div>
      
      <!-- 建议文本预览 -->
      <div class="suggestion-preview">
        <span class="suggestion-text">{{ truncatedSuggestion }}</span>
        <span v-if="isTruncated" class="suggestion-more">...</span>
      </div>
      
      <!-- 完整建议文本（悬停时显示） -->
      <div v-if="showFullText && isTruncated" class="suggestion-full-text">
        {{ suggestion }}
      </div>
    </div>
    
    <!-- 操作按钮区域 -->
    <div class="suggestion-actions">
      <button 
        class="action-button accept" 
        title="接受建议 (Tab)"
        @click="handleAccept"
      >
        <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
        接受
      </button>
      <button 
        class="action-button reject" 
        title="拒绝建议 (Esc)"
        @click="handleReject"
      >
        <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
        </svg>
        拒绝
      </button>
      <button 
        class="action-button regenerate" 
        title="重新生成 (Ctrl+R)"
        @click="handleRegenerate"
      >
        <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
        </svg>
        重试
      </button>
    </div>
    
    <!-- 快捷键提示 -->
    <div class="suggestion-shortcuts">
      <span class="shortcut-item">
        <kbd>Tab</kbd> 接受
      </span>
      <span class="shortcut-item">
        <kbd>Esc</kbd> 拒绝
      </span>
      <span class="shortcut-item">
        <kbd>Ctrl+R</kbd> 重试
      </span>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, computed, ref } from 'vue';

const props = defineProps({
  suggestion: {
    type: String,
    default: ''
  },
  visible: {
    type: Boolean,
    default: false
  },
  position: {
    type: Object,
    default: () => ({ top: 0, left: 0 })
  },
  maxPreviewLength: {
    type: Number,
    default: 100
  }
});

const emit = defineEmits(['accept', 'reject', 'regenerate']);

// 响应式状态
const showFullText = ref(false);

// 计算属性
const truncatedSuggestion = computed(() => {
  if (props.suggestion.length <= props.maxPreviewLength) {
    return props.suggestion;
  }
  return props.suggestion.slice(0, props.maxPreviewLength);
});

const isTruncated = computed(() => {
  return props.suggestion.length > props.maxPreviewLength;
});

// 智能位置计算
const suggestionStyle = computed(() => {
  const { top, left } = props.position;
  const style = {
    top: `${top + 20}px`,
    left: `${left}px`,
    transform: 'translateY(0)'
  };
  
  // 检查是否会超出视窗
  if (typeof window !== 'undefined') {
    const viewportHeight = window.innerHeight;
    const viewportWidth = window.innerWidth;
    
    // 如果建议框会超出底部，则显示在光标上方
    if (top + 200 > viewportHeight) {
      style.top = `${top - 120}px`;
    }
    
    // 如果建议框会超出右侧，则向左偏移
    if (left + 350 > viewportWidth) {
      style.left = `${Math.max(10, viewportWidth - 360)}px`;
    }
  }
  
  return style;
});

// 事件处理函数
const handleAccept = () => {
  emit('accept', props.suggestion);
};

const handleReject = () => {
  emit('reject');
};

const handleRegenerate = () => {
  emit('regenerate');
};

const handleMouseEnter = () => {
  showFullText.value = true;
};

const handleMouseLeave = () => {
  showFullText.value = false;
};
</script>

<style scoped>
.completion-suggestion {
  position: absolute;
  z-index: 1000;
  width: 350px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15), 0 4px 12px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(79, 209, 197, 0.2);
  overflow: hidden;
  animation: suggestionSlideIn 0.2s ease-out;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

@keyframes suggestionSlideIn {
  from {
    opacity: 0;
    transform: translateY(-10px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.suggestion-content {
  padding: 16px;
}

.suggestion-header {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  color: #4FD1C5;
  font-weight: 600;
  font-size: 13px;
}

.suggestion-icon {
  margin-right: 8px;
  display: flex;
  align-items: center;
}

.suggestion-preview {
  color: #374151;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 8px;
  position: relative;
}

.suggestion-text {
  display: block;
  word-break: break-word;
}

.suggestion-more {
  color: #9CA3AF;
  font-style: italic;
}

.suggestion-full-text {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  padding: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  z-index: 10;
  color: #374151;
  font-size: 14px;
  line-height: 1.5;
  max-height: 200px;
  overflow-y: auto;
  animation: fadeIn 0.15s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}

.suggestion-actions {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  background: #F9FAFB;
  border-top: 1px solid #E5E7EB;
}

.action-button {
  display: flex;
  align-items: center;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 12px;
  font-weight: 500;
  border: none;
  flex: 1;
  justify-content: center;
}

.action-button.accept {
  background: #4FD1C5;
  color: white;
}

.action-button.accept:hover {
  background: #38B2AC;
  transform: translateY(-1px);
}

.action-button.reject {
  background: #F3F4F6;
  color: #6B7280;
}

.action-button.reject:hover {
  background: #E5E7EB;
  color: #374151;
}

.action-button.regenerate {
  background: #EBF8FF;
  color: #3182CE;
}

.action-button.regenerate:hover {
  background: #BEE3F8;
  color: #2C5282;
}

.suggestion-shortcuts {
  display: flex;
  justify-content: center;
  gap: 12px;
  padding: 8px 16px;
  background: #F9FAFB;
  border-top: 1px solid #E5E7EB;
  font-size: 11px;
  color: #6B7280;
}

.shortcut-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

kbd {
  background: #E5E7EB;
  color: #374151;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  font-size: 10px;
  font-weight: 600;
  border: 1px solid #D1D5DB;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .completion-suggestion {
    width: 300px;
    left: 10px !important;
    right: 10px;
    width: calc(100vw - 20px);
    max-width: 350px;
  }
  
  .suggestion-shortcuts {
    display: none;
  }
}
</style>
