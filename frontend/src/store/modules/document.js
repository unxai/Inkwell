import { defineStore } from 'pinia'
import axios from 'axios'

export const useDocumentStore = defineStore('document', {
  state: () => ({
    outline: [],
    isGeneratingOutline: false,
    documentType: 'article', // 'article', 'academic', 'creative'
  }),
  
  actions: {
    
    setDocumentType(type) {
      this.documentType = type
    },
    
    updateOutline(newOutline) {
      this.outline = newOutline
    }
  }
})