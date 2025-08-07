<template>
  <div class="templates-panel h-full flex flex-col bg-white">
    <!-- Header -->
    <div class="flex items-center justify-between p-4 border-b border-gray-200 bg-gradient-to-r from-purple-50 to-pink-50">
      <div class="flex items-center space-x-2">
        <div class="w-3 h-3 rounded-full bg-purple-500"></div>
        <h3 class="text-lg font-semibold text-gray-800">文档模板</h3>
      </div>
      <button
        @click="$emit('toggle-panel')"
        class="p-1 text-gray-400 hover:text-gray-600 transition-colors"
      >
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
        </svg>
      </button>
    </div>

    <!-- Template Categories -->
    <div class="flex-shrink-0 p-4 border-b border-gray-100">
      <div class="flex space-x-2">
        <button
          v-for="category in categories"
          :key="category.key"
          @click="selectedCategory = category.key"
          :class="selectedCategory === category.key 
            ? 'bg-purple-100 text-purple-700 border-purple-200' 
            : 'bg-gray-50 text-gray-600 border-gray-200 hover:bg-gray-100'"
          class="px-3 py-1.5 text-sm rounded-lg border transition-colors"
        >
          {{ category.name }}
        </button>
      </div>
    </div>

    <!-- Templates List -->
    <div class="flex-1 overflow-y-auto p-4 space-y-3">
      <div
        v-for="template in filteredTemplates"
        :key="template.id"
        class="template-card p-4 border border-gray-200 rounded-lg hover:border-purple-300 hover:shadow-md transition-all cursor-pointer group"
        @click="selectTemplate(template)"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <div class="flex items-center space-x-2 mb-2">
              <div class="text-2xl">{{ template.icon }}</div>
              <h4 class="font-semibold text-gray-800 group-hover:text-purple-700">
                {{ template.name }}
              </h4>
              <span v-if="template.isPro" class="px-2 py-0.5 bg-yellow-100 text-yellow-700 text-xs rounded-full">
                Pro
              </span>
            </div>
            <p class="text-sm text-gray-600 mb-3 line-clamp-2">
              {{ template.description }}
            </p>
            <div class="flex flex-wrap gap-1">
              <span
                v-for="tag in template.tags"
                :key="tag"
                class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded"
              >
                {{ tag }}
              </span>
            </div>
          </div>
        </div>

        <!-- Template Preview -->
        <div v-if="template.preview" class="mt-3 pt-3 border-t border-gray-100">
          <p class="text-xs text-gray-500 mb-2">预览:</p>
          <div class="text-xs text-gray-700 bg-gray-50 p-2 rounded italic">
            "{{ template.preview }}"
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="mt-3 pt-3 border-t border-gray-100 flex space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            @click.stop="useTemplate(template)"
            class="text-xs px-3 py-1 bg-purple-600 text-white rounded hover:bg-purple-700 transition-colors"
          >
            使用模板
          </button>
          <button
            @click.stop="previewTemplate(template)"
            class="text-xs px-3 py-1 bg-gray-100 text-gray-600 rounded hover:bg-gray-200 transition-colors"
          >
            详细预览
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="filteredTemplates.length === 0" class="text-center py-8">
        <div class="text-4xl mb-2">📝</div>
        <p class="text-gray-500">该分类下暂无模板</p>
      </div>
    </div>

    <!-- Template Preview Modal -->
    <div v-if="showPreviewModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50" @click="showPreviewModal = false">
      <div class="bg-white rounded-lg max-w-2xl w-full mx-4 max-h-[80vh] overflow-hidden" @click.stop>
        <div class="p-4 border-b border-gray-200">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div class="text-2xl">{{ selectedTemplate?.icon }}</div>
              <div>
                <h3 class="text-lg font-semibold">{{ selectedTemplate?.name }}</h3>
                <p class="text-sm text-gray-600">{{ selectedTemplate?.description }}</p>
              </div>
            </div>
            <button @click="showPreviewModal = false" class="text-gray-400 hover:text-gray-600">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
        </div>
        
        <div class="p-6 overflow-y-auto max-h-96">
          <div class="prose prose-sm max-w-none">
            <div v-html="selectedTemplate?.fullContent || selectedTemplate?.content"></div>
          </div>
        </div>
        
        <div class="p-4 border-t border-gray-200 flex justify-end space-x-3">
          <button 
            @click="showPreviewModal = false"
            class="px-4 py-2 text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
          >
            取消
          </button>
          <button 
            @click="useTemplate(selectedTemplate); showPreviewModal = false"
            class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
          >
            使用此模板
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { showSuccess } from '@/utils/toast-service'

const emit = defineEmits(['toggle-panel', 'use-template'])

// UI State
const selectedCategory = ref('academic')
const showPreviewModal = ref(false)
const selectedTemplate = ref(null)

// Categories
const categories = [
  { key: 'academic', name: '学术论文' },
  { key: 'business', name: '商业文档' },
  { key: 'creative', name: '创意写作' },
  { key: 'technical', name: '技术文档' },
  { key: 'personal', name: '个人文档' }
]

// Templates Data
const templates = reactive([
  // Academic Templates
  {
    id: 'research-paper',
    category: 'academic',
    name: '研究论文',
    icon: '🎓',
    description: '标准学术研究论文格式，包含摘要、引言、方法、结果、讨论等部分',
    tags: ['学术', '研究', 'APA格式'],
    preview: '摘要：本研究旨在探讨...',
    content: `<h1>论文标题</h1>
<h2>摘要</h2>
<p>本研究旨在探讨...（请在此处添加您的研究摘要，简要说明研究目的、方法、结果和结论）</p>

<h2>关键词</h2>
<p>关键词1, 关键词2, 关键词3</p>

<h2>1. 引言</h2>
<p>（研究背景和问题陈述）</p>

<h2>2. 文献综述</h2>
<p>（相关研究回顾）</p>

<h2>3. 研究方法</h2>
<p>（研究设计和方法）</p>

<h2>4. 结果与分析</h2>
<p>（研究发现）</p>

<h2>5. 讨论</h2>
<p>（结果讨论）</p>

<h2>6. 结论</h2>
<p>（研究结论和建议）</p>

<h2>参考文献</h2>
<p>（按照学术格式添加参考文献）</p>`
  },
  {
    id: 'essay',
    category: 'academic',
    name: '学术论文',
    icon: '📖',
    description: '经典的五段式论文结构，适用于各种学术写作',
    tags: ['论文', '五段式', '学术写作'],
    preview: '在当今社会中...',
    content: `<h1>论文标题</h1>

<h2>引言</h2>
<p>在当今社会中...（请在此处提出您的主题和论点）</p>

<h2>论点一</h2>
<p>（第一个支撑论点及其论证）</p>

<h2>论点二</h2>
<p>（第二个支撑论点及其论证）</p>

<h2>论点三</h2>
<p>（第三个支撑论点及其论证）</p>

<h2>结论</h2>
<p>（总结论点，重申主题，提出展望）</p>`
  },

  // Business Templates
  {
    id: 'business-plan',
    category: 'business',
    name: '商业计划书',
    icon: '💼',
    description: '完整的商业计划书模板，包含市场分析、财务预测等核心部分',
    tags: ['商业', '计划书', '创业'],
    preview: '执行摘要：本计划书旨在...',
    content: `<h1>商业计划书</h1>

<h2>执行摘要</h2>
<p>本计划书旨在...（简要概述您的商业想法和关键信息）</p>

<h2>公司描述</h2>
<p>（公司背景、使命和愿景）</p>

<h2>市场分析</h2>
<p>（目标市场、竞争分析）</p>

<h2>产品或服务</h2>
<p>（详细描述您的产品或服务）</p>

<h2>营销策略</h2>
<p>（市场推广和销售策略）</p>

<h2>运营计划</h2>
<p>（日常运营和管理结构）</p>

<h2>财务预测</h2>
<p>（收入预测、成本分析、盈利预期）</p>

<h2>风险分析</h2>
<p>（潜在风险和应对措施）</p>`
  },
  {
    id: 'project-proposal',
    category: 'business',
    name: '项目提案',
    icon: '📋',
    description: '标准项目提案格式，适用于内部项目申请或客户提案',
    tags: ['项目', '提案', '商务'],
    preview: '项目概述：本项目旨在...',
    content: `<h1>项目提案</h1>

<h2>项目概述</h2>
<p>本项目旨在...（简要介绍项目背景和目标）</p>

<h2>问题陈述</h2>
<p>（描述需要解决的问题或挑战）</p>

<h2>解决方案</h2>
<p>（提出的解决方案和方法）</p>

<h2>项目目标</h2>
<p>（具体、可衡量的项目目标）</p>

<h2>实施计划</h2>
<p>（项目时间线和里程碑）</p>

<h2>资源需求</h2>
<p>（人力、物力、财力需求）</p>

<h2>预期结果</h2>
<p>（项目预期成果和效益）</p>

<h2>风险管理</h2>
<p>（潜在风险和缓解措施）</p>`
  },

  // Creative Templates
  {
    id: 'short-story',
    category: 'creative',
    name: '短篇小说',
    icon: '📚',
    description: '短篇小说创作模板，包含基本的故事结构指导',
    tags: ['小说', '创作', '文学'],
    preview: '在一个寂静的夜晚...',
    content: `<h1>短篇小说标题</h1>

<p>在一个寂静的夜晚...（开场，设置场景和氛围）</p>

<p>（人物介绍）</p>

<p>（冲突的引入）</p>

<p>（情节发展）</p>

<p>（高潮）</p>

<p>（结局）</p>`
  },
  {
    id: 'blog-post',
    category: 'creative',
    name: '博客文章',
    icon: '✍️',
    description: '引人入胜的博客文章模板，适用于个人博客或内容营销',
    tags: ['博客', '内容', '写作'],
    preview: '你是否曾经想过...',
    content: `<h1>博客标题</h1>

<p>你是否曾经想过...（抓住读者注意力的开头）</p>

<h2>子标题一</h2>
<p>（第一个要点或故事）</p>

<h2>子标题二</h2>
<p>（第二个要点或故事）</p>

<h2>子标题三</h2>
<p>（第三个要点或故事）</p>

<h2>结论</h2>
<p>（总结要点，号召行动或提供思考）</p>`
  },

  // Technical Templates
  {
    id: 'api-documentation',
    category: 'technical',
    name: 'API 文档',
    icon: '🔧',
    description: 'RESTful API 文档模板，包含端点描述、参数说明等',
    tags: ['API', '文档', '技术'],
    preview: 'API 概述：本API提供...',
    content: `<h1>API 文档</h1>

<h2>概述</h2>
<p>本API提供...（API的基本介绍和用途）</p>

<h2>认证</h2>
<p>（认证方式说明）</p>

<h2>基础URL</h2>
<pre><code>https://api.example.com/v1</code></pre>

<h2>端点</h2>

<h3>GET /users</h3>
<p>获取用户列表</p>
<p><strong>参数：</strong></p>
<ul>
<li>page (可选): 页码</li>
<li>limit (可选): 每页数量</li>
</ul>

<p><strong>响应示例：</strong></p>
<pre><code>{
  "users": [],
  "total": 100,
  "page": 1
}</code></pre>

<h2>错误代码</h2>
<p>（常见错误代码说明）</p>`
  },

  // Personal Templates
  {
    id: 'diary',
    category: 'personal',
    name: '日记模板',
    icon: '📔',
    description: '每日反思和记录模板，帮助您养成写日记的习惯',
    tags: ['日记', '反思', '个人'],
    preview: '今天是2024年...',
    content: `<h1>日记 - [日期]</h1>

<h2>今日天气</h2>
<p>（今天的天气情况）</p>

<h2>今日亮点</h2>
<p>（今天最值得记住的事情）</p>

<h2>今日学习</h2>
<p>（今天学到的新知识或技能）</p>

<h2>今日感悟</h2>
<p>（今天的思考和感受）</p>

<h2>明日计划</h2>
<p>（明天的主要计划和目标）</p>

<h2>感恩记录</h2>
<p>（今天感谢的人或事）</p>`
  },
  {
    id: 'meeting-notes',
    category: 'personal',
    name: '会议纪要',
    icon: '📝',
    description: '标准会议记录模板，确保重要信息不遗漏',
    tags: ['会议', '纪要', '工作'],
    preview: '会议主题：...',
    content: `<h1>会议纪要</h1>

<p><strong>会议主题：</strong></p>
<p><strong>会议时间：</strong></p>
<p><strong>会议地点：</strong></p>
<p><strong>主持人：</strong></p>
<p><strong>参会人员：</strong></p>

<h2>会议议程</h2>
<ol>
<li>（议程项目一）</li>
<li>（议程项目二）</li>
<li>（议程项目三）</li>
</ol>

<h2>讨论要点</h2>
<p>（主要讨论内容和观点）</p>

<h2>决定事项</h2>
<ul>
<li>（决定一）</li>
<li>（决定二）</li>
</ul>

<h2>行动项目</h2>
<ul>
<li>（任务）- 负责人：XXX，截止时间：XXXX</li>
</ul>

<h2>下次会议</h2>
<p><strong>时间：</strong></p>
<p><strong>议题：</strong></p>`
  }
])

// Computed
const filteredTemplates = computed(() => {
  return templates.filter(template => template.category === selectedCategory.value)
})

// Methods
const selectTemplate = (template) => {
  selectedTemplate.value = template
}

const previewTemplate = (template) => {
  selectedTemplate.value = template
  showPreviewModal.value = true
}

const useTemplate = (template) => {
  emit('use-template', template)
  showSuccess(`已应用模板: ${template.name}`)
}
</script>

<style scoped>
.templates-panel {
  min-height: 400px;
  max-height: 100vh;
}

.template-card {
  transition: all 0.2s ease;
}

.template-card:hover {
  transform: translateY(-2px);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>