import { defineStore } from 'pinia'
import axios from 'axios'

export const useReferenceStore = defineStore('reference', {
  state: () => ({
    references: [],
    selectedStyle: 'apa', // 'apa', 'mla', 'ieee', 'harvard'
  }),
  
  actions: {
    async formatReference(reference) {
      try {
        const response = await axios.post('/api/v1/reference/format', {
          ...reference,
          style: this.selectedStyle
        })
        
        return response.data.formatted_citation
      } catch (error) {
        console.error('格式化引用失败:', error)
        throw error
      }
    },
    
    async addReference(reference) {
      try {
        const formattedCitation = await this.formatReference(reference)
        
        const newReference = {
          ...reference,
          formattedCitation,
          id: Date.now().toString()
        }
        
        this.references.push(newReference)
        return newReference
      } catch (error) {
        console.error('添加引用失败:', error)
        throw error
      }
    },
    
    removeReference(id) {
      const index = this.references.findIndex(ref => ref.id === id)
      if (index !== -1) {
        this.references.splice(index, 1)
      }
    },
    
    setSelectedStyle(style) {
      this.selectedStyle = style
    },
    
    async updateAllReferencesFormat() {
      // 当引用样式改变时，更新所有引用的格式
      for (const reference of this.references) {
        try {
          reference.formattedCitation = await this.formatReference(reference)
        } catch (error) {
          console.error(`更新引用 ${reference.id} 格式失败:`, error)
        }
      }
    }
  }
})