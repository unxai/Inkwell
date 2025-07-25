import { debounce } from 'lodash';

/**
 * 创建一个防抖函数，用于限制函数的执行频率
 * @param {Function} fn 需要防抖的函数
 * @param {Number} wait 等待时间（毫秒）
 * @param {Object} options 选项对象
 * @param {Boolean} options.leading 是否在延迟开始前调用函数
 * @param {Boolean} options.trailing 是否在延迟结束后调用函数
 * @param {Number} options.maxWait 最大等待时间
 * @returns {Function} 防抖后的函数
 */
export const createDebouncedFunction = (fn, wait = 300, options = {}) => {
  return debounce(fn, wait, options);
};

/**
 * 创建一个用于搜索的防抖函数
 * @param {Function} searchFn 搜索函数
 * @param {Number} wait 等待时间（毫秒）
 * @returns {Function} 防抖后的搜索函数
 */
export const createDebouncedSearch = (searchFn, wait = 300) => {
  return debounce(searchFn, wait);
};

/**
 * 创建一个用于表单输入的防抖函数
 * @param {Function} inputHandler 输入处理函数
 * @param {Number} wait 等待时间（毫秒）
 * @returns {Function} 防抖后的输入处理函数
 */
export const createDebouncedInput = (inputHandler, wait = 300) => {
  return debounce(inputHandler, wait);
};

/**
 * 创建一个用于窗口调整大小的防抖函数
 * @param {Function} resizeHandler 调整大小处理函数
 * @param {Number} wait 等待时间（毫秒）
 * @returns {Function} 防抖后的调整大小处理函数
 */
export const createDebouncedResize = (resizeHandler, wait = 200) => {
  return debounce(resizeHandler, wait);
};

/**
 * 创建一个用于滚动事件的防抖函数
 * @param {Function} scrollHandler 滚动处理函数
 * @param {Number} wait 等待时间（毫秒）
 * @returns {Function} 防抖后的滚动处理函数
 */
export const createDebouncedScroll = (scrollHandler, wait = 100) => {
  return debounce(scrollHandler, wait);
};