import { defineStore } from 'pinia'
import axios from 'axios'

export const useEditorStore = defineStore('editor', {
  state: () => ({
    content: '<p>欢迎使用墨井智能写作助手！</p>',
    wordCount: 0,
    aiStatus: '空闲',
    isConnected: false,
    contextWindowBefore: 1536, // 上文token数
    contextWindowAfter: 256,   // 下文token数
    completionText: '',        // AI生成的补全文本
    isGenerating: false,       // 是否正在生成补全
    cursorPosition: 0,         // 当前光标位置
  }),
  
  actions: {
    /**
     * 更新编辑器内容
     * @param {string} newContent - 新的内容
     */
    updateContent(newContent) {
      this.content = newContent
      // 更新字数统计
      const textContent = newContent.replace(/<[^>]*>/g, '')
      this.wordCount = textContent.length
    },
    
    /**
     * 更新AI状态
     * @param {string} status - AI状态
     */
    updateAiStatus(status) {
      this.aiStatus = status
    },
    
    /**
     * 设置连接状态
     * @param {boolean} status - 连接状态
     */
    setConnectionStatus(status) {
      this.isConnected = status
    },
    
    /**
     * 更新光标位置
     * @param {number} position - 光标位置
     */
    updateCursorPosition(position) {
      this.cursorPosition = position
    },
    
    /**
     * 更新补全文本
     * @param {string} text - 补全文本
     */
    updateCompletionText(text) {
      this.completionText = text
    },
    
    /**
     * 设置生成状态
     * @param {boolean} isGenerating - 是否正在生成
     */
    setGeneratingState(isGenerating) {
      this.isGenerating = isGenerating
    },
    
    /**
     * 清除补全文本
     */
    clearCompletionText() {
      this.completionText = ''
    },
    
    /**
     * 接受补全建议
     */
    acceptCompletion() {
      // 清除补全文本
      this.completionText = ''
      this.isGenerating = false
    },
    
    /**
     * 拒绝补全建议
     */
    rejectCompletion() {
      // 清除补全文本
      this.completionText = ''
      this.isGenerating = false
    },
    
    /**
     * 优化文本（改写/扩写/简化）
     * @param {string} text - 要优化的文本
     * @param {string} type - 优化类型：'rewrite', 'expand', 'simplify'
     * @returns {Promise<string>} 优化后的文本
     */
    async optimizeText(text, type) {
      try {
        this.isGenerating = true
        this.aiStatus = type === 'rewrite' ? '改写中...' : 
                        type === 'expand' ? '扩写中...' : 
                        type === 'simplify' ? '简化中...' : '处理中...'
        
        const response = await axios.post('/api/v1/completion/optimize', {
          text,
          action: type,
          temperature: type === 'expand' ? 0.8 : 0.5
        })
        
        this.isGenerating = false
        this.aiStatus = '已完成'
        
        return response.data.completion
      } catch (error) {
        console.error('文本优化失败:', error)
        this.isGenerating = false
        this.aiStatus = '错误'
        throw error
      }
    }
  }
})