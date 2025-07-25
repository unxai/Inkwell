<template>
  <div v-if="visible" class="error-message" :class="{ 'error-message--show': visible }">
    <div class="error-message__content">
      <div class="error-message__icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
          <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm-1.72 6.97a.75.75 0 10-1.06 1.06L10.94 12l-1.72 1.72a.75.75 0 101.06 1.06L12 13.06l1.72 1.72a.75.75 0 101.06-1.06L13.06 12l1.72-1.72a.75.75 0 10-1.06-1.06L12 10.94l-1.72-1.72z" clip-rule="evenodd" />
        </svg>
      </div>
      <div class="error-message__text">{{ message }}</div>
      <button class="error-message__close" @click="hide">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
          <path fill-rule="evenodd" d="M5.47 5.47a.75.75 0 011.06 0L12 10.94l5.47-5.47a.75.75 0 111.06 1.06L13.06 12l5.47 5.47a.75.75 0 11-1.06 1.06L12 13.06l-5.47 5.47a.75.75 0 01-1.06-1.06L10.94 12 5.47 6.53a.75.75 0 010-1.06z" clip-rule="evenodd" />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';

const props = defineProps({
  message: {
    type: String,
    default: '发生错误，请稍后重试'
  },
  duration: {
    type: Number,
    default: 5000 // 默认显示5秒
  },
  autoClose: {
    type: Boolean,
    default: true
  }
});

const visible = ref(false);
let timer = null;

// 显示错误消息
const show = () => {
  visible.value = true;
  
  if (props.autoClose && props.duration > 0) {
    clearTimeout(timer);
    timer = setTimeout(() => {
      hide();
    }, props.duration);
  }
};

// 隐藏错误消息
const hide = () => {
  visible.value = false;
  clearTimeout(timer);
};

// 创建全局错误消息实例
const createGlobalErrorMessage = () => {
  // 创建全局方法
  window.$errorMessage = {
    show: (message, duration) => {
      // 更新消息
      if (message) {
        props.message = message;
      }
      
      // 更新持续时间
      if (duration !== undefined) {
        props.duration = duration;
      }
      
      // 显示消息
      show();
    },
    hide
  };
};

onMounted(() => {
  createGlobalErrorMessage();
  
  // 默认不显示
  visible.value = false;
});

onBeforeUnmount(() => {
  clearTimeout(timer);
});

// 导出方法供外部使用
defineExpose({
  show,
  hide
});
</script>

<style scoped>
.error-message {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%) translateY(-100px);
  z-index: 9999;
  transition: transform 0.3s ease-in-out;
  max-width: 90%;
  width: auto;
}

.error-message--show {
  transform: translateX(-50%) translateY(0);
}

.error-message__content {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background-color: #FEE2E2;
  border: 1px solid #FECACA;
  border-radius: 6px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.error-message__icon {
  flex-shrink: 0;
  color: #DC2626;
  width: 24px;
  height: 24px;
  margin-right: 12px;
}

.error-message__text {
  flex-grow: 1;
  font-size: 14px;
  color: #991B1B;
  line-height: 1.5;
}

.error-message__close {
  flex-shrink: 0;
  background: none;
  border: none;
  cursor: pointer;
  color: #991B1B;
  padding: 4px;
  margin-left: 12px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-message__close:hover {
  background-color: rgba(153, 27, 27, 0.1);
}
</style>