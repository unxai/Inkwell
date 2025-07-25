<template>
  <div class="container mx-auto px-4 py-6">
    <div class="flex flex-col lg:flex-row gap-6">
      <!-- 主编辑区域 -->
      <div class="flex-grow">
        <div class="bg-white rounded-lg shadow-md overflow-hidden">
          <TextEditor 
            ref="editorRef"
            :initial-content="editorContent"
            @update:content="handleContentUpdate"
            @accept-completion="handleAcceptCompletion"
            @reject-completion="handleRejectCompletion"
          />
        </div>
        
        <!-- 字数统计和工具栏 -->
        <div class="mt-4 flex flex-wrap justify-between items-center">
          <div class="text-sm text-gray-600">
            {{ wordCount }} 字 | {{ charCount }} 字符 | 编辑时间: {{ formatTime(editingTime) }}
          </div>
          
          <div class="flex space-x-2 mt-2 sm:mt-0">
            <button 
              @click="toggleAiPanel"
              class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors"
              :class="showAiPanel ? 'bg-[#1A365D] text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
            >
              {{ showAiPanel ? '隐藏AI面板' : '显示AI面板' }}
            </button>
            
            <button 
              @click="saveDocument"
              class="px-3 py-1.5 bg-[#4FD1C5] text-white rounded-md text-sm font-medium hover:bg-[#3ABAB4] transition-colors"
            >
              保存文档
            </button>
          </div>
        </div>
      </div>
      
      <!-- 侧边AI辅助面板 -->
      <div 
        v-show="showAiPanel"
        class="lg:w-80 xl:w-96 flex-shrink-0 transition-all duration-300"
      >
        <div class="bg-white rounded-lg shadow-md h-full">
          <div class="p-4 border-b border-gray-200">
            <h2 class="text-lg font-medium text-[#1A365D]">AI 辅助工具</h2>
          </div>
          
          <div class="p-4">
            <!-- 标签页切换 -->
            <div class="flex border-b border-gray-200 mb-4">
              <button 
                v-for="tab in tabs" 
                :key="tab.id"
                @click="activeTab = tab.id"
                class="py-2 px-4 text-sm font-medium transition-colors border-b-2 -mb-px"
                :class="activeTab === tab.id ? 'border-[#4FD1C5] text-[#1A365D]' : 'border-transparent text-gray-500 hover:text-gray-700'"
              >
                {{ tab.name }}
              </button>
            </div>
            
            <!-- 文本优化面板 -->
            <div v-if="activeTab === 'optimize'">
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">选择优化类型</label>
                <div class="flex flex-wrap gap-2">
                  <button 
                    v-for="action in optimizeActions" 
                    :key="action.id"
                    @click="selectedOptimizeAction = action.id"
                    class="px-3 py-1.5 rounded-md text-sm transition-colors"
                    :class="selectedOptimizeAction === action.id ? 'bg-[#1A365D] text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
                  >
                    {{ action.name }}
                  </button>
                </div>
              </div>
              
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">选择文本范围</label>
                <div class="flex items-center">
                  <button 
                    @click="textScope = 'selection'"
                    class="px-3 py-1.5 rounded-l-md text-sm transition-colors"
                    :class="textScope === 'selection' ? 'bg-[#1A365D] text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
                  >
                    选中文本
                  </button>
                  <button 
                    @click="textScope = 'all'"
                    class="px-3 py-1.5 rounded-r-md text-sm transition-colors"
                    :class="textScope === 'all' ? 'bg-[#1A365D] text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
                  >
                    全文
                  </button>
                </div>
              </div>
              
              <button 
                @click="optimizeText"
                class="w-full py-2 bg-[#4FD1C5] text-white rounded-md text-sm font-medium hover:bg-[#3ABAB4] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="isProcessing || (!hasSelection && textScope === 'selection')"
              >
                {{ isProcessing ? '处理中...' : '开始优化' }}
              </button>
            </div>
            
            <!-- 风格调整面板 -->
            <div v-if="activeTab === 'style'">
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">目标风格</label>
                <select 
                  v-model="styleOptions.targetStyle"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-[#4FD1C5] focus:border-[#4FD1C5]"
                >
                  <option v-for="style in stylesList" :key="style.id" :value="style.id">{{ style.name }}</option>
                </select>
              </div>
              
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">语气</label>
                <select 
                  v-model="styleOptions.tone"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-[#4FD1C5] focus:border-[#4FD1C5]"
                >
                  <option value="">不指定</option>
                  <option v-for="tone in tonesList" :key="tone.id" :value="tone.id">{{ tone.name }}</option>
                </select>
              </div>
              
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">正式程度</label>
                <select 
                  v-model="styleOptions.formality"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-[#4FD1C5] focus:border-[#4FD1C5]"
                >
                  <option value="">不指定</option>
                  <option v-for="formality in formalityLevels" :key="formality.id" :value="formality.id">{{ formality.name }}</option>
                </select>
              </div>
              
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">选择文本范围</label>
                <div class="flex items-center">
                  <button 
                    @click="textScope = 'selection'"
                    class="px-3 py-1.5 rounded-l-md text-sm transition-colors"
                    :class="textScope === 'selection' ? 'bg-[#1A365D] text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
                  >
                    选中文本
                  </button>
                  <button 
                    @click="textScope = 'all'"
                    class="px-3 py-1.5 rounded-r-md text-sm transition-colors"
                    :class="textScope === 'all' ? 'bg-[#1A365D] text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
                  >
                    全文
                  </button>
                </div>
              </div>
              
              <button 
                @click="adjustStyle"
                class="w-full py-2 bg-[#4FD1C5] text-white rounded-md text-sm font-medium hover:bg-[#3ABAB4] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="isProcessing || (!hasSelection && textScope === 'selection')"
              >
                {{ isProcessing ? '处理中...' : '调整风格' }}
              </button>
            </div>
            
            <!-- 大纲生成面板 -->
            <div v-if="activeTab === 'outline'">
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">大纲类型</label>
                <select 
                  v-model="outlineType"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-[#4FD1C5] focus:border-[#4FD1C5]"
                >
                  <option value="article">文章大纲</option>
                  <option value="essay">论文大纲</option>
                  <option value="report">报告大纲</option>
                </select>
              </div>
              
              <div class="mb-4">
                <label class="block text-sm font-medium text-gray-700 mb-1">主题</label>
                <input 
                  v-model="outlineSubject"
                  type="text"
                  placeholder="输入文章主题"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-[#4FD1C5] focus:border-[#4FD1C5]"
                />
              </div>
              
              <button 
                @click="generateOutline"
                class="w-full py-2 bg-[#4FD1C5] text-white rounded-md text-sm font-medium hover:bg-[#3ABAB4] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                :disabled="isProcessing || !outlineSubject"
              >
                {{ isProcessing ? '生成中...' : '生成大纲' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import TextEditor from '../components/editor/TextEditor.vue';
import { useEditorStore } from '../store/modules/editor';
import { useCompletion } from '../composables/useCompletion';
import api from '../services/api';

const editorStore = useEditorStore();
const editorRef = ref(null);
const editorContent = ref('');
const showAiPanel = ref(true);
const activeTab = ref('optimize');
const isProcessing = ref(false);
const editingTime = ref(0);
const editingTimer = ref(null);
const textScope = ref('selection');
const hasSelection = ref(false);

// 文本优化选项
const selectedOptimizeAction = ref('rewrite');
const optimizeActions = [
  { id: 'rewrite', name: '改写' },
  { id: 'expand', name: '扩写' },
  { id: 'simplify', name: '简化' }
];

// 风格调整选项
const styleOptions = ref({
  targetStyle: 'academic',
  tone: '',
  formality: ''
});

const stylesList = [
  { id: 'academic', name: '学术' },
  { id: 'business', name: '商务' },
  { id: 'creative', name: '创意' },
  { id: 'technical', name: '技术' },
  { id: 'casual', name: '随意' },
  { id: 'news', name: '新闻' }
];

const tonesList = [
  { id: 'formal', name: '正式' },
  { id: 'friendly', name: '友好' },
  { id: 'authoritative', name: '权威' },
  { id: 'enthusiastic', name: '热情' },
  { id: 'neutral', name: '中立' }
];

const formalityLevels = [
  { id: 'very_formal', name: '非常正式' },
  { id: 'formal', name: '正式' },
  { id: 'neutral', name: '中性' },
  { id: 'casual', name: '随意' },
  { id: 'very_casual', name: '非常随意' }
];

// 大纲生成选项
const outlineType = ref('article');
const outlineSubject = ref('');

// 标签页配置
const tabs = [
  { id: 'optimize', name: '文本优化' },
  { id: 'style', name: '风格调整' },
  { id: 'outline', name: '大纲生成' }
];

// 使用自动完成组合式函数
const { requestCompletion } = useCompletion();

// 计算字数和字符数
const wordCount = computed(() => {
  const text = editorContent.value.replace(/<[^>]*>/g, '');
  return text.trim().split(/\s+/).filter(Boolean).length;
});

const charCount = computed(() => {
  const text = editorContent.value.replace(/<[^>]*>/g, '');
  return text.length;
});

// 格式化时间
const formatTime = (seconds) => {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;
  
  return [
    hours.toString().padStart(2, '0'),
    minutes.toString().padStart(2, '0'),
    secs.toString().padStart(2, '0')
  ].join(':');
};

// 处理内容更新
const handleContentUpdate = (content) => {
  editorContent.value = content;
  
  // 检查是否有选中的文本
  if (editorRef.value && editorRef.value.editor) {
    const { editor } = editorRef.value;
    hasSelection.value = !editor.state.selection.empty;
  }
};

// 处理接受补全
const handleAcceptCompletion = () => {
  console.log('接受补全');
};

// 处理拒绝补全
const handleRejectCompletion = () => {
  console.log('拒绝补全');
};

// 切换AI面板显示
const toggleAiPanel = () => {
  showAiPanel.value = !showAiPanel.value;
};

// 保存文档
const saveDocument = () => {
  try {
    const content = editorContent.value;
    const title = '未命名文档';
    const date = new Date().toISOString();
    
    // 创建一个Blob对象
    const blob = new Blob([content], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    
    // 创建一个下载链接
    const a = document.createElement('a');
    a.href = url;
    a.download = `${title}-${date.split('T')[0]}.html`;
    document.body.appendChild(a);
    a.click();
    
    // 清理
    URL.revokeObjectURL(url);
    document.body.removeChild(a);
    
    // 显示成功消息
    window.$message?.success?.('文档已保存');
  } catch (error) {
    console.error('保存文档失败:', error);
    window.$message?.error?.('保存文档失败');
  }
};

// 优化文本
const optimizeText = async () => {
  try {
    isProcessing.value = true;
    
    let text = '';
    if (textScope.value === 'selection') {
      // 获取选中的文本
      if (editorRef.value && editorRef.value.editor) {
        const { editor } = editorRef.value;
        text = editor.state.selection.content().content.textBetween(0, editor.state.selection.content().content.size, ' ');
        if (!text) {
          window.$message?.error?.('请先选择要优化的文本');
          isProcessing.value = false;
          return;
        }
      } else {
        window.$message?.error?.('编辑器未初始化');
        isProcessing.value = false;
        return;
      }
    } else {
      // 获取全文
      if (editorRef.value && editorRef.value.editor) {
        text = editorRef.value.editor.getText();
      } else {
        text = editorContent.value.replace(/<[^>]*>/g, '');
      }
    }
    
    // 调用API - 使用editorStore中的方法
    const result = await editorStore.optimizeText(text, selectedOptimizeAction.value);
    
    // 更新编辑器内容
    if (textScope.value === 'selection' && editorRef.value && editorRef.value.editor) {
      editorRef.value.editor.chain().focus().deleteSelection().insertContent(result).run();
    } else if (editorRef.value && editorRef.value.editor) {
      editorRef.value.editor.commands.setContent(result);
    }
    
    window.$message?.success?.('文本优化完成');
  } catch (error) {
    console.error('文本优化失败:', error);
    window.$message?.error?.('文本优化失败: ' + (error.response?.data?.detail || '请稍后重试'));
  } finally {
    isProcessing.value = false;
  }
};

// 调整风格
const adjustStyle = async () => {
  try {
    isProcessing.value = true;
    
    let text = '';
    if (textScope.value === 'selection') {
      // 获取选中的文本
      if (editorRef.value && editorRef.value.editor) {
        const { editor } = editorRef.value;
        text = editor.state.selection.content().content.textBetween(0, editor.state.selection.content().content.size, ' ');
        if (!text) {
          window.$message?.error?.('请先选择要调整风格的文本');
          isProcessing.value = false;
          return;
        }
      } else {
        window.$message?.error?.('编辑器未初始化');
        isProcessing.value = false;
        return;
      }
    } else {
      // 获取全文
      if (editorRef.value && editorRef.value.editor) {
        text = editorRef.value.editor.getText();
      } else {
        text = editorContent.value.replace(/<[^>]*>/g, '');
      }
    }
    
    // 调用API
    const response = await api.post('/api/v1/style/adjust', {
      text,
      target_style: styleOptions.value.targetStyle,
      tone: styleOptions.value.tone || undefined,
      formality: styleOptions.value.formality || undefined
    });
    
    const result = response.data.result || response.data.completion;
    
    // 更新编辑器内容
    if (textScope.value === 'selection' && editorRef.value && editorRef.value.editor) {
      editorRef.value.editor.chain().focus().deleteSelection().insertContent(result).run();
    } else if (editorRef.value && editorRef.value.editor) {
      editorRef.value.editor.commands.setContent(result);
    }
    
    window.$message?.success?.('风格调整完成');
  } catch (error) {
    console.error('风格调整失败:', error);
    window.$message?.error?.('风格调整失败: ' + (error.response?.data?.detail || '请稍后重试'));
  } finally {
    isProcessing.value = false;
  }
};

// 生成大纲
const generateOutline = async () => {
  try {
    isProcessing.value = true;
    
    // 调用API
    const response = await api.post('/api/v1/academic/outline', {
      type: outlineType.value,
      subject: outlineSubject.value
    });
    
    // 将大纲插入到编辑器中
    if (editorRef.value && editorRef.value.editor) {
      editorRef.value.editor.chain().focus().insertContent(response.outline).run();
    } else {
      window.$message?.error?.('编辑器未初始化');
      isProcessing.value = false;
      return;
    }
    
    window.$message?.success?.('大纲生成完成');
  } catch (error) {
    console.error('大纲生成失败:', error);
    window.$message?.error?.('大纲生成失败: ' + (error.response?.data?.detail || '请稍后重试'));
  } finally {
    isProcessing.value = false;
  }
};

// 启动编辑时间计时器
const startEditingTimer = () => {
  editingTimer.value = setInterval(() => {
    editingTime.value++;
  }, 1000);
};

onMounted(() => {
  // 启动编辑时间计时器
  startEditingTimer();
  
  // 初始化选择状态
  if (editorRef.value) {
    hasSelection.value = editorRef.value.hasSelection?.() || false;
  }
});

onBeforeUnmount(() => {
  // 清除计时器
  if (editingTimer.value) {
    clearInterval(editingTimer.value);
  }
});
</script>

<style scoped>
/* 添加过渡效果 */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}
</style>