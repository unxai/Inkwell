<template>
  <div class="ai-assist-panel">
    <h2 class="text-base font-bold mb-3 text-[#1A365D] flex items-center">
      <svg class="w-4 h-4 mr-1.5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <path d="M12 16v-4"></path>
        <path d="M12 8h.01"></path>
      </svg>
      AI 辅助功能
    </h2>
    
    <div class="space-y-2">
      <!-- 自动完成 -->
      <div 
        class="p-2 border border-gray-200 rounded-md hover:border-[#4FD1C5] hover:bg-gray-50 transition-all cursor-pointer group"
        :class="{'opacity-60 cursor-not-allowed': !isConnected}"
        @click="isConnected && handleAutoComplete()"
      >
        <div class="flex items-center justify-between">
          <h3 class="font-medium text-[#1A365D] group-hover:text-[#4FD1C5] transition-colors text-sm">自动完成</h3>
          <svg class="w-3.5 h-3.5 text-gray-400 group-hover:text-[#4FD1C5] transition-colors" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </div>
        <p class="text-xs text-gray-600 mt-0.5">实时生成文本建议</p>
      </div>
      
      <!-- 改写内容 -->
      <div 
        class="p-2 border border-gray-200 rounded-md hover:border-[#4FD1C5] hover:bg-gray-50 transition-all cursor-pointer group"
        :class="{'opacity-60 cursor-not-allowed': !isConnected}"
        @click="isConnected && handleRewrite()"
      >
        <div class="flex items-center justify-between">
          <h3 class="font-medium text-[#1A365D] group-hover:text-[#4FD1C5] transition-colors text-sm">改写内容</h3>
          <svg class="w-3.5 h-3.5 text-gray-400 group-hover:text-[#4FD1C5] transition-colors" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
        </div>
        <p class="text-xs text-gray-600 mt-0.5">优化选中的文本段落</p>
        <div class="mt-0.5 text-xs text-gray-500">选中文本后使用</div>
      </div>
      
      <!-- 扩写内容 -->
      <div 
        class="p-2 border border-gray-200 rounded-md hover:border-[#4FD1C5] hover:bg-gray-50 transition-all cursor-pointer group"
        :class="{'opacity-60 cursor-not-allowed': !isConnected}"
        @click="isConnected && handleExpand()"
      >
        <div class="flex items-center justify-between">
          <h3 class="font-medium text-[#1A365D] group-hover:text-[#4FD1C5] transition-colors text-sm">扩写内容</h3>
          <svg class="w-3.5 h-3.5 text-gray-400 group-hover:text-[#4FD1C5] transition-colors" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="7" y1="12" x2="21" y2="12"></line>
            <line x1="14" y1="5" x2="14" y2="19"></line>
            <line x1="3" y1="12" x2="3" y2="12"></line>
          </svg>
        </div>
        <p class="text-xs text-gray-600 mt-0.5">扩展选中的文本内容</p>
        <div class="mt-0.5 text-xs text-gray-500">选中文本后使用</div>
      </div>
      
      <!-- 简化内容 -->
      <div 
        class="p-2 border border-gray-200 rounded-md hover:border-[#4FD1C5] hover:bg-gray-50 transition-all cursor-pointer group"
        :class="{'opacity-60 cursor-not-allowed': !isConnected}"
        @click="isConnected && handleSimplify()"
      >
        <div class="flex items-center justify-between">
          <h3 class="font-medium text-[#1A365D] group-hover:text-[#4FD1C5] transition-colors text-sm">简化内容</h3>
          <svg class="w-3.5 h-3.5 text-gray-400 group-hover:text-[#4FD1C5] transition-colors" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </div>
        <p class="text-xs text-gray-600 mt-0.5">简化选中的文本内容</p>
        <div class="mt-0.5 text-xs text-gray-500">选中文本后使用</div>
      </div>
      
      <!-- AI 状态信息 -->
      <div class="mt-4 bg-gray-50 p-2 rounded-md">
        <div class="flex items-center justify-between mb-1">
          <span class="text-xs font-medium text-gray-700">AI 状态</span>
          <span 
            :class="[
              'text-xs px-1.5 py-0.5 rounded-full flex items-center', 
              isConnected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            ]"
          >
            <span 
              class="w-1.5 h-1.5 mr-1 rounded-full"
              :class="isConnected ? 'bg-green-500' : 'bg-red-500'"
            ></span>
            {{ isConnected ? '已连接' : '未连接' }}
          </span>
        </div>
        
        <div class="text-xs text-gray-500">
          <div class="flex items-center justify-between">
            <span>当前状态:</span>
            <span 
              :class="{
                'text-yellow-600': aiStatus === 'processing',
                'text-green-600': aiStatus === 'idle',
                'text-gray-600': aiStatus !== 'processing' && aiStatus !== 'idle'
              }"
            >
              {{ aiStatus === 'idle' ? '就绪' : aiStatus === 'processing' ? '处理中' : aiStatus }}
            </span>
          </div>
        </div>
      </div>
      
      <!-- 快捷键提示 -->
      <div class="mt-2 text-xs text-gray-500 p-1.5 border-t border-gray-200">
        <div class="flex justify-between mb-1">
          <span class="font-medium">Tab</span>
          <span>接受建议</span>
        </div>
        <div class="flex justify-between">
          <span class="font-medium">Esc</span>
          <span>拒绝建议</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  isConnected: {
    type: Boolean,
    default: false
  },
  aiStatus: {
    type: String,
    default: 'idle'
  },
  contextWindowBefore: {
    type: Number,
    default: 1536
  },
  contextWindowAfter: {
    type: Number,
    default: 256
  }
})

const emit = defineEmits([
  'auto-complete',
  'rewrite',
  'expand',
  'simplify'
])

const handleAutoComplete = () => {
  emit('auto-complete')
}

const handleRewrite = () => {
  emit('rewrite')
}

const handleExpand = () => {
  emit('expand')
}

const handleSimplify = () => {
  emit('simplify')
}
</script>