import { toast } from 'vue3-toastify';

/**
 * 显示成功提示
 * @param {string} message - 提示消息
 * @param {object} options - 配置选项
 */
export const showSuccess = (message, options = {}) => {
  toast.success(message, {
    autoClose: 3000,
    position: toast.POSITION.TOP_RIGHT,
    ...options
  });
};

/**
 * 显示错误提示
 * @param {string} message - 提示消息
 * @param {object} options - 配置选项
 */
export const showError = (message, options = {}) => {
  toast.error(message, {
    autoClose: 3000,
    position: toast.POSITION.TOP_RIGHT,
    ...options
  });
};

/**
 * 显示警告提示
 * @param {string} message - 提示消息
 * @param {object} options - 配置选项
 */
export const showWarning = (message, options = {}) => {
  toast.warning(message, {
    autoClose: 3000,
    position: toast.POSITION.TOP_RIGHT,
    ...options
  });
};

/**
 * 显示信息提示
 * @param {string} message - 提示消息
 * @param {object} options - 配置选项
 */
export const showInfo = (message, options = {}) => {
  toast.info(message, {
    autoClose: 3000,
    position: toast.POSITION.TOP_RIGHT,
    ...options
  });
};