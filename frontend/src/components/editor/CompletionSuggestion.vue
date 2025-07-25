<template>
  <div 
    v-if="visible && suggestion" 
    class="completion-suggestion"
    :style="{ top: `${position.top}px`, left: `${position.left}px` }"
  >
    <div class="suggestion-content">
      <span class="suggestion-text">{{ suggestion }}</span>
    </div>
    <div class="suggestion-actions">
      <button 
        class="action-button accept" 
        title="接受建议 (Tab)"
        @click="handleAccept"
      >
        Accept →
      </button>
      <button 
        class="action-button reject" 
        title="拒绝建议 (Esc)"
        @click="handleReject"
      >
        Try Again
      </button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

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
  }
});

const emit = defineEmits(['accept', 'reject']);

const handleAccept = () => {
  emit('accept', props.suggestion);
};

const handleReject = () => {
  emit('reject');
};
</script>

<style scoped>
.completion-suggestion {
  position: absolute;
  z-index: 10;
  display: flex;
  flex-direction: column;
  max-width: 80%;
}

.suggestion-content {
  background-color: rgba(255, 255, 255, 0.98);
  border: 1px solid rgba(79, 209, 197, 0.3);
  border-radius: 3px;
  padding: 6px 10px;
  color: #666;
  font-style: italic;
  max-width: 100%;
  word-break: break-word;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.suggestion-text {
  white-space: normal;
  overflow-wrap: break-word;
  word-wrap: break-word;
  hyphens: auto;
  color: rgba(100, 100, 100, 0.8);
}

.suggestion-actions {
  display: flex;
  align-items: center;
  margin-top: 6px;
  gap: 6px;
}

.action-button {
  padding: 3px 10px;
  border-radius: 3px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 12px;
}

.action-button.accept {
  background-color: #4FD1C5;
  color: white;
  border: none;
}

.action-button.accept:hover {
  background-color: #3DB9B0;
}

.action-button.reject {
  background-color: transparent;
  color: #333;
  border: none;
}

.action-button.reject:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.keyboard-shortcut {
  font-size: 11px;
  color: #666;
  padding: 2px 5px;
  border: 1px solid #eee;
  border-radius: 3px;
}
</style>
