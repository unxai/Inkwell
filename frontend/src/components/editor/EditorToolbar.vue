<template>
  <div class="editor-toolbar bg-white border-b border-gray-200 p-1.5 flex flex-wrap items-center gap-1 justify-center">
    <!-- 文本格式化工具 -->
    <button
      @click="editor.chain().focus().toggleBold().run()"
      :class="{ 'is-active': editor.isActive('bold') }"
      class="toolbar-btn"
      title="加粗 (Ctrl+B)"
      @mouseenter="debouncedShowTooltip($event, '加粗 (Ctrl+B)')"
      @mouseleave="hideTooltip"
    >
      <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M6 4h8a4 4 0 0 1 4 4 4 4 0 0 1-4 4H6z"></path>
        <path d="M6 12h9a4 4 0 0 1 4 4 4 4 0 0 1-4 4H6z"></path>
      </svg>
    </button>
    
    <button
      @click="editor.chain().focus().toggleItalic().run()"
      :class="{ 'is-active': editor.isActive('italic') }"
      class="toolbar-btn"
      title="斜体 (Ctrl+I)"
      @mouseenter="debouncedShowTooltip($event, '斜体 (Ctrl+I)')"
      @mouseleave="hideTooltip"
    >
      <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="19" y1="4" x2="10" y2="4"></line>
        <line x1="14" y1="20" x2="5" y2="20"></line>
        <line x1="15" y1="4" x2="9" y2="20"></line>
      </svg>
    </button>
    
    <button
      @click="editor.chain().focus().toggleStrike().run()"
      :class="{ 'is-active': editor.isActive('strike') }"
      class="toolbar-btn"
      title="删除线"
      @mouseenter="debouncedShowTooltip($event, '删除线')"
      @mouseleave="hideTooltip"
    >
      <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="5" y1="12" x2="19" y2="12"></line>
        <path d="M16 6C16 6 16 6 16 6C16 6 15 5 12 5C9 5 7 7 7 9C7 11 9 12 12 12C15 12 17 13 17 15C17 17 15 19 12 19C9 19 8 18 8 18"></path>
      </svg>
    </button>
    
    <button
      @click="editor.chain().focus().toggleHighlight().run()"
      :class="{ 'is-active': editor.isActive('highlight') }"
      class="toolbar-btn"
      title="高亮"
      @mouseenter="debouncedShowTooltip($event, '高亮')"
      @mouseleave="hideTooltip"
    >
      <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
        <path d="M2 17l10 5 10-5"></path>
        <path d="M2 12l10 5 10-5"></path>
      </svg>
    </button>
    
    <div class="h-5 w-px bg-gray-300 mx-1"></div>
    
    <!-- 标题工具 -->
    <div class="relative group">
      <button
        @click="showHeadingMenu = !showHeadingMenu"
        class="toolbar-btn flex items-center"
        title="标题"
        @mouseenter="debouncedShowTooltip($event, '标题')"
        @mouseleave="hideTooltip"
      >
        <span class="mr-1">标题</span>
        <svg class="w-3 h-3" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="6 9 12 15 18 9"></polyline>
        </svg>
      </button>
      
      <div 
        v-show="showHeadingMenu" 
        class="absolute top-full left-0 mt-1 bg-white border border-gray-200 rounded-md shadow-lg z-10 py-1 min-w-[100px]"
      >
        <button
          @click="editor.chain().focus().toggleHeading({ level: 1 }).run(); showHeadingMenu = false"
          :class="{ 'bg-gray-100': editor.isActive('heading', { level: 1 }) }"
          class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
        >
          一级标题 (Alt+1)
        </button>
        <button
          @click="editor.chain().focus().toggleHeading({ level: 2 }).run(); showHeadingMenu = false"
          :class="{ 'bg-gray-100': editor.isActive('heading', { level: 2 }) }"
          class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
        >
          二级标题 (Alt+2)
        </button>
        <button
          @click="editor.chain().focus().toggleHeading({ level: 3 }).run(); showHeadingMenu = false"
          :class="{ 'bg-gray-100': editor.isActive('heading', { level: 3 }) }"
          class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
        >
          三级标题 (Alt+3)
        </button>
        <button
          @click="editor.chain().focus().setParagraph().run(); showHeadingMenu = false"
          :class="{ 'bg-gray-100': editor.isActive('paragraph') }"
          class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
        >
          正文
        </button>
      </div>
    </div>
    
    <!-- 列表工具 -->
    <button
      @click="editor.chain().focus().toggleBulletList().run()"
      :class="{ 'is-active': editor.isActive('bulletList') }"
      class="toolbar-btn"
      title="无序列表"
      @mouseenter="debouncedShowTooltip($event, '无序列表')"
      @mouseleave="hideTooltip"
    >
      <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="8" y1="6" x2="21" y2="6"></line>
        <line x1="8" y1="12" x2="21" y2="12"></line>
        <line x1="8" y1="18" x2="21" y2="18"></line>
        <line x1="3" y1="6" x2="3.01" y2="6"></line>
        <line x1="3" y1="12" x2="3.01" y2="12"></line>
        <line x1="3" y1="18" x2="3.01" y2="18"></line>
      </svg>
    </button>
    
    <button
      @click="editor.chain().focus().toggleOrderedList().run()"
      :class="{ 'is-active': editor.isActive('orderedList') }"
      class="toolbar-btn"
      title="有序列表"
      @mouseenter="debouncedShowTooltip($event, '有序列表')"
      @mouseleave="hideTooltip"
    >
      <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <line x1="10" y1="6" x2="21" y2="6"></line>
        <line x1="10" y1="12" x2="21" y2="12"></line>
        <line x1="10" y1="18" x2="21" y2="18"></line>
        <path d="M4 6h1v4"></path>
        <path d="M4 10h2"></path>
        <path d="M6 18H4c0-1 2-2 2-3s-1-1.5-2-1"></path>
      </svg>
    </button>
    
    <div class="h-5 w-px bg-gray-300 mx-1"></div>
    
    <!-- 引用和代码块 -->
    <button
      @click="editor.chain().focus().toggleBlockquote().run()"
      :class="{ 'is-active': editor.isActive('blockquote') }"
      class="toolbar-btn"
      title="引用"
      @mouseenter="debouncedShowTooltip($event, '引用')"
      @mouseleave="hideTooltip"
    >
      <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 21c3 0 7-1 7-8V5c0-1.25-.756-2.017-2-2H4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2 1 0 1 0 1 1v1c0 1-1 2-2 2s-1 .008-1 1.031V20c0 1 0 1 1 1z"></path>
        <path d="M15 21c3 0 7-1 7-8V5c0-1.25-.757-2.017-2-2h-4c-1.25 0-2 .75-2 1.972V11c0 1.25.75 2 2 2h.75c0 2.25.25 4-2.75 4v3c0 1 0 1 1 1z"></path>
      </svg>
    </button>
    
    <button
      @click="editor.chain().focus().toggleCodeBlock().run()"
      :class="{ 'is-active': editor.isActive('codeBlock') }"
      class="toolbar-btn"
      title="代码块"
      @mouseenter="debouncedShowTooltip($event, '代码块')"
      @mouseleave="hideTooltip"
    >
      <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="16 18 22 12 16 6"></polyline>
        <polyline points="8 6 2 12 8 18"></polyline>
      </svg>
    </button>
    
    <div class="h-5 w-px bg-gray-300 mx-1"></div>
    
    <!-- 撤销和重做 -->
    <button
      @click="editor.chain().focus().undo().run()"
      :disabled="!editor.can().undo()"
      class="toolbar-btn"
      :class="{ 'opacity-50 cursor-not-allowed': !editor.can().undo() }"
      title="撤销 (Ctrl+Z)"
      @mouseenter="debouncedShowTooltip($event, '撤销 (Ctrl+Z)')"
      @mouseleave="hideTooltip"
    >
      <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 7v6h6"></path>
        <path d="M3 13c0-4.97 4.03-9 9-9a9 9 0 0 1 9 9 9 9 0 0 1-9 9 9 9 0 0 1-6-2.3L3 17"></path>
      </svg>
    </button>
    
    <button
      @click="editor.chain().focus().redo().run()"
      :disabled="!editor.can().redo()"
      class="toolbar-btn"
      :class="{ 'opacity-50 cursor-not-allowed': !editor.can().redo() }"
      title="重做 (Ctrl+Shift+Z)"
      @mouseenter="debouncedShowTooltip($event, '重做 (Ctrl+Shift+Z)')"
      @mouseleave="hideTooltip"
    >
      <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 7v6h-6"></path>
        <path d="M21 13c0-4.97-4.03-9-9-9a9 9 0 0 0-9 9 9 9 0 0 0 9 9 9 9 0 0 0 6-2.3l3 2.3"></path>
      </svg>
    </button>
    
    <div class="h-5 w-px bg-gray-300 mx-1"></div>
    
    <!-- 清除格式 -->
    <button
      @click="editor.chain().focus().clearNodes().unsetAllMarks().run()"
      class="toolbar-btn"
      title="清除格式"
      @mouseenter="debouncedShowTooltip($event, '清除格式')"
      @mouseleave="hideTooltip"
    >
      <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 20h9"></path>
        <path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
        <line x1="15" y1="9" x2="18" y2="12"></line>
      </svg>
    </button>
    
    <!-- 工具提示 -->
    <transition name="tooltip">
      <div 
        v-if="tooltipVisible" 
        class="absolute bg-gray-800 text-white text-xs rounded py-1 px-2 z-50 pointer-events-none"
        :style="{
          left: `${tooltipPosition.x}px`,
          top: `${tooltipPosition.y}px`,
          transform: 'translateX(-50%)'
        }"
      >
        {{ tooltipText }}
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'

defineProps({
  editor: {
    type: Object,
    required: true
  }
})

const showHeadingMenu = ref(false)
const tooltipVisible = ref(false)
const tooltipText = ref('')
const tooltipPosition = ref({ x: 0, y: 0 })

// 点击外部关闭标题菜单
const handleClickOutside = (event) => {
  const isClickOutside = !event.target.closest('.toolbar-btn')
  if (isClickOutside && showHeadingMenu.value) {
    showHeadingMenu.value = false
  }
}

// 处理键盘快捷键
const handleKeyDown = (event) => {
  // 如果用户正在输入，不处理快捷键
  if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
    return
  }
  
  // 常用快捷键
  if (event.ctrlKey || event.metaKey) {
    switch (event.key.toLowerCase()) {
      case 'b':
        if (!event.shiftKey && !event.altKey) {
          event.preventDefault()
          editor.chain().focus().toggleBold().run()
        }
        break
      case 'i':
        if (!event.shiftKey && !event.altKey) {
          event.preventDefault()
          editor.chain().focus().toggleItalic().run()
        }
        break
      case 'u':
        if (!event.shiftKey && !event.altKey) {
          event.preventDefault()
          editor.chain().focus().toggleUnderline().run()
        }
        break
    }
  }
  
  // Alt + 数字键快捷键
  if (event.altKey && !event.ctrlKey && !event.metaKey && !event.shiftKey) {
    switch (event.key) {
      case '1':
        event.preventDefault()
        editor.chain().focus().toggleHeading({ level: 1 }).run()
        break
      case '2':
        event.preventDefault()
        editor.chain().focus().toggleHeading({ level: 2 }).run()
        break
      case '3':
        event.preventDefault()
        editor.chain().focus().toggleHeading({ level: 3 }).run()
        break
    }
  }
}

// 显示工具提示
const showTooltip = (event, text) => {
  // 获取按钮位置
  if (event && event.currentTarget) {
    const rect = event.currentTarget.getBoundingClientRect()
    
    tooltipText.value = text
    tooltipPosition.value = {
      x: rect.left + rect.width / 2,
      y: rect.bottom + 5
    }
    
    tooltipVisible.value = true
  }
}

// 隐藏工具提示
const hideTooltip = () => {
  tooltipVisible.value = false
}

// 防抖函数
const debounce = (fn, delay) => {
  let timer = null
  return function(...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

// 防抖处理的工具提示显示
const debouncedShowTooltip = debounce(showTooltip, 300)

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeyDown)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped>
.editor-toolbar {
  @apply sticky top-0 z-10;
}

.toolbar-btn {
  @apply p-1.5 rounded text-sm text-gray-700 hover:bg-gray-100 transition-colors focus:outline-none focus:ring-1 focus:ring-[#4FD1C5];
  position: relative;
}

.toolbar-btn.is-active {
  @apply bg-gray-100 text-[#1A365D];
}

.toolbar-btn:disabled {
  @apply cursor-not-allowed opacity-50;
}

/* 移动端适配 */
@media (max-width: 640px) {
  .editor-toolbar {
    @apply justify-center;
  }
  
  .toolbar-btn {
    @apply p-1;
  }
}

/* 工具提示动画 */
.tooltip-enter-active,
.tooltip-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.tooltip-enter-from,
.tooltip-leave-to {
  opacity: 0;
  transform: translateY(-5px) translateX(-50%);
}
</style>