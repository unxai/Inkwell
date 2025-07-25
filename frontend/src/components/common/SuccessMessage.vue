<template>
  <div v-if="visible" class="success-message" :class="{ 'success-message--show': visible }">
    <div class="success-message__content">
      <div class="success-message__icon">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-6 h-6">
          <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm13.36-1.814a.75.75 0 10-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z" clip-rule="evenodd" />
        </svg>
      </div>
      <div class="success-message__text">{{ message }}</div>
      <button class="success-message__close" @click="hide">
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
    default: '操作成功'
  },
  duration: {
    type: Number,
    default: 3000 // 默认显示3秒
  },
  autoClose: {
    type: Boolean,
    default: true
  }
});

const visible = ref(false);
let timer = null;

// 显示成功消息
const show = () => {
  visible.value = true;
  
  if (props.autoClose && props.duration > 0) {
    clearTimeout(timer);
    timer = setTimeout(() => {
      hide();
    }, props.duration);
  }
};

// 隐藏成功消息
const hide = () => {
  visible.value = false;
  clearTimeout(timer);
};

// 创建全局成功消息实例
const createGlobalSuccessMessage = () => {
  // 创建全局方法
  window.$successMessage = {
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
  createGlobalSuccessMessage();
  
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
.success-message {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%) translateY(-100px);
  z-index: 9999;
  transition: transform 0.3s ease-in-out;
  max-width: 90%;
  width: auto;
}

.success-message--show {
  transform: translateX(-50%) translateY(0);
}

.success-message__content {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  background-color: #D1FAE5;
  border: 1px solid #A7F3D0;
  border-radius: 6px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.success-message__icon {
  flex-shrink: 0;
  color: #059669;
  width: 24px;
  height: 24px;
  margin-right: 12px;
}

.success-message__text {
  flex-grow: 1;
  font-size: 14px;
  color: #065F46;
  line-height: 1.5;
}

.success-message__close {
  flex-shrink: 0;
  background: none;
  border: none;
  cursor: pointer;
  color: #065F46;
  padding: 4px;
  margin-left: 12px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.success-message__close:hover {
  background-color: rgba(6, 95, 70, 0.1);
}
</style>