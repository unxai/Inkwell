import { defineStore } from 'pinia'
import axios from 'axios'

export const useDocumentStore = defineStore('document', {
  state: () => ({
    outline: [],
    isGeneratingOutline: false,
    documentType: 'article', // 'article', 'academic', 'creative'
  }),
  
  actions: {
    async generateOutline(topic, keywords, depth, style) {
      this.isGeneratingOutline = true
      
      try {
        const response = await axios.post('/api/v1/document/outline', {
          topic,
          keywords,
          depth,
          style
        })
        
        this.outline = response.data.outline
        return this.outline
      } catch (error) {
        console.error('生成大纲失败:', error)
        throw error
      } finally {
        this.isGeneratingOutline = false
      }
    },
    
    async generateAcademicStructure(title, outline) {
      try {
        const response = await axios.post('/api/v1/document/academic', {
          title,
          type: 'academic',
          outline
        })
        
        return response.data.content
      } catch (error) {
        console.error('生成学术论文结构失败:', error)
        throw error
      }
    },
    
    setDocumentType(type) {
      this.documentType = type
    },
    
    updateOutline(newOutline) {
      this.outline = newOutline
    }
  }
})