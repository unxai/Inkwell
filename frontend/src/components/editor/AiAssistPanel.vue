<template>
  <div class="ai-assist-panel">
    <h2 class="text-lg font-bold mb-4 text-[#1A365D] flex items-center">
      <svg class="w-5 h-5 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <path d="M12 16v-4"></path>
        <path d="M12 8h.01"></path>
      </svg>
      AI 辅助功能
    </h2>
    
    <div class="space-y-3">
      <!-- 自动完成 -->
      <div 
        class="p-3 border border-gray-200 rounded-md hover:border-[#4FD1C5] hover:bg-gray-50 transition-all cursor-pointer group"
        :class="{'opacity-60 cursor-not-allowed': !isConnected}"
        @click="isConnected && handleAutoComplete()"
      >
        <div class="flex items-center justify-between">
          <h3 class="font-medium text-[#1A365D] group-hover:text-[#4FD1C5] transition-colors">自动完成</h3>
          <svg class="w-4 h-4 text-gray-400 group-hover:text-[#4FD1C5] transition-colors" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </div>
        <p class="text-sm text-gray-600 mt-1">实时生成文本建议</p>
      </div>
      
      <!-- 改写内容 -->
      <div 
        class="p-3 border border-gray-200 rounded-md hover:border-[#4FD1C5] hover:bg-gray-50 transition-all cursor-pointer group"
        :class="{'opacity-60 cursor-not-allowed': !isConnected}"
        @click="isConnected && handleRewrite()"
      >
        <div class="flex items-center justify-between">
          <h3 class="font-medium text-[#1A365D] group-hover:text-[#4FD1C5] transition-colors">改写内容</h3>
          <svg class="w-4 h-4 text-gray-400 group-hover:text-[#4FD1C5] transition-colors" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
        </div>
        <p class="text-sm text-gray-600 mt-1">优化选中的文本段落</p>
        <div class="mt-1 text-xs text-gray-500">选中文本后使用</div>
      </div>
      
      <!-- 扩写内容 -->
      <div 
        class="p-3 border border-gray-200 rounded-md hover:border-[#4FD1C5] hover:bg-gray-50 transition-all cursor-pointer group"
        :class="{'opacity-60 cursor-not-allowed': !isConnected}"
        @click="isConnected && handleExpand()"
      >
        <div class="flex items-center justify-between">
          <h3 class="font-medium text-[#1A365D] group-hover:text-[#4FD1C5] transition-colors">扩写内容</h3>
          <svg class="w-4 h-4 text-gray-400 group-hover:text-[#4FD1C5] transition-colors" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="7" y1="12" x2="21" y2="12"></line>
            <line x1="14" y1="5" x2="14" y2="19"></line>
            <line x1="3" y1="12" x2="3" y2="12"></line>
          </svg>
        </div>
        <p class="text-sm text-gray-600 mt-1">扩展选中的文本内容</p>
        <div class="mt-1 text-xs text-gray-500">选中文本后使用</div>
      </div>
      
      <!-- 简化内容 -->
      <div 
        class="p-3 border border-gray-200 rounded-md hover:border-[#4FD1C5] hover:bg-gray-50 transition-all cursor-pointer group"
        :class="{'opacity-60 cursor-not-allowed': !isConnected}"
        @click="isConnected && handleSimplify()"
      >
        <div class="flex items-center justify-between">
          <h3 class="font-medium text-[#1A365D] group-hover:text-[#4FD1C5] transition-colors">简化内容</h3>
          <svg class="w-4 h-4 text-gray-400 group-hover:text-[#4FD1C5] transition-colors" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
        </div>
        <p class="text-sm text-gray-600 mt-1">简化选中的文本内容</p>
        <div class="mt-1 text-xs text-gray-500">选中文本后使用</div>
      </div>
      
      <!-- AI 状态信息 -->
      <div class="mt-6 bg-gray-50 p-3 rounded-md">
        <div class="flex items-center justify-between mb-2">
          <span class="text-sm font-medium text-gray-700">AI 状态</span>
          <span 
            :class="[
              'text-xs px-2 py-0.5 rounded-full flex items-center', 
              isConnected ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            ]"
          >
            <span 
              class="w-2 h-2 mr-1 rounded-full"
              :class="isConnected ? 'bg-green-500' : 'bg-red-500'"
            ></span>
            {{ isConnected ? '已连接' : '未连接' }}
          </span>
        </div>
        
        <div class="text-xs text-gray-500 space-y-1">
          <div class="flex items-center justify-between">
            <span>上下文窗口:</span>
            <span>{{ contextWindowBefore }} / {{ contextWindowAfter }} tokens</span>
          </div>
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
      <div class="mt-2 text-xs text-gray-500 p-2 border-t border-gray-200">
        <div class="font-medium mb-1">快捷键:</div>
        <div class="flex justify-between">
          <span>Tab</span>
          <span>接受建议</span>
        </div>
        <div class="flex justify-between">
          <span>Esc</span>
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