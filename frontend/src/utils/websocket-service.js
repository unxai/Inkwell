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
    this.maxReconnectAttempts = 5;
    this.reconnectTimeout = null;
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
    if (this.ws && (this.ws.readyState === WebSocket.OPEN || this.ws.readyState === WebSocket.CONNECTING)) {
      return;
    }

    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = (event) => {
        console.log('WebSocket连接已建立');
        this.isConnected = true;
        this.reconnectAttempts = 0;
        this._notifyListeners('open', event);
      };

      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this._notifyListeners('message', data);

        // 处理补全消息
        if (data.type === 'token' || data.type === 'start' || data.type === 'end') {
          this._notifyListeners('completion', data);
        }
      };

      this.ws.onclose = (event) => {
        console.log('WebSocket连接已关闭');
        this.isConnected = false;
        this._notifyListeners('close', event);
        this._attemptReconnect();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket错误:', error);
        this._notifyListeners('error', error);
      };
    } catch (error) {
      console.error('WebSocket连接失败:', error);
      this._attemptReconnect();
    }
  }

  /**
   * 尝试重新连接
   */
  _attemptReconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      this.reconnectAttempts++;
      const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
      
      console.log(`尝试在 ${delay}ms 后重新连接... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
      
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = setTimeout(() => {
        this.connect();
      }, delay);
    } else {
      console.error('达到最大重连次数，停止重连');
    }
  }

  /**
   * 发送消息
   * @param {Object} data - 要发送的数据
   */
  send(data) {
    if (!this.ws || this.ws.readyState !== WebSocket.OPEN) {
      console.error('WebSocket未连接，无法发送消息');
      return false;
    }

    try {
      this.ws.send(JSON.stringify(data));
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
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
    
    clearTimeout(this.reconnectTimeout);
    this.isConnected = false;
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