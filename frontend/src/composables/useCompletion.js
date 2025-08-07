import { ref, computed } from 'vue'
import WebSocketService from '../utils/websocket-service'

/**
 * 文本补全组合式函数
 * @param {Object} options - 配置选项
 * @returns {Object} - 文本补全相关的状态和方法
 */
export function useCompletion(options = {}) {
  const {
    wsUrl = 'ws://localhost:8000/api/v1/completion/ws',
    contextWindowBefore = 1536,
    contextWindowAfter = 256
  } = options

  // 状态
  const isConnected = ref(false)
  const isGenerating = ref(false)
  const currentCompletion = ref('')
  const completionBuffer = ref('')
  const status = ref('空闲')
  const error = ref(null)
  const currentAction = ref('completion') // 当前操作类型：completion, rewrite, expand, simplify

  // WebSocket服务
  const ws = new WebSocketService(wsUrl)

  // 计算属性
  const isReady = computed(() => isConnected.value && !isGenerating.value)
  const canReconnect = computed(() => {
    const state = ws.getConnectionState()
    return !state.isConnected && !state.isConnecting && !state.shouldReconnect
  })

  // 连接WebSocket
  const connect = () => {
    ws.connect()
  }

  // 手动重连
  const reconnect = () => {
    console.log('手动重连WebSocket')
    ws.resetReconnect()
    ws.connect()
  }
  // 断开WebSocket连接
  const disconnect = () => {
    ws.disconnect()
  }

  // 发送WebSocket消息
  const send = (data) => {
    if (!isConnected.value) {
      error.value = '未连接到服务器'
      return false
    }

    return ws.send(data)
  }

  // 请求文本补全
  const requestCompletion = (text, contextBefore = null, contextAfter = null, cursorPosition = null) => {
    if (!isConnected.value) {
      error.value = '未连接到服务器'
      return false
    }

    if (isGenerating.value) {
      error.value = '正在生成中，请等待完成'
      return false
    }

    isGenerating.value = true
    status.value = '生成中...'
    currentCompletion.value = ''
    completionBuffer.value = ''
    error.value = null
    currentAction.value = 'completion'

    return ws.requestCompletion(text, contextBefore, contextAfter, cursorPosition)
  }

  // 请求文本优化（改写/扩写/简化）
  const requestTextOptimization = (text, action) => {
    if (!isConnected.value) {
      error.value = '未连接到服务器'
      return false
    }

    if (isGenerating.value) {
      error.value = '正在生成中，请等待完成'
      return false
    }

    isGenerating.value = true
    status.value = action === 'rewrite' ? '改写中...' : 
                   action === 'expand' ? '扩写中...' : 
                   action === 'simplify' ? '简化中...' : '处理中...'
    currentCompletion.value = ''
    completionBuffer.value = ''
    error.value = null
    currentAction.value = action

    return ws.send({
      text,
      action,
      temperature: action === 'expand' ? 0.8 : 0.5 // 扩写时使用更高的创造性
    })
  }

  // 取消当前生成
  const cancelCompletion = () => {
    if (isGenerating.value) {
      isGenerating.value = false
      status.value = '已取消'
      currentCompletion.value = ''
      completionBuffer.value = ''
    }
  }

  // 处理WebSocket事件
  ws.on('open', () => {
    isConnected.value = true
    status.value = '已连接'
  })

  ws.on('close', (event) => {
    isConnected.value = false
    status.value = '未连接'
    
    // 清理生成状态，避免loading状态卡住
    if (isGenerating.value) {
      isGenerating.value = false
      currentCompletion.value = ''
      completionBuffer.value = ''
      
      // 设置错误信息，通知用户连接中断
      if (event && event.code === 1001) {
        error.value = 'WebSocket连接异常关闭，请重试'
      } else {
        error.value = '连接已断开'
      }
      
      console.warn('WebSocket连接关闭，清理生成状态', { code: event?.code, reason: event?.reason })
    }
  })

  ws.on('error', (err) => {
    error.value = '连接错误: ' + (err?.message || err)
    status.value = '错误'
    
    // 清理生成状态
    if (isGenerating.value) {
      isGenerating.value = false
      currentCompletion.value = ''
      completionBuffer.value = ''
      console.error('WebSocket错误，清理生成状态', err)
    }
  })

  ws.on('completion', (data) => {
    if (data.type === 'start') {
      completionBuffer.value = ''
      status.value = currentAction.value === 'completion' ? '生成中...' : 
                     currentAction.value === 'rewrite' ? '改写中...' : 
                     currentAction.value === 'expand' ? '扩写中...' : 
                     currentAction.value === 'simplify' ? '简化中...' : '处理中...'
    } else if (data.type === 'token') {
      completionBuffer.value += data.token
      currentCompletion.value = completionBuffer.value
    } else if (data.type === 'end') {
      currentCompletion.value = data.completion || completionBuffer.value
      isGenerating.value = false
      status.value = '已完成'
    } else if (data.type === 'error') {
      // 处理错误消息
      error.value = data.error || '处理请求时出错'
      status.value = '错误'
      isGenerating.value = false
      currentCompletion.value = ''
      completionBuffer.value = ''
    }
  })

  // 自动连接
  connect()

  return {
    isConnected,
    isGenerating,
    isReady,
    canReconnect,
    status,
    error,
    currentCompletion,
    currentAction,
    contextWindowBefore,
    contextWindowAfter,
    connect,
    reconnect,
    disconnect,
    send,
    requestCompletion,
    requestTextOptimization,
    cancelCompletion,
    on: ws.on.bind(ws),
    off: ws.off.bind(ws)
  }
}
