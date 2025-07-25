<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-bold text-inkwell-blue mb-6">学术论文结构生成器</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <!-- 左侧：用户输入区 -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <h2 class="text-lg font-semibold mb-4">论文信息</h2>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">论文类型</label>
            <select 
              v-model="paperType" 
              class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-inkwell-teal focus:border-transparent"
            >
              <option value="research">研究论文</option>
              <option value="review">综述论文</option>
              <option value="case-study">案例研究</option>
              <option value="thesis">学位论文</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">学科领域</label>
            <select 
              v-model="discipline" 
              class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-inkwell-teal focus:border-transparent"
            >
              <option value="science">自然科学</option>
              <option value="social">社会科学</option>
              <option value="humanities">人文学科</option>
              <option value="engineering">工程技术</option>
              <option value="medicine">医学</option>
              <option value="business">商业管理</option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">论文标题</label>
            <input 
              v-model="title" 
              type="text" 
              class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-inkwell-teal focus:border-transparent"
              placeholder="输入论文标题"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">研究问题/目标</label>
            <textarea 
              v-model="researchQuestion" 
              rows="3" 
              class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-inkwell-teal focus:border-transparent"
              placeholder="描述您的研究问题或研究目标"
            ></textarea>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">关键词</label>
            <input 
              v-model="keywords" 
              type="text" 
              class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-inkwell-teal focus:border-transparent"
              placeholder="用逗号分隔关键词"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">引用格式</label>
            <select 
              v-model="citationStyle" 
              class="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-inkwell-teal focus:border-transparent"
            >
              <option value="apa">APA</option>
              <option value="mla">MLA</option>
              <option value="chicago">Chicago</option>
              <option value="harvard">Harvard</option>
              <option value="ieee">IEEE</option>
            </select>
          </div>
          
          <button 
            @click="generateStructure" 
            class="w-full bg-inkwell-blue hover:bg-blue-800 text-white font-medium py-2 px-4 rounded-md transition-colors"
            :disabled="isGenerating"
          >
            {{ isGenerating ? '生成中...' : '生成论文结构' }}
          </button>
        </div>
      </div>
      
      <!-- 右侧：生成的结构预览 -->
      <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold">论文结构</h2>
          <div class="flex space-x-2">
            <button 
              @click="copyToClipboard" 
              class="text-inkwell-blue hover:text-blue-800 p-1"
              title="复制到剪贴板"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
                <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z" />
              </svg>
            </button>
            <button 
              @click="createNewDocument" 
              class="text-inkwell-blue hover:text-blue-800 p-1"
              title="创建新文档"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M6 2a2 2 0 00-2 2v12a2 2 0 002 2h8a2 2 0 002-2V7.414A2 2 0 0015.414 6L12 2.586A2 2 0 0010.586 2H6zm5 6a1 1 0 10-2 0v2H7a1 1 0 100 2h2v2a1 1 0 102 0v-2h2a1 1 0 100-2h-2V8z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>
        </div>
        
        <div v-if="isGenerating" class="flex justify-center items-center h-64">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-inkwell-blue"></div>
        </div>
        
        <div v-else-if="structure" class="structure-preview overflow-y-auto max-h-[500px]">
          <div v-html="formattedStructure"></div>
        </div>
        
        <div v-else class="flex flex-col justify-center items-center h-64 text-gray-500">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <p>填写左侧表单并点击"生成论文结构"</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()

// 表单数据
const paperType = ref('research')
const discipline = ref('science')
const title = ref('')
const researchQuestion = ref('')
const keywords = ref('')
const citationStyle = ref('apa')

// 状态
const isGenerating = ref(false)
const structure = ref(null)
const error = ref(null)

// 格式化结构
const formattedStructure = computed(() => {
  if (!structure.value) return ''
  
  // 将结构转换为HTML
  let html = `<h2 class="text-xl font-bold mb-3">${structure.value.title}</h2>`
  
  // 添加摘要
  if (structure.value.abstract) {
    html += `<div class="mb-4">
      <h3 class="text-lg font-semibold mb-2">摘要</h3>
      <p class="text-gray-700">${structure.value.abstract}</p>
    </div>`
  }
  
  // 添加章节
  if (structure.value.sections && structure.value.sections.length > 0) {
    html += `<div class="mb-4">
      <h3 class="text-lg font-semibold mb-2">章节结构</h3>
      <ul class="list-disc pl-5 space-y-2">`
    
    structure.value.sections.forEach(section => {
      html += `<li>
        <div class="font-medium">${section.title}</div>`
      
      if (section.description) {
        html += `<div class="text-sm text-gray-600 mt-1">${section.description}</div>`
      }
      
      if (section.subsections && section.subsections.length > 0) {
        html += `<ul class="list-circle pl-5 mt-2 space-y-1">`
        section.subsections.forEach(subsection => {
          html += `<li>
            <div class="font-medium">${subsection.title}</div>`
          
          if (subsection.description) {
            html += `<div class="text-sm text-gray-600 mt-1">${subsection.description}</div>`
          }
          
          html += `</li>`
        })
        html += `</ul>`
      }
      
      html += `</li>`
    })
    
    html += `</ul></div>`
  }
  
  // 添加引用指南
  if (structure.value.citationGuide) {
    html += `<div class="mb-4">
      <h3 class="text-lg font-semibold mb-2">引用指南 (${citationStyle.value.toUpperCase()})</h3>
      <div class="text-gray-700">${structure.value.citationGuide}</div>
    </div>`
  }
  
  return html
})

// 生成论文结构
const generateStructure = async () => {
  if (!title.value) {
    alert('请输入论文标题')
    return
  }
  
  isGenerating.value = true
  error.value = null
  
  try {
    // 调用后端API生成论文结构
    const response = await axios.post('/api/v1/academic/structure', {
      paper_type: paperType.value,
      discipline: discipline.value,
      title: title.value,
      research_question: researchQuestion.value,
      keywords: keywords.value,
      citation_style: citationStyle.value
    })
    
    structure.value = response.data
  } catch (err) {
    console.error('生成论文结构失败:', err)
    error.value = err.message || '生成失败，请重试'
    
    // 如果API尚未实现，使用模拟数据
    structure.value = generateMockStructure()
  } finally {
    isGenerating.value = false
  }
}

// 生成模拟数据（在API实现前使用）
const generateMockStructure = () => {
  const mockStructures = {
    research: {
      title: title.value || '研究论文标题',
      abstract: '本研究旨在探讨...[摘要内容将根据研究问题生成]',
      sections: [
        {
          title: '1. 引言',
          description: '介绍研究背景、问题陈述和研究目的',
          subsections: [
            { title: '1.1 研究背景', description: '概述研究领域的当前状态和重要性' },
            { title: '1.2 问题陈述', description: '明确定义待解决的研究问题' },
            { title: '1.3 研究目的和目标', description: '阐述研究的具体目标和预期成果' }
          ]
        },
        {
          title: '2. 文献综述',
          description: '回顾和评价相关研究文献',
          subsections: [
            { title: '2.1 理论框架', description: '讨论支持研究的理论基础' },
            { title: '2.2 相关研究', description: '分析与研究问题相关的现有研究' },
            { title: '2.3 研究差距', description: '确定现有研究中的不足之处' }
          ]
        },
        {
          title: '3. 研究方法',
          description: '详细说明研究设计和方法',
          subsections: [
            { title: '3.1 研究设计', description: '描述研究的整体方法和设计' },
            { title: '3.2 数据收集', description: '解释数据收集的方法和工具' },
            { title: '3.3 数据分析', description: '详述数据分析的技术和程序' }
          ]
        },
        {
          title: '4. 结果',
          description: '呈现研究发现',
          subsections: [
            { title: '4.1 主要发现', description: '展示与研究问题直接相关的结果' },
            { title: '4.2 数据分析', description: '提供详细的数据分析和统计结果' }
          ]
        },
        {
          title: '5. 讨论',
          description: '解释和评价研究结果',
          subsections: [
            { title: '5.1 结果解释', description: '解释研究发现的意义' },
            { title: '5.2 与现有研究的比较', description: '将结果与现有文献进行比较' },
            { title: '5.3 研究局限性', description: '讨论研究的局限性和不足' }
          ]
        },
        {
          title: '6. 结论',
          description: '总结研究的主要发现和贡献',
          subsections: [
            { title: '6.1 研究总结', description: '概述研究的主要发现和结论' },
            { title: '6.2 理论和实践意义', description: '讨论研究对理论和实践的贡献' },
            { title: '6.3 未来研究方向', description: '提出未来研究的建议' }
          ]
        }
      ],
      citationGuide: getCitationGuide(citationStyle.value)
    },
    review: {
      title: title.value || '综述论文标题',
      abstract: '本综述旨在评估...[摘要内容将根据研究问题生成]',
      sections: [
        {
          title: '1. 引言',
          description: '介绍综述的目的和范围',
          subsections: [
            { title: '1.1 研究领域概述', description: '概述综述所涵盖的研究领域' },
            { title: '1.2 综述目的', description: '阐明进行此综述的原因和目标' },
            { title: '1.3 综述范围和方法', description: '定义综述的范围和采用的方法' }
          ]
        },
        {
          title: '2. 文献搜索方法',
          description: '描述文献检索和筛选的过程',
          subsections: [
            { title: '2.1 搜索策略', description: '详述文献搜索的策略和关键词' },
            { title: '2.2 纳入和排除标准', description: '说明文献筛选的标准' },
            { title: '2.3 文献评价方法', description: '解释如何评估所选文献的质量' }
          ]
        },
        {
          title: '3. 文献综述',
          description: '按主题或时间顺序组织文献回顾',
          subsections: [
            { title: '3.1 主题一', description: '分析与第一个主题相关的文献' },
            { title: '3.2 主题二', description: '分析与第二个主题相关的文献' },
            { title: '3.3 主题三', description: '分析与第三个主题相关的文献' }
          ]
        },
        {
          title: '4. 综合分析',
          description: '整合和比较文献中的发现',
          subsections: [
            { title: '4.1 主要趋势和模式', description: '识别文献中的主要趋势和模式' },
            { title: '4.2 争议和差距', description: '讨论文献中的争议和研究差距' },
            { title: '4.3 理论框架', description: '提出或修改理论框架' }
          ]
        },
        {
          title: '5. 讨论和未来方向',
          description: '讨论综述的意义和未来研究方向',
          subsections: [
            { title: '5.1 综述的意义', description: '讨论综述对研究领域的贡献' },
            { title: '5.2 实践启示', description: '探讨综述对实践的启示' },
            { title: '5.3 未来研究方向', description: '提出未来研究的建议' }
          ]
        },
        {
          title: '6. 结论',
          description: '总结综述的主要发现和贡献',
          subsections: []
        }
      ],
      citationGuide: getCitationGuide(citationStyle.value)
    }
  }
  
  return mockStructures[paperType.value] || mockStructures.research
}

// 获取引用格式指南
const getCitationGuide = (style) => {
  const guides = {
    apa: `
      <p class="mb-2">APA格式（第7版）引用示例：</p>
      <ul class="list-disc pl-5 space-y-1 text-sm">
        <li><strong>期刊文章：</strong> 作者, A. A., 作者, B. B., & 作者, C. C. (年份). 文章标题. <em>期刊名称</em>, <em>卷</em>(期), 页码. DOI</li>
        <li><strong>书籍：</strong> 作者, A. A. (年份). <em>书名</em>. 出版商.</li>
        <li><strong>编辑书籍中的章节：</strong> 作者, A. A., & 作者, B. B. (年份). 章节标题. 在 A. 编辑 & B. 编辑 (编), <em>书名</em> (页码). 出版商.</li>
        <li><strong>网页：</strong> 作者, A. A. (年份, 月 日). 标题. 网站名称. URL</li>
      </ul>
    `,
    mla: `
      <p class="mb-2">MLA格式（第8版）引用示例：</p>
      <ul class="list-disc pl-5 space-y-1 text-sm">
        <li><strong>期刊文章：</strong> 作者姓, 名. "文章标题." <em>期刊名称</em>, 卷, 期, 年份, 页码.</li>
        <li><strong>书籍：</strong> 作者姓, 名. <em>书名</em>. 出版商, 年份.</li>
        <li><strong>编辑书籍中的章节：</strong> 作者姓, 名. "章节标题." <em>书名</em>, 编辑 名 姓, 出版商, 年份, 页码.</li>
        <li><strong>网页：</strong> 作者姓, 名. "标题." <em>网站名称</em>, 出版商, 日 月 年份, URL.</li>
      </ul>
    `,
    chicago: `
      <p class="mb-2">Chicago格式（第17版）引用示例：</p>
      <ul class="list-disc pl-5 space-y-1 text-sm">
        <li><strong>脚注（期刊文章）：</strong> 名 姓, "文章标题," <em>期刊名称</em> 卷, 期 (年份): 页码.</li>
        <li><strong>脚注（书籍）：</strong> 名 姓, <em>书名</em> (出版地: 出版商, 年份), 页码.</li>
        <li><strong>参考文献（期刊文章）：</strong> 姓, 名. "文章标题." <em>期刊名称</em> 卷, 期 (年份): 页码.</li>
        <li><strong>参考文献（书籍）：</strong> 姓, 名. <em>书名</em>. 出版地: 出版商, 年份.</li>
      </ul>
    `,
    harvard: `
      <p class="mb-2">Harvard格式引用示例：</p>
      <ul class="list-disc pl-5 space-y-1 text-sm">
        <li><strong>正文引用：</strong> (作者姓, 年份, p. 页码)</li>
        <li><strong>参考文献（期刊文章）：</strong> 作者姓, 名首字母. (年份) '文章标题', <em>期刊名称</em>, 卷(期), 页码.</li>
        <li><strong>参考文献（书籍）：</strong> 作者姓, 名首字母. (年份) <em>书名</em>. 出版地: 出版商.</li>
        <li><strong>参考文献（网页）：</strong> 作者姓, 名首字母. (年份) <em>标题</em> [在线]. 可获取于: URL [访问日期: 日 月 年].</li>
      </ul>
    `,
    ieee: `
      <p class="mb-2">IEEE格式引用示例：</p>
      <ul class="list-disc pl-5 space-y-1 text-sm">
        <li><strong>期刊文章：</strong> [1] A. A. 作者, B. B. 作者, 和 C. C. 作者, "文章标题," <em>期刊名称缩写</em>, 卷, 期, 页码, 月 年份.</li>
        <li><strong>书籍：</strong> [2] A. A. 作者, <em>书名</em>. 出版地: 出版商, 年份, 页码.</li>
        <li><strong>会议论文：</strong> [3] A. A. 作者, "论文标题," 在 <em>会议名称缩写</em>, 地点, 年份, 页码.</li>
        <li><strong>网页：</strong> [4] "页面标题," 网站名称. [在线]. 可获取于: URL (访问日期: 日-月-年).</li>
      </ul>
    `
  }
  
  return guides[style] || guides.apa
}

// 复制到剪贴板
const copyToClipboard = () => {
  if (!structure.value) return
  
  // 创建纯文本版本的结构
  let text = `${structure.value.title}\n\n`
  text += `摘要:\n${structure.value.abstract}\n\n`
  text += `章节结构:\n`
  
  structure.value.sections.forEach(section => {
    text += `${section.title}\n`
    if (section.description) {
      text += `${section.description}\n`
    }
    
    if (section.subsections && section.subsections.length > 0) {
      section.subsections.forEach(subsection => {
        text += `  ${subsection.title}\n`
        if (subsection.description) {
          text += `  ${subsection.description}\n`
        }
      })
    }
    text += '\n'
  })
  
  // 复制到剪贴板
  navigator.clipboard.writeText(text)
    .then(() => {
      alert('已复制到剪贴板')
    })
    .catch(err => {
      console.error('复制失败:', err)
      alert('复制失败，请手动复制')
    })
}

// 创建新文档
const createNewDocument = () => {
  if (!structure.value) return
  
  // 将结构转换为HTML内容
  let content = `<h1>${structure.value.title}</h1>`
  
  // 添加摘要
  content += `<h2>摘要</h2><p>${structure.value.abstract}</p>`
  
  // 添加章节
  structure.value.sections.forEach(section => {
    content += `<h2>${section.title}</h2>`
    if (section.description) {
      content += `<p><em>${section.description}</em></p>`
    }
    
    if (section.subsections && section.subsections.length > 0) {
      section.subsections.forEach(subsection => {
        content += `<h3>${subsection.title}</h3>`
        if (subsection.description) {
          content += `<p><em>${subsection.description}</em></p>`
        }
        // 添加一些占位符内容
        content += `<p>[在此处添加${subsection.title.toLowerCase()}的内容]</p>`
      })
    } else {
      // 添加一些占位符内容
      content += `<p>[在此处添加${section.title.toLowerCase()}的内容]</p>`
    }
  })
  
  // 添加参考文献部分
  content += `<h2>参考文献</h2><p>[在此处添加参考文献]</p>`
  
  // 保存到本地存储或状态管理
  localStorage.setItem('newDocument', content)
  
  // 导航到编辑器页面
  router.push({ 
    path: '/', 
    query: { 
      newDocument: 'true',
      title: structure.value.title
    } 
  })
}
</script>

<style scoped>
.structure-preview {
  line-height: 1.6;
}

/* 自定义列表样式 */
:deep(.list-circle) {
  list-style-type: circle;
}

:deep(h2) {
  color: #1A365D;
}

:deep(h3) {
  color: #2C5282;
}
</style>