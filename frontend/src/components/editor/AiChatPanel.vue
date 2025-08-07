<template>
  <div class="ai-chat-panel h-full flex flex-col bg-white">
    <!-- Chat Header -->
    <div class="flex items-center justify-between p-4 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
      <div class="flex items-center space-x-2">
        <div class="w-3 h-3 rounded-full bg-blue-500 animate-pulse"></div>
        <h3 class="text-lg font-semibold text-gray-800">AI 写作助手</h3>
      </div>
      <div class="flex items-center space-x-2">
        <span class="text-xs text-gray-500">{{ isConnected ? '已连接' : '未连接' }}</span>
        <button
          @click="$emit('toggle-panel')"
          class="p-1 text-gray-400 hover:text-gray-600 transition-colors"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="p-3 border-b border-gray-100">
      <div class="grid grid-cols-2 gap-2 text-xs">
        <button
          @click="insertSuggestion('继续写作')"
          class="p-2 text-left text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
        >
          💫 继续写作
        </button>
        <button
          @click="insertSuggestion('总结上文')"
          class="p-2 text-left text-green-600 bg-green-50 rounded-lg hover:bg-green-100 transition-colors"
        >
          📝 总结上文
        </button>
        <button
          @click="insertSuggestion('改善表达')"
          class="p-2 text-left text-purple-600 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors"
        >
          ✨ 改善表达
        </button>
        <button
          @click="insertSuggestion('添加例子')"
          class="p-2 text-left text-orange-600 bg-orange-50 rounded-lg hover:bg-orange-100 transition-colors"
        >
          💡 添加例子
        </button>
      </div>
    </div>

    <!-- Chat Messages -->
    <div class="flex-1 overflow-y-auto p-4 space-y-4" ref="messagesContainer">
      <div v-if="messages.length === 0" class="text-center text-gray-500 py-8">
        <div class="text-2xl mb-2">🤖</div>
        <p>你好！我是你的AI写作助手</p>
        <p class="text-sm mt-1">你可以问我关于写作的任何问题</p>
      </div>
      
      <div
        v-for="message in messages"
        :key="message.id"
        class="message-container"
        :class="message.role === 'user' ? 'user-message' : 'assistant-message'"
      >
        <div class="flex items-start space-x-3">
          <div class="flex-shrink-0">
            <div
              class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium"
              :class="message.role === 'user' 
                ? 'bg-blue-100 text-blue-700' 
                : 'bg-gray-100 text-gray-700'"
            >
              {{ message.role === 'user' ? '你' : 'AI' }}
            </div>
          </div>
          <div class="flex-1 space-y-1">
            <div
              class="inline-block p-3 rounded-lg max-w-full"
              :class="message.role === 'user' 
                ? 'bg-blue-600 text-white' 
                : 'bg-gray-100 text-gray-800'"
            >
              <p class="whitespace-pre-wrap text-sm" v-html="formatMessage(message.content)"></p>
            </div>
            <div class="text-xs text-gray-500">{{ formatTime(message.timestamp) }}</div>
          </div>
        </div>
        
        <!-- AI message actions -->
        <div v-if="message.role === 'assistant'" class="ml-11 mt-2 flex space-x-2">
          <button
            @click="copyToClipboard(message.content)"
            class="text-xs px-2 py-1 text-gray-500 hover:text-gray-700 hover:bg-gray-100 rounded transition-colors"
          >
            复制
          </button>
          <button
            @click="insertToEditor(message.content)"
            class="text-xs px-2 py-1 text-blue-500 hover:text-blue-700 hover:bg-blue-50 rounded transition-colors"
          >
            插入到编辑器
          </button>
        </div>
      </div>
      
      <!-- Loading indicator -->
      <div v-if="isLoading" class="flex items-start space-x-3">
        <div class="flex-shrink-0">
          <div class="w-8 h-8 rounded-full bg-gray-100 text-gray-700 flex items-center justify-center text-sm font-medium">
            AI
          </div>
        </div>
        <div class="flex-1">
          <div class="bg-gray-100 rounded-lg p-3">
            <div class="flex space-x-1">
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Chat Input -->
    <div class="border-t border-gray-200 p-4 bg-gray-50">
      <div class="flex space-x-2">
        <input
          v-model="newMessage"
          type="text"
          placeholder="问我关于写作的任何问题..."
          class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
          @keyup.enter="sendMessage"
          @keydown.ctrl.enter="sendMessage"
          :disabled="isLoading || !isConnected"
        />
        <button
          @click="sendMessage"
          :disabled="!newMessage.trim() || isLoading || !isConnected"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm font-medium"
        >
          <svg v-if="!isLoading" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
          </svg>
          <svg v-else class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <circle cx="12" cy="12" r="10" stroke-width="4" class="opacity-25"></circle>
            <path fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" class="opacity-75"></path>
          </svg>
        </button>
      </div>
      <div class="text-xs text-gray-500 mt-2 flex justify-between">
        <span>支持 Ctrl+Enter 发送</span>
        <span>{{ messages.length }} 条对话</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { showSuccess, showError } from '@/utils/toast-service'

const props = defineProps({
  isConnected: {
    type: Boolean,
    default: false
  },
  currentDocument: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['toggle-panel', 'insert-text'])

// Chat state
const messages = reactive([])
const newMessage = ref('')
const isLoading = ref(false)
const messagesContainer = ref(null)

// Initialize with a welcome message
onMounted(() => {
  messages.push({
    id: Date.now(),
    role: 'assistant',
    content: '你好！我是墨井的AI写作助手。我可以帮助你：\n\n• 续写文章内容\n• 改善文本表达\n• 提供写作建议\n• 回答写作相关问题\n\n有什么我可以帮助你的吗？',
    timestamp: new Date()
  })
})

// Scroll to bottom when new message is added
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// Send message to AI
const sendMessage = async () => {
  if (!newMessage.value.trim() || isLoading.value || !props.isConnected) return

  const userMessage = {
    id: Date.now(),
    role: 'user',
    content: newMessage.value.trim(),
    timestamp: new Date()
  }

  messages.push(userMessage)
  const currentMessage = newMessage.value.trim()
  newMessage.value = ''
  scrollToBottom()

  // Set loading state
  isLoading.value = true

  try {
    // Call AI service
    const response = await fetch('/api/v1/chat/completion', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: currentMessage,
        context: props.currentDocument ? props.currentDocument.slice(-1500) : '', // Last 1500 chars as context
        conversation_history: messages.slice(-10).map(msg => ({
          role: msg.role,
          content: msg.content
        }))
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()

    // Add AI response
    const aiMessage = {
      id: Date.now() + 1,
      role: 'assistant',
      content: data.response || '抱歉，我现在无法回答这个问题。',
      timestamp: new Date()
    }

    messages.push(aiMessage)
    scrollToBottom()

  } catch (error) {
    console.error('Chat error:', error)
    const errorMessage = {
      id: Date.now() + 1,
      role: 'assistant',
      content: '抱歉，发生了错误。请稍后重试。',
      timestamp: new Date()
    }
    messages.push(errorMessage)
    showError('AI聊天服务暂时不可用')
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

// Quick action suggestions
const insertSuggestion = (suggestion) => {
  newMessage.value = suggestion
  sendMessage()
}

// Format message content (simple markdown-like formatting)
const formatMessage = (content) => {
  return content
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/`(.*?)`/g, '<code class="bg-gray-100 px-1 rounded text-xs">$1</code>')
}

// Format timestamp
const formatTime = (timestamp) => {
  const now = new Date()
  const diff = now - timestamp
  const minutes = Math.floor(diff / 60000)
  
  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}小时前`
  
  return timestamp.toLocaleDateString()
}

// Copy to clipboard
const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    showSuccess('已复制到剪贴板')
  } catch (error) {
    console.error('Copy failed:', error)
    showError('复制失败')
  }
}

// Insert to editor
const insertToEditor = (text) => {
  emit('insert-text', text)
  showSuccess('已插入到编辑器')
}

// Clear chat history
const clearHistory = () => {
  messages.splice(0, messages.length)
  messages.push({
    id: Date.now(),
    role: 'assistant',
    content: '对话记录已清除。有什么我可以帮助你的吗？',
    timestamp: new Date()
  })
}

// Export chat method
defineExpose({
  clearHistory
})
</script>

<style scoped>
.ai-chat-panel {
  min-height: 400px;
  max-height: 100vh;
}

.message-container {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
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

/* Message styling */
.user-message {
  margin-left: 2rem;
}

.assistant-message {
  margin-right: 2rem;
}

/* Input focus styles */
input:focus {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Button hover effects */
button:hover:not(:disabled) {
  transform: translateY(-1px);
}

button:active:not(:disabled) {
  transform: translateY(0);
}
</style>