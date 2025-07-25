<template>
  <div class="min-h-screen bg-white text-gray-900 flex flex-col">
    <!-- 错误提示组件 -->
    <ErrorMessage ref="errorMessageRef" />
    <!-- 成功提示组件 -->
    <SuccessMessage ref="successMessageRef" />
    <header class="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-10">
      <div class="container mx-auto px-4 py-3 flex items-center justify-between">
        <div class="flex items-center">
          <router-link to="/" class="flex items-center">
            <h1 class="text-2xl font-bold text-[#1A365D]">墨井</h1>
            <span class="ml-2 text-sm text-gray-500">智能写作助手</span>
          </router-link>
        </div>
        
        <!-- 桌面导航 -->
        <nav class="hidden md:flex space-x-6">
          <router-link to="/" class="text-gray-700 hover:text-[#4FD1C5] transition-colors duration-200" active-class="text-[#4FD1C5] font-medium">智能编辑器</router-link>
          <router-link to="/academic" class="text-gray-700 hover:text-[#4FD1C5] transition-colors duration-200" active-class="text-[#4FD1C5] font-medium">学术论文</router-link>
          <router-link to="/reference" class="text-gray-700 hover:text-[#4FD1C5] transition-colors duration-200" active-class="text-[#4FD1C5] font-medium">引用管理</router-link>
        </nav>
        
        <!-- 移动端菜单按钮 -->
        <button 
          @click="isMobileMenuOpen = !isMobileMenuOpen" 
          class="md:hidden flex items-center p-2 rounded-md text-gray-700 hover:text-[#4FD1C5] hover:bg-gray-100 focus:outline-none"
        >
          <svg v-if="!isMobileMenuOpen" class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
          <svg v-else class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <!-- 移动端导航菜单 -->
      <div 
        v-show="isMobileMenuOpen" 
        class="md:hidden bg-white border-b border-gray-200"
      >
        <div class="container mx-auto px-4 py-2 space-y-2">
          <router-link 
            v-for="(link, index) in navLinks" 
            :key="index" 
            :to="link.path" 
            class="block py-2 px-4 text-gray-700 hover:bg-gray-100 hover:text-[#4FD1C5] rounded-md transition-colors duration-200"
            active-class="bg-gray-100 text-[#4FD1C5] font-medium"
            @click="isMobileMenuOpen = false"
          >
            {{ link.name }}
          </router-link>
        </div>
      </div>
    </header>
    
    <main class="flex-grow">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    
    <footer class="bg-gray-50 border-t border-gray-200 py-4">
      <div class="container mx-auto px-4 text-center text-sm text-gray-500">
        <p>&copy; {{ new Date().getFullYear() }} 墨井智能写作助手</p>
        <p class="mt-1">传统写作与现代智能的完美结合</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ErrorMessage from './components/common/ErrorMessage.vue';
import SuccessMessage from './components/common/SuccessMessage.vue';

// 移动端菜单状态
const isMobileMenuOpen = ref(false);

// 错误消息组件引用
const errorMessageRef = ref(null);

// 成功消息组件引用
const successMessageRef = ref(null);

// 在组件挂载后设置全局消息实例
onMounted(() => {
  window.$message = {
    error: (message, duration) => {
      if (errorMessageRef.value) {
        errorMessageRef.value.show(message, duration);
      }
    },
    success: (message, duration) => {
      if (successMessageRef.value) {
        successMessageRef.value.show(message, duration);
      }
    }
  };
});

// 导航链接
const navLinks = [
  { name: '智能编辑器', path: '/' },
  { name: '学术论文', path: '/academic' },
  { name: '引用管理', path: '/reference' }
];
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
