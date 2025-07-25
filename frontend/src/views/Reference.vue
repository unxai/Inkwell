<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold mb-6">引用管理系统</h1>
    
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <!-- 引用格式选择器 -->
      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">引用格式</label>
        <div class="flex flex-wrap gap-2">
          <button 
            v-for="style in citationStyles" 
            :key="style.value"
            @click="selectedStyle = style.value"
            :class="[
              'px-3 py-1.5 rounded-md text-sm font-medium transition-colors',
              selectedStyle === style.value 
                ? 'bg-inkwell-blue text-white' 
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            ]"
          >
            {{ style.label }}
          </button>
        </div>
      </div>
      
      <!-- 添加新引用表单 -->
      <div class="border-t border-gray-200 pt-6 mb-6">
        <h2 class="text-lg font-bold mb-4">添加新引用</h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">作者</label>
            <input 
              type="text" 
              v-model="newReference.author" 
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-inkwell-teal focus:border-transparent"
              placeholder="作者姓名"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">标题</label>
            <input 
              type="text" 
              v-model="newReference.title" 
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-inkwell-teal focus:border-transparent"
              placeholder="作品标题"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">出版商/期刊</label>
            <input 
              type="text" 
              v-model="newReference.publisher" 
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-inkwell-teal focus:border-transparent"
              placeholder="出版商或期刊名称"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">出版年份</label>
            <input 
              type="text" 
              v-model="newReference.year" 
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-inkwell-teal focus:border-transparent"
              placeholder="出版年份"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">URL链接（可选）</label>
            <input 
              type="text" 
              v-model="newReference.url" 
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-inkwell-teal focus:border-transparent"
              placeholder="https://example.com"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">DOI标识符（可选）</label>
            <input 
              type="text" 
              v-model="newReference.doi" 
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-inkwell-teal focus:border-transparent"
              placeholder="10.xxxx/xxxxx"
            />
          </div>
        </div>
        
        <div class="mt-4 flex justify-end">
          <button 
            @click="addReference" 
            class="btn btn-primary"
            :disabled="!canAddReference"
          >
            添加引用
          </button>
        </div>
      </div>
      
      <!-- 引用列表 -->
      <div class="border-t border-gray-200 pt-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-bold">引用列表</h2>
          <div class="flex gap-2">
            <button class="btn btn-outline text-sm">导入引用</button>
            <button class="btn btn-outline text-sm">导出引用</button>
          </div>
        </div>
        
        <div v-if="references.length === 0" class="text-center py-8 text-gray-500">
          暂无引用，请添加新引用
        </div>
        
        <div v-else class="space-y-4">
          <div 
            v-for="(reference, index) in references" 
            :key="index"
            class="p-4 border border-gray-200 rounded-md hover:border-inkwell-teal transition-colors"
          >
            <div class="flex justify-between">
              <h3 class="font-medium">{{ reference.title }}</h3>
              <div class="flex gap-2">
                <button class="text-sm text-gray-500 hover:text-inkwell-teal">编辑</button>
                <button class="text-sm text-gray-500 hover:text-red-500" @click="removeReference(index)">删除</button>
              </div>
            </div>
            
            <p class="text-sm text-gray-600 mt-1">{{ reference.author }} ({{ reference.year }})</p>
            
            <div class="mt-3 p-3 bg-gray-50 rounded text-sm">
              <p>{{ formatCitation(reference) }}</p>
            </div>
            
            <div class="mt-2 flex justify-end">
              <button class="text-sm text-inkwell-teal hover:underline">复制引用</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import axios from 'axios'

// 引用样式
const citationStyles = [
  { label: 'APA', value: 'apa' },
  { label: 'MLA', value: 'mla' },
  { label: 'IEEE', value: 'ieee' },
  { label: '哈佛', value: 'harvard' }
]

// 状态
const selectedStyle = ref('apa')
const references = ref([])
const newReference = ref({
  author: '',
  title: '',
  publisher: '',
  year: '',
  url: '',
  doi: ''
})

// 计算属性
const canAddReference = computed(() => {
  return newReference.value.author && 
         newReference.value.title && 
         newReference.value.publisher && 
         newReference.value.year
})

// 方法
const addReference = async () => {
  if (!canAddReference.value) {
    return
  }
  
  try {
    // 调用后端API格式化引用
    const response = await axios.post('/api/v1/reference/format', {
      ...newReference.value,
      style: selectedStyle.value
    })
    
    // 添加到引用列表
    references.value.push({
      ...newReference.value,
      formattedCitation: response.data.formatted_citation
    })
    
    // 清空表单
    newReference.value = {
      author: '',
      title: '',
      publisher: '',
      year: '',
      url: '',
      doi: ''
    }
  } catch (error) {
    console.error('添加引用失败:', error)
    alert('添加引用失败，请稍后重试')
    
    // 模拟数据（实际项目中应删除）
    references.value.push({
      ...newReference.value,
      formattedCitation: formatCitation(newReference.value)
    })
    
    // 清空表单
    newReference.value = {
      author: '',
      title: '',
      publisher: '',
      year: '',
      url: '',
      doi: ''
    }
  }
}

const removeReference = (index) => {
  references.value.splice(index, 1)
}

const formatCitation = (reference) => {
  // 根据选择的引用样式格式化引用
  switch (selectedStyle.value) {
    case 'apa':
      return `${reference.author}. (${reference.year}). ${reference.title}. ${reference.publisher}.`
    case 'mla':
      return `${reference.author}. "${reference.title}." ${reference.publisher}, ${reference.year}.`
    case 'ieee':
      return `[1] ${reference.author}, "${reference.title}," ${reference.publisher}, ${reference.year}.`
    case 'harvard':
      return `${reference.author} (${reference.year}) ${reference.title}. ${reference.publisher}.`
    default:
      return `${reference.author} (${reference.year}). ${reference.title}. ${reference.publisher}.`
  }
}
</script>