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
    updateContent(newContent) {
      this.content = newContent
      // 更新字数统计
      const textContent = newContent.replace(/<[^>]*>/g, '')
      this.wordCount = textContent.length
    },
    
    updateAiStatus(status) {
      this.aiStatus = status
    },
    
    setConnectionStatus(status) {
      this.isConnected = status
    },
    
    // 更新光标位置
    updateCursorPosition(position) {
      this.cursorPosition = position
    },
    
    // 更新补全文本
    updateCompletionText(text) {
      this.completionText = text
    },
    
    // 设置生成状态
    setGeneratingState(isGenerating) {
      this.isGenerating = isGenerating
    },
    
    // 清除补全文本
    clearCompletionText() {
      this.completionText = ''
    },
    
    // 接受补全建议
    acceptCompletion() {
      // 清除补全文本
      this.completionText = ''
      this.isGenerating = false
    },
    
    // 拒绝补全建议
    rejectCompletion() {
      // 清除补全文本
      this.completionText = ''
      this.isGenerating = false
    },
    
    async getCompletion(text, contextBefore, contextAfter, cursorPosition) {
      try {
        this.isGenerating = true
        this.aiStatus = '生成中...'
        
        const response = await axios.post('/api/v1/completion/generate', {
          text,
          context_before: contextBefore,
          context_after: contextAfter,
          cursor_position: cursorPosition,
          max_tokens: 50
        })
        
        this.completionText = response.data.completion
        this.isGenerating = false
        this.aiStatus = '已完成'
        
        return response.data.completion
      } catch (error) {
        console.error('获取文本补全失败:', error)
        this.isGenerating = false
        this.aiStatus = '错误'
        throw error
      }
    },
    
    async optimizeText(text, type) {
      // type: 'rewrite', 'expand', 'simplify'
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