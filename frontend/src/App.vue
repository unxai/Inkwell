<template>
  <div class="min-h-screen bg-white text-gray-900 flex flex-col">
    <!-- 使用 Vue3 Toastify 替代原有的错误和成功提示组件 -->
    
    <main class="flex-grow">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import BaseNavigation from './components/ui/BaseNavigation.vue';
import { showSuccess, showError } from './utils/toast-service';

// 在组件挂载后设置全局消息实例
onMounted(() => {
  window.$message = {
    error: (message, duration) => {
      showError(message, { autoClose: duration || 3000 });
    },
    success: (message, duration) => {
      showSuccess(message, { autoClose: duration || 3000 });
    }
  };
});
</script>

<style>
/* 页面过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 全局样式 */
html {
  scroll-behavior: smooth;
}

body {
  font-family: 'PingFang SC', 'Helvetica Neue', 'Microsoft YaHei', sans-serif;
}

/* 自定义滚动条 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
