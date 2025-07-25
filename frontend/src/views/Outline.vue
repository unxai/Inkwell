<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold mb-6">文章大纲生成</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- 左侧输入区 -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 class="text-lg font-bold mb-4">输入信息</h2>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">文章主题</label>
            <input 
              type="text" 
              v-model="topic" 
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-inkwell-teal focus:border-transparent"
              placeholder="请输入文章主题"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">关键词（用逗号分隔）</label>
            <input 
              type="text" 
              v-model="keywordsInput" 
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-inkwell-teal focus:border-transparent"
              placeholder="关键词1, 关键词2, 关键词3..."
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">大纲深度</label>
            <select 
              v-model="depth" 
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-inkwell-teal focus:border-transparent"
            >
              <option value="1">1级（仅主标题）</option>
              <option value="2">2级（主标题 + 子标题）</option>
              <option value="3">3级（主标题 + 子标题 + 小标题）</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">大纲风格</label>
            <select 
              v-model="style" 
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-inkwell-teal focus:border-transparent"
            >
              <option value="academic">学术论文</option>
              <option value="blog">博客文章</option>
              <option value="report">工作报告</option>
              <option value="creative">创意写作</option>
            </select>
          </div>
          
          <button 
            @click="generateOutline" 
            class="w-full btn btn-primary"
            :disabled="isGenerating"
          >
            {{ isGenerating ? '生成中...' : '生成大纲' }}
          </button>
        </div>
      </div>
      
      <!-- 右侧预览区 -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <h2 class="text-lg font-bold mb-4">大纲预览</h2>
        
        <div v-if="isGenerating" class="flex justify-center items-center h-64">
          <div class="text-center">
            <div class="inline-block animate-spin rounded-full h-8 w-8 border-4 border-inkwell-teal border-t-transparent"></div>
            <p class="mt-2 text-gray-600">正在生成大纲...</p>
          </div>
        </div>
        
        <div v-else-if="outline.length === 0" class="flex justify-center items-center h-64">
          <p class="text-gray-500">请输入文章主题并点击"生成大纲"按钮</p>
        </div>
        
        <div v-else class="outline-container">
          <ul class="outline-list">
            <li v-for="(item, index) in outline" :key="index" class="outline-item">
              <div class="flex items-center">
                <span class="font-medium">{{ item.title }}</span>
                <button class="ml-2 text-xs text-gray-500 hover:text-inkwell-teal">编辑</button>
              </div>
              
              <ul v-if="item.children && item.children.length > 0" class="pl-6 mt-2">
                <li v-for="(child, childIndex) in item.children" :key="`${index}-${childIndex}`" class="mt-2">
                  <div class="flex items-center">
                    <span>{{ child.title }}</span>
                    <button class="ml-2 text-xs text-gray-500 hover:text-inkwell-teal">编辑</button>
                  </div>
                  
                  <ul v-if="child.children && child.children.length > 0" class="pl-6 mt-2">
                    <li v-for="(grandChild, grandChildIndex) in child.children" :key="`${index}-${childIndex}-${grandChildIndex}`" class="mt-2">
                      <div class="flex items-center">
                        <span class="text-sm">{{ grandChild.title }}</span>
                        <button class="ml-2 text-xs text-gray-500 hover:text-inkwell-teal">编辑</button>
                      </div>
                    </li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>
          
          <div class="mt-6 flex justify-between">
            <button class="btn btn-outline">导出大纲</button>
            <button class="btn btn-secondary">创建文档</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

// 状态
const topic = ref('')
const keywordsInput = ref('')
const depth = ref('2')
const style = ref('blog')
const isGenerating = ref(false)
const outline = ref([])

// 计算属性
const keywords = computed(() => {
  return keywordsInput.value.split(',')
    .map(keyword => keyword.trim())
    .filter(keyword => keyword !== '')
})

// 方法
const generateOutline = async () => {
  if (!topic.value) {
    alert('请输入文章主题')
    return
  }
  
  isGenerating.value = true
  
  try {
    // 调用后端API生成大纲
    const response = await axios.post('/api/v1/document/outline', {
      topic: topic.value,
      keywords: keywords.value,
      depth: parseInt(depth.value),
      style: style.value
    })
    
    outline.value = response.data.outline
  } catch (error) {
    console.error('生成大纲失败:', error)
    alert('生成大纲失败，请稍后重试')
    
    // 模拟数据（实际项目中应删除）
    outline.value = [
      {
        title: '引言',
        children: [
          { title: '研究背景', children: [] },
          { title: '研究意义', children: [] }
        ]
      },
      {
        title: '文献综述',
        children: [
          { title: '相关理论基础', children: [] },
          { title: '研究现状', children: [] }
        ]
      },
      {
        title: '研究方法',
        children: []
      },
      {
        title: '结论',
        children: []
      }
    ]
  } finally {
    isGenerating.value = false
  }
}
</script>

<style scoped>
.outline-list {
  list-style-type: none;
  padding: 0;
}

.outline-item {
  margin-bottom: 1rem;
}

.outline-item > div {
  font-weight: 600;
}
</style>