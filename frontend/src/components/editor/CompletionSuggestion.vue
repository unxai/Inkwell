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
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
        </svg>
      </button>
      <button 
        class="action-button reject" 
        title="拒绝建议 (Esc)"
        @click="handleReject"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
        </svg>
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
  align-items: center;
  max-width: 80%;
}

.suggestion-content {
  background-color: rgba(79, 209, 197, 0.1);
  border: 1px solid rgba(79, 209, 197, 0.3);
  border-radius: 4px;
  padding: 2px 6px;
  color: #666;
  font-style: italic;
}

.suggestion-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.suggestion-actions {
  display: flex;
  margin-left: 4px;
}

.action-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin-left: 2px;
  cursor: pointer;
  transition: all 0.2s;
}

.action-button.accept {
  background-color: rgba(79, 209, 197, 0.2);
  color: #1A365D;
}

.action-button.accept:hover {
  background-color: rgba(79, 209, 197, 0.4);
}

.action-button.reject {
  background-color: rgba(229, 62, 62, 0.1);
  color: #822727;
}

.action-button.reject:hover {
  background-color: rgba(229, 62, 62, 0.2);
}
</style>