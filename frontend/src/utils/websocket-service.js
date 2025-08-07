/**
 * WebSocket服务类
 * 用于处理与后端的WebSocket通信
 */
class WebSocketService {
  constructor(url) {
    this.url = url || import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000';
    this.ws = null;
    this.isConnected = false;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 3; // 降低最大重连次数
    this.reconnectTimeout = null;
    this.shouldReconnect = true; // 添加重连开关
    this.isConnecting = false; // 防止重复连接
    
    // 添加请求限流
    this.lastRequestTime = 0;
    this.requestThrottleDelay = 500; // 500ms内最多发送一次请求
    
    this.listeners = {
      open: [],
      message: [],
      close: [],
      error: [],
      completion: []
    };
  }

  /**
   * 连接WebSocket
   */
  connect() {
    // 防止重复连接
    if (this.isConnecting) {
      console.log('WebSocket正在连接中，跳过重复连接');
      return;
    }

    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
      console.log('WebSocket已连接或正在连接');
      return;
    }

    this.isConnecting = true;

    try {
      console.log(`尝试连接WebSocket: ${this.url}`);
      this.ws = new WebSocket(this.url);

      this.ws.onopen = (event) => {
        console.log('WebSocket连接已建立');
        this.isConnected = true;
        this.isConnecting = false;
        this.reconnectAttempts = 0;
        this.shouldReconnect = true; // 连接成功后恢复重连能力
        this._notifyListeners('open', event);
      };

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this._notifyListeners('message', data);

        // 处理补全消息（包括错误消息）
        if (data.type === 'token' || data.type === 'start' || data.type === 'end' || data.type === 'error') {
          this._notifyListeners('completion', data);
        }
      };

      this.ws.onclose = (event) => {
        console.log('WebSocket连接关闭', { code: event.code, reason: event.reason });
        this.isConnected = false;
        this.isConnecting = false;
        this._notifyListeners('close', event);
        
        // 只在应该重连且不是主动关闭时才重连
        if (this.shouldReconnect && event.code !== 1000) {
          this._attemptReconnect();
        }
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket错误:', error);
        this.isConnecting = false;
        this._notifyListeners('error', error);
      };
    } catch (error) {
      console.error('WebSocket连接失败:', error);
      this.isConnecting = false;
      if (this.shouldReconnect) {
        this._attemptReconnect();
      }
    }
  }

  /**
   * 尝试重新连接
   */
  _attemptReconnect() {
    // 检查是否应该重连
    if (!this.shouldReconnect) {
      console.log('已禁用重连，停止重连尝试');
      return;
    }

    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.log(`达到最大重连次数(${this.maxReconnectAttempts})，停止重连`);
      this.shouldReconnect = false; // 停止后续重连
      return;
    }

    if (this.isConnecting) {
      console.log('正在连接中，跳过重连');
      return;
    }

    this.reconnectAttempts++;
    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 10000); // 最大延迟10秒
    
    console.log(`第${this.reconnectAttempts}次重连，${delay}ms后尝试`);
    
    clearTimeout(this.reconnectTimeout);
    this.reconnectTimeout = setTimeout(() => {
      if (this.shouldReconnect && !this.isConnected) {
        this.connect();
      }
    }, delay);
  }

  /**
   * 发送消息
   * @param {Object} data - 要发送的数据
   */
  send(data) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      console.warn('WebSocket未连接，无法发送消息');
      return false;
    }

    // 添加请求限流检查
    const now = Date.now();
    if (now - this.lastRequestTime < this.requestThrottleDelay) {
      console.log(`请求过于频繁，跳过发送 (${now - this.lastRequestTime}ms < ${this.requestThrottleDelay}ms)`);
      return false;
    }

    try {
      this.ws.send(JSON.stringify(data));
      this.lastRequestTime = now;
      return true;
    } catch (error) {
      console.error('发送消息失败:', error);
      return false;
    }
  }

  /**
   * 关闭连接
   */
  disconnect() {
    console.log('主动断开WebSocket连接');
    this.shouldReconnect = false; // 主动断开时禁用重连
    
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }
    
    if (this.ws) {
      // 使用正常关闭代码
      this.ws.close(1000, '用户主动断开');
      this.ws = null;
    }
    
    this.isConnected = false;
    this.isConnecting = false;
    this.reconnectAttempts = 0;
  }

  /**
   * 重置重连状态（用于手动重连）
   */
  resetReconnect() {
    this.shouldReconnect = true;
    this.reconnectAttempts = 0;
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }
  }

  /**
   * 获取连接状态
   */
  getConnectionState() {
    return {
      isConnected: this.isConnected,
      isConnecting: this.isConnecting,
      reconnectAttempts: this.reconnectAttempts,
      shouldReconnect: this.shouldReconnect
    };
  }

  /**
   * 添加事件监听器
   * @param {string} event - 事件名称 (open, message, close, error, completion)
   * @param {Function} callback - 回调函数
   */
  on(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event].push(callback);
    }
  }

  /**
   * 移除事件监听器
   * @param {string} event - 事件名称
   * @param {Function} callback - 要移除的回调函数
   */
  off(event, callback) {
    if (this.listeners[event]) {
      this.listeners[event] = this.listeners[event].filter(cb => cb !== callback);
    }
  }

  /**
   * 通知所有监听器
   * @param {string} event - 事件名称
   * @param {any} data - 事件数据
   */
  _notifyListeners(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach(callback => {
        try {
          callback(data);
        } catch (error) {
          console.error(`执行 ${event} 监听器时出错:`, error);
        }
      });
    }
  }

  /**
   * 请求文本补全
   * @param {string} text - 当前文本
   * @param {string} contextBefore - 上文
   * @param {string} contextAfter - 下文
   * @param {number} cursorPosition - 光标位置
   */
  requestCompletion(text, contextBefore = null, contextAfter = null, cursorPosition = null) {
    return this.send({
      text,
      context_before: contextBefore,
      context_after: contextAfter,
      cursor_position: cursorPosition,
      max_tokens: 50,
      temperature: 0.7,
      action: 'completion'
    });
  }
  
  /**
   * 请求文本改写
   * @param {string} text - 要改写的文本
   */
  requestRewrite(text) {
    return this.send({
      text,
      action: 'rewrite',
      temperature: 0.5
    });
  }
  
  /**
   * 请求文本扩写
   * @param {string} text - 要扩写的文本
   */
  requestExpand(text) {
    return this.send({
      text,
      action: 'expand',
      temperature: 0.8
    });
  }
  
  /**
   * 请求文本简化
   * @param {string} text - 要简化的文本
   */
  requestSimplify(text) {
    return this.send({
      text,
      action: 'simplify',
      temperature: 0.5
    });
  }
}

export default WebSocketService;