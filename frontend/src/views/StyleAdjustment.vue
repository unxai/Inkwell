<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-[#1A365D] mb-6">写作风格调整</h1>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- 左侧：原文输入区 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold text-[#1A365D] mb-4">原文</h2>
        <textarea
          v-model="originalText"
          class="w-full h-64 p-4 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#4FD1C5] focus:border-transparent"
          placeholder="请输入需要调整风格的文本..."
        ></textarea>
      </div>
      
      <!-- 右侧：风格调整后的文本 -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold text-[#1A365D] mb-4">调整后的文本</h2>
        <div 
          v-if="adjustedText" 
          class="w-full h-64 p-4 border border-gray-300 rounded-md overflow-auto"
        >
          {{ adjustedText }}
        </div>
        <div 
          v-else 
          class="w-full h-64 p-4 border border-gray-300 rounded-md flex items-center justify-center text-gray-500"
        >
          <span v-if="isLoading">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-[#4FD1C5]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            正在调整文本风格...
          </span>
          <span v-else>调整后的文本将显示在这里</span>
        </div>
      </div>
    </div>
    
    <!-- 风格选项 -->
    <div class="mt-8 bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-semibold text-[#1A365D] mb-4">风格选项</h2>
      
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <!-- 目标风格 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">目标风格</label>
          <select 
            v-model="targetStyle" 
            class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#4FD1C5] focus:border-transparent"
          >
            <option v-for="style in styleOptions.styles" :key="style" :value="style">{{ style }}</option>
          </select>
        </div>
        
        <!-- 语气 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">语气</label>
          <select 
            v-model="tone" 
            class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#4FD1C5] focus:border-transparent"
          >
            <option value="">不指定</option>
            <option v-for="t in styleOptions.tones" :key="t" :value="t">{{ t }}</option>
          </select>
        </div>
        
        <!-- 正式程度 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">正式程度</label>
          <select 
            v-model="formality" 
            class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#4FD1C5] focus:border-transparent"
          >
            <option value="">不指定</option>
            <option v-for="f in styleOptions.formality_levels" :key="f" :value="f">{{ f }}</option>
          </select>
        </div>
        
        <!-- 目标受众 -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">目标受众</label>
          <select 
            v-model="audience" 
            class="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#4FD1C5] focus:border-transparent"
          >
            <option value="">不指定</option>
            <option v-for="a in styleOptions.audiences" :key="a" :value="a">{{ a }}</option>
          </select>
        </div>
      </div>
      
      <!-- 调整按钮 -->
      <div class="mt-6 flex justify-center">
        <button 
          @click="adjustStyle" 
          class="px-6 py-3 bg-[#1A365D] text-white rounded-md hover:bg-[#2D4A7A] focus:outline-none focus:ring-2 focus:ring-[#4FD1C5] focus:ring-offset-2 disabled:opacity-50"
          :disabled="!originalText || !targetStyle || isLoading"
        >
          调整风格
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// 文本内容
const originalText = ref('');
const adjustedText = ref('');
const isLoading = ref(false);

// 风格选项
const targetStyle = ref('学术');
const tone = ref('');
const formality = ref('');
const audience = ref('');

// 可用的风格选项
const styleOptions = ref({
  styles: ['学术', '商务', '新闻', '文学', '科普', '技术', '幽默', '叙事', '说明', '议论', '抒情'],
  tones: ['正式', '专业', '友好', '热情', '权威', '中立', '幽默', '严肃', '温暖', '冷静', '激励'],
  formality_levels: ['非常正式', '正式', '中等正式', '随意', '非常随意'],
  audiences: ['专业人士', '学生', '普通读者', '儿童', '青少年', '老年人', '企业高管', '技术人员', '学者']
});

// 获取可用的风格选项
onMounted(async () => {
  try {
    const response = await axios.get('/api/v1/style/styles');
    styleOptions.value = response.data;
  } catch (error) {
    console.error('获取风格选项失败:', error);
  }
});

// 调整文本风格
const adjustStyle = async () => {
  if (!originalText.value || !targetStyle.value) return;
  
  isLoading.value = true;
  adjustedText.value = '';
  
  try {
    const response = await axios.post('/api/v1/style/adjust', {
      text: originalText.value,
      target_style: targetStyle.value,
      tone: tone.value || undefined,
      formality: formality.value || undefined,
      audience: audience.value || undefined
    });
    
    adjustedText.value = response.data.styled_text;
  } catch (error) {
    console.error('调整文本风格失败:', error);
    alert('调整文本风格失败，请稍后重试');
  } finally {
    isLoading.value = false;
  }
};
</script>