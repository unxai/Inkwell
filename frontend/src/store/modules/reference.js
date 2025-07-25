import { defineStore } from 'pinia'
import axios from 'axios'

export const useReferenceStore = defineStore('reference', {
  state: () => ({
    references: [],
    selectedStyle: 'apa', // 'apa', 'mla', 'ieee', 'harvard'
  }),
  
  actions: {
    addReference(reference) {
      const newReference = {
        ...reference,
        id: Date.now().toString()
      }
      
      this.references.push(newReference)
      return newReference
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