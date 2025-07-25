/**
 * API服务
 * 用于处理与后端API的交互
 */
import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
});

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 可以在这里添加认证信息等
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response.data;
  },
  error => {
    // 错误处理
    console.error('API请求错误:', error);
    
    // 显示错误提示
    if (window.$message) {
      window.$message.error(error.response?.data?.detail || '请求失败，请稍后重试');
    }
    
    return Promise.reject(error);
  }
);

export default api;