<template>
  <div class="text-editor h-full">
    
    <!-- 编辑器内容区 -->
    <div class="editor-content-wrapper relative h-full w-full paper-effect" ref="editorContainer">
      <editor-content :editor="editor" class="editor-content prose max-w-none h-full" />
      
      <!-- AI建议控制面板 - 只在浮动工具条操作时显示 -->
      <div 
        v-if="showFloatingToolbarSuggestion && suggestionText"
        :style="getControlsPosition()"
        class="ai-suggestion-controls bg-white rounded-lg shadow-lg border p-2"
      >
        <!-- 建议内容显示区域 -->
        <div class="flex items-start space-x-2 mb-2">
          <svg class="w-3 h-3 text-blue-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
          </svg>
          <div class="flex-1">
            <div class="text-xs text-gray-500 mb-1">AI建议</div>
            <div class="text-sm text-gray-700 leading-relaxed max-w-xs">{{ suggestionText }}</div>
          </div>
        </div>
        
        <!-- 控制按钮 -->
        <div class="flex items-center justify-end space-x-2">
          <button 
            @click="applySuggestion"
            class="px-2 py-1 bg-blue-500 text-white text-xs rounded hover:bg-blue-600 transition-colors"
            title="应用建议 (Tab)"
          >
            应用
          </button>
          <button 
            @click="rejectSuggestion"
            class="px-2 py-1 bg-gray-200 text-gray-600 text-xs rounded hover:bg-gray-300 transition-colors"
            title="取消建议 (Esc)"
          >
            取消
          </button>
        </div>
      </div>
      
      
      <!-- AI操作提示指示器 -->
      <div 
        v-if="aiStatus === 'processing'" 
        class="absolute bottom-4 right-4 bg-white bg-opacity-90 rounded-full shadow-md p-2 flex items-center space-x-2 text-sm text-gray-600 border border-gray-200"
      >
        <div class="flex items-center space-x-2">
          <svg class="animate-spin h-4 w-4 text-[#4FD1C5]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <span>AI 思考中...</span>
        </div>
      </div>
      
      <!-- 自动完成提示 -->
      <div 
        v-if="showSuggestion && suggestionText && !showFloatingToolbarSuggestion"
        class="absolute bottom-4 left-4 bg-white bg-opacity-90 rounded-lg shadow-md p-2 flex items-center space-x-2 text-xs text-gray-600 border border-gray-200"
      >
        <svg class="w-3 h-3 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
        </svg>
        <span>按 <kbd class="px-1 py-0.5 text-xs font-semibold text-gray-800 bg-gray-100 border border-gray-300 rounded">Tab</kbd> 应用建议，<kbd class="px-1 py-0.5 text-xs font-semibold text-gray-800 bg-gray-100 border border-gray-300 rounded">Esc</kbd> 取消</span>
      </div>
    </div>
    
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import Placeholder from '@tiptap/extension-placeholder'
import Highlight from '@tiptap/extension-highlight'
import { useEditorStore } from '@/store/modules/editor'
import { Extension } from '@tiptap/core'
import { Plugin, PluginKey } from 'prosemirror-state'
import { Decoration, DecorationSet } from 'prosemirror-view'

const props = defineProps({
  initialContent: {
    type: String,
    default: '<p>欢迎使用墨井智能写作助手！</p>'
  },
  autoCompleteEnabled: {
    type: Boolean,
    default: true
  },
  isConnected: {
    type: Boolean,
    default: false
  },
  references: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits([
  'update:content',
  'text-change',
  'completion-accepted',
  'completion-rejected',
  'selection-change',
  'show-floating-toolbar',
  'hide-floating-toolbar',
  'request-completion'
])

// 使用编辑器状态管理
const editorStore = useEditorStore()
const wordCount = ref(0)
const aiStatus = ref('idle')
// 文本选择状态
const selectedText = ref('')
const selectionRange = ref({ from: 0, to: 0 })

// 编辑时间
const editingTime = ref(0)
let editingTimer = null

// 自动完成相关状态
const editorContainer = ref(null)
const showSuggestion = ref(false)
const showFloatingToolbarSuggestion = ref(false) // 浮动工具条触发的建议
const suggestionText = ref('')
const suggestionPosition = ref({ top: 0, left: 0 })
const currentCursorPosition = ref(0)
const typingTimer = ref(null) // 用户输入定时器
const showToolbarTimeout = ref(null) // 浮动工具条显示延迟定时器
const typingDelay = 1000 // 光标停留触发时间(毫秒)
const lastCompletionTime = ref(0) // 上次请求补全的时间
const completionCooldown = 3000 // 补全请求冷却时间(毫秒)
const cursorIdleTimer = ref(null) // 光标停留定时器
const suggestionPluginKey = new PluginKey('suggestion')

// 待替换内容
const pendingReplacement = ref(null)

// 创建建议显示扩展
const SuggestionExtension = Extension.create({
  name: 'suggestion',
  
  addProseMirrorPlugins() {
    return [
      new Plugin({
        key: suggestionPluginKey,
        state: {
          init() {
            return {
              suggestion: '',
              position: 0,
              show: false
            }
          },
          apply(tr, oldState) {
            const meta = tr.getMeta(suggestionPluginKey)
            if (meta) {
              return { ...oldState, ...meta }
            }
            return oldState
          }
        },
        props: {
          decorations(state) {
            const pluginState = suggestionPluginKey.getState(state)
            if (!pluginState.show || !pluginState.suggestion) {
              return null
            }
            
            const decorations = []
            const pos = pluginState.position
            const suggestion = pluginState.suggestion
            
            // 创建建议装饰
            const decoration = Decoration.widget(pos, () => {
              const span = document.createElement('span')
              span.className = 'inline-suggestion'
              span.textContent = suggestion
              span.setAttribute('data-suggestion', suggestion)
              return span
            }, {
              side: 1,
              key: 'suggestion'
            })
            
            decorations.push(decoration)
            return DecorationSet.create(state.doc, decorations)
          }
        }
      })
    ]
  }
})

// 显示内联建议
const showInlineSuggestion = (suggestion) => {
  if (!editor.value || !suggestion) return
  
  const { state, dispatch } = editor.value.view
  const { from } = state.selection
  
  // 更新插件状态以显示建议
  const tr = state.tr.setMeta(suggestionPluginKey, {
    suggestion: suggestion,
    position: from,
    show: true
  })
  
  dispatch(tr)
  showSuggestion.value = true
  suggestionText.value = suggestion
}

// 隐藏内联建议
const hideInlineSuggestion = () => {
  if (!editor.value) return
  
  const { state, dispatch } = editor.value.view
  
  // 更新插件状态以隐藏建议
  const tr = state.tr.setMeta(suggestionPluginKey, {
    suggestion: '',
    position: 0,
    show: false
  })
  
  dispatch(tr)
  showSuggestion.value = false
  suggestionText.value = ''
}

// 监听文本选择变化
const handleSelectionUpdate = ({ editor }) => {
  const { state } = editor
  const { selection } = state
  const { from, to } = selection
  
  // 更新选择范围
  selectionRange.value = { from, to }
  
  // 获取选中的文本
  const text = state.doc.textBetween(from, to)
  selectedText.value = text
  
  // 发送选择变化事件
  emit('selection-change', {
    text,
    from,
    to,
    hasSelection: from !== to
  })
  
  // 如果有选中文本，显示浮动工具条
  if (text.trim() && from !== to && text.trim().length >= 2) {
    // 获取选择位置的坐标
    try {
      const startCoords = editor.view.coordsAtPos(from)
      const endCoords = editor.view.coordsAtPos(to)
      const containerRect = editorContainer.value?.getBoundingClientRect()

      if (containerRect) {
        // 计算选中文本的中心位置（相对于视口）
        const selectionCenterX = (startCoords.left + endCoords.left) / 2
        const selectionTop = startCoords.top
        const selectionBottom = Math.max(startCoords.bottom, endCoords.bottom)
        
        // 工具条尺寸
        const toolbarWidth = 350
        const toolbarHeight = 60 // 增加高度以适应按钮
        const margin = 12 // 减少边距，使工具条更贴近选中文本
        
        // 计算工具条位置（相对于视口）
        let left = selectionCenterX - (toolbarWidth / 2)
        let top = selectionTop - toolbarHeight - margin
        
        // 水平边界检查 - 确保工具条不超出视口
        const viewportWidth = window.innerWidth
        const minLeft = 10
        const maxLeft = viewportWidth - toolbarWidth - 10
        
        if (left < minLeft) {
          left = minLeft
        } else if (left > maxLeft) {
          left = maxLeft
        }
        
        // 垂直位置检查 - 如果上方空间不足，显示在选中文本下方
        if (top < 10) {
          top = selectionBottom + margin
        }
        
        // 确保工具条不超出视口底部
        const viewportHeight = window.innerHeight
        if (top + toolbarHeight > viewportHeight - 10) {
          top = viewportHeight - toolbarHeight - 10
        }

        const position = { top, left }

        clearTimeout(showToolbarTimeout.value)
        showToolbarTimeout.value = setTimeout(() => {
          emit('show-floating-toolbar', {
            position,
            selectedText: text,
            selectionRange: { from, to }
          })
        }, 300) // 减少延迟，提升响应速度
      }
    } catch (error) {
      console.warn('无法计算浮动工具条位置:', error)
    }
  } else {
    clearTimeout(showToolbarTimeout.value)
    emit('hide-floating-toolbar')
  }
  
  // 更新光标位置
  currentCursorPosition.value = from
  editorStore.updateCursorPosition(from)
  
  // 如果有建议显示且是自动完成模式，隐藏内联建议
  if (showSuggestion.value && !showFloatingToolbarSuggestion.value) {
    hideInlineSuggestion()
  } else if (showFloatingToolbarSuggestion.value) {
    updateSuggestionPosition()
  }
  
  // 光标位置改变时，重新设置自动完成定时器
  if (props.autoCompleteEnabled && from === to) { // 只有在没有选中文本时才触发自动完成
    // 清除之前的定时器
    if (cursorIdleTimer.value) {
      clearTimeout(cursorIdleTimer.value)
    }
    
    // 设置新的光标空闲定时器
    cursorIdleTimer.value = setTimeout(() => {
      console.log('光标空闲触发自动完成')
      triggerAutoCompletion()
    }, typingDelay)
  }
}

// 初始化编辑器
const editor = useEditor({
  extensions: [
    StarterKit.configure({
      heading: {
        levels: [1, 2, 3]
      }
    }),
    Placeholder.configure({
      placeholder: '开始写作，或输入 / 使用 AI 辅助功能...'
    }),
    Highlight.configure({
      multicolor: true
    }),
    SuggestionExtension
  ],
  content: props.initialContent,
  onUpdate: ({ editor }) => {
    const html = editor.getHTML()
    const text = editor.getText()
    
    // 更新字数统计（中文字符计数）
    wordCount.value = text.replace(/\s+/g, '').length
    
    // 更新状态管理中的内容
    editorStore.updateContent(html)
    
    // 向父组件发送更新事件
    emit('update:content', html)
    emit('text-change', text)
    
    // 保存当前光标位置
    if (editor.state.selection) {
      currentCursorPosition.value = editor.state.selection.from
      editorStore.updateCursorPosition(currentCursorPosition.value)
    }
    
    // 编辑时清除光标空闲定时器，不立即触发自动完成
    if (cursorIdleTimer.value) {
      clearTimeout(cursorIdleTimer.value)
      cursorIdleTimer.value = null
    }
  },
  onSelectionUpdate: handleSelectionUpdate,
  onFocus: () => {
    // 编辑器获得焦点时，开始计时
    if (!editingTimer) {
      editingTimer = setInterval(() => {
        editingTime.value++
      }, 1000)
    }
    
    // 添加键盘事件监听
    document.addEventListener('keydown', handleKeyDown)
  },
  onBlur: () => {
    // 编辑器失去焦点时，停止计时
    if (editingTimer) {
      clearInterval(editingTimer)
      editingTimer = null
    }
    
    // 移除键盘事件监听
    document.removeEventListener('keydown', handleKeyDown)
    
    // 延迟隐藏浮动工具条，给用户时间点击工具条
    setTimeout(() => {
      emit('hide-floating-toolbar')
    }, 150)
  }
})

// 监听AI状态变化
watch(() => editorStore.aiStatus, (newStatus) => {
  aiStatus.value = newStatus
})

// 优化触发自动完成的逻辑
const triggerAutoCompletion = () => {
  if (!editor.value) {
    console.log('❌ 编辑器不存在')
    return
  }
  
  if (aiStatus.value === 'processing') {
    console.log('❌ AI正在处理中')
    return
  }
  
  // 如果当前有建议显示，不触发自动完成
  if (showSuggestion.value || showFloatingToolbarSuggestion.value) {
    console.log('❌ 当前有建议显示中')
    return
  }
  
  const now = Date.now()
  
  
  const { state } = editor.value
  const { from } = state.selection
  const text = editor.value.getText()
  
  // 获取光标前的上下文
  const contextBefore = text.slice(0, from)
  const contextAfter = text.slice(from)
  
  // 基本触发条件：至少有一些文本内容
  if (!contextBefore.trim() || contextBefore.trim().length < 5) {
    console.log('❌ 前文内容不足，实际长度:', contextBefore.trim().length)
    return
  }
  
  // 检查编辑器是否仍然处于活动状态
  if (!editor.value.isFocused) {
    console.log('❌ 编辑器未聚焦')
    return
  }
  
  // 检查当前是否有选中的文本，如果有则不触发自动完成
  if (from !== state.selection.to) {
    console.log('❌ 有文本被选中，from:', from, 'to:', state.selection.to)
    return
  }

  
  // 更新上次请求时间
  lastCompletionTime.value = now
  
  // 请求补全
  emit('request-completion', {
    text: contextBefore,
    contextBefore,
    contextAfter,
    cursorPosition: from
  })
  
}

// 计算控制按钮位置 - 优化为使用视口坐标
const getControlsPosition = () => {
  const controlsWidth = 300
  const controlsHeight = 120 // 增加高度以适应内容
  const margin = 12
  
  // 使用视口坐标进行定位
  let top = suggestionPosition.value.top + margin
  let left = suggestionPosition.value.left - (controlsWidth / 2) // 居中对齐
  
  // 水平边界检查 - 确保不超出视口
  const viewportWidth = window.innerWidth
  if (left < 10) {
    left = 10
  } else if (left + controlsWidth > viewportWidth - 10) {
    left = viewportWidth - controlsWidth - 10
  }
  
  // 垂直边界检查 - 如果下方空间不足，显示在选中文字上方
  const viewportHeight = window.innerHeight
  if (top + controlsHeight > viewportHeight - 10) {
    top = suggestionPosition.value.top - controlsHeight - margin
  }
  
  // 确保不超出视口顶部
  if (top < 10) {
    top = 10
  }
  
  return {
    position: 'fixed', // 使用fixed定位相对于视口
    top: top + 'px',
    left: left + 'px',
    zIndex: 1001
  }
}


// 更新建议位置 - 优化为支持选中文字定位
const updateSuggestionPosition = (useSelection = false) => {
  if (!editor.value) return
  
  try {
    const { from, to } = editor.value.state.selection
    let coords
    
    if (useSelection && from !== to) {
      // 如果有选中文字，使用选中文字的中心位置
      const startCoords = editor.value.view.coordsAtPos(from)
      const endCoords = editor.value.view.coordsAtPos(to)
      coords = {
        top: startCoords.top,
        left: (startCoords.left + endCoords.left) / 2,
        bottom: Math.max(startCoords.bottom, endCoords.bottom)
      }
    } else {
      // 使用光标位置
      coords = editor.value.view.coordsAtPos(from)
    }
    
    // 直接使用视口坐标，不需要相对于容器计算
    suggestionPosition.value = {
      top: coords.top,
      left: coords.left
    }
  } catch (error) {
    console.warn('无法计算建议位置:', error)
  }
}

// 显示建议 - 修改为支持两种显示模式
const showSuggestionText = (suggestion, isFromFloatingToolbar = false) => {
  if (!suggestion || !suggestion.trim() || !editor.value) return
  
  // 如果当前有其他AI操作正在进行，先清理
  if (showSuggestion.value || showFloatingToolbarSuggestion.value) {
    hideSuggestion()
  }
  
  suggestionText.value = suggestion.trim()
  
  if (isFromFloatingToolbar) {
    // 浮动工具条触发的操作显示控制面板，使用选中文字位置
    showFloatingToolbarSuggestion.value = true
    updateSuggestionPosition(true) // 传入true使用选中文字位置
  } else {
    // 自动完成显示为内联建议
    showInlineSuggestion(suggestion.trim())
  }
}

// 隐藏建议
const hideSuggestion = () => {
  showSuggestion.value = false
  showFloatingToolbarSuggestion.value = false
  suggestionText.value = ''
  hideInlineSuggestion()
  // 清理pending replacement，避免冲突
  pendingReplacement.value = null
}

// 应用建议
const applySuggestion = () => {
  if ((!showSuggestion.value && !showFloatingToolbarSuggestion.value) || !suggestionText.value || !editor.value) return
  
  // 如果有pending replacement，则执行替换操作
  if (pendingReplacement.value) {
    const { from, to, newText } = pendingReplacement.value
    // 选中原文本并替换
    editor.value.chain()
      .focus()
      .setTextSelection({ from, to })
      .deleteSelection()
      .insertContent(newText)
      .run()
    
    // 清除pending replacement
    pendingReplacement.value = null
  } else {
    // 普通插入操作
    editor.value.chain().focus().insertContent(suggestionText.value).run()
  }
  
  // 清除建议
  hideSuggestion()
  
  // 清除所有相关的定时器
  if (typingTimer.value) {
    clearTimeout(typingTimer.value)
    typingTimer.value = null
  }
  
  if (cursorIdleTimer.value) {
    clearTimeout(cursorIdleTimer.value)
    cursorIdleTimer.value = null
  }
  
  // 设置更长的冷却时间，避免应用后立即再次触发
  lastCompletionTime.value = Date.now()
  
  // 自动完成应用后，点击页面外的位置取消光标焦点
  setTimeout(() => {
    if (editor.value) {
      // 让编辑器失去焦点
      editor.value.commands.blur()
      // 创建一个临时的不可见元素并让它获得焦点
      const tempElement = document.createElement('input')
      tempElement.style.position = 'absolute'
      tempElement.style.left = '-9999px'
      tempElement.style.opacity = '0'
      document.body.appendChild(tempElement)
      tempElement.focus()
      // 立即移除临时元素
      setTimeout(() => {
        document.body.removeChild(tempElement)
      }, 10)
    }
  }, 100)
  
  // 发送接受事件
  emit('completion-accepted', suggestionText.value)
}

// 拒绝建议
const rejectSuggestion = () => {
  if (!showSuggestion.value && !showFloatingToolbarSuggestion.value) return
  
  // 清除pending replacement
  pendingReplacement.value = null
  
  // 清除建议
  hideSuggestion()
  
  // 取消光标以避免连续生成
  if (typingTimer.value) {
    clearTimeout(typingTimer.value)
    typingTimer.value = null
  }
  
  // 设置冷却时间
  lastCompletionTime.value = Date.now()
  
  emit('completion-rejected')
}

// 处理键盘事件
const handleKeyDown = (event) => {
  if (!editor.value) return
  
  // Tab 键应用建议
  if (event.key === 'Tab' && (showSuggestion.value || showFloatingToolbarSuggestion.value)) {
    event.preventDefault()
    applySuggestion()
    return
  }
  
  // Escape 键拒绝建议
  if (event.key === 'Escape' && (showSuggestion.value || showFloatingToolbarSuggestion.value)) {
    event.preventDefault()
    rejectSuggestion()
    return
  }
  
  // 其他按键隐藏建议
  if ((showSuggestion.value || showFloatingToolbarSuggestion.value) && !['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'].includes(event.key)) {
    hideSuggestion()
  }
}

// 生命周期钩子
onMounted(() => {
  // 可以在这里添加需要的键盘事件监听
})

onBeforeUnmount(() => {
  // 移除键盘事件监听
  document.removeEventListener('keydown', handleKeyDown)
  
  // 清除计时器
  if (editingTimer) {
    clearInterval(editingTimer)
    editingTimer = null
  }
  
  // 清除输入定时器
  if (typingTimer.value) {
    clearTimeout(typingTimer.value)
    typingTimer.value = null
  }
  
  // 清除光标空闲定时器
  if (cursorIdleTimer.value) {
    clearTimeout(cursorIdleTimer.value)
    cursorIdleTimer.value = null
  }
  
  // 清除浮动工具条显示定时器
  if (showToolbarTimeout.value) {
    clearTimeout(showToolbarTimeout.value)
    showToolbarTimeout.value = null
  }
  
  // 销毁编辑器
  if (editor.value) {
    editor.value.destroy()
  }
})

// 暴露编辑器实例和方法，以便父组件可以访问
defineExpose({
  editor,
  currentCursorPosition,
  selectedText,
  selectionRange,
  showSuggestion: showSuggestionText,
  hideSuggestion,
  applySuggestion,
  rejectSuggestion,
  pendingReplacement
})
</script>

<style>
.text-editor {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.editor-content-wrapper {
  flex-grow: 1;
  overflow-y: auto;
  padding: 1rem 1rem; /* 减少内边距，让内容区域更大 */
  background-color: #f9f9f9;
  height: calc(100vh - 180px); /* 调整编辑器高度，确保不会太高 */
}

.paper-effect {
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
  border-radius: 2px;
  max-width: 95%; /* 将编辑器宽度设置为95% */
  margin: 0 auto;
  padding: 40px 60px;
  position: relative;
  min-height: calc(100% - 40px);
}

.paper-effect::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(to right, transparent, rgba(79, 209, 197, 0.3), transparent);
}

.editor-content {
  height: 100%;
  outline: none;
}

/* Tiptap编辑器样式 */
.ProseMirror {
  height: 100%;
  outline: none;
  font-size: 16px;
  line-height: 1.8;
  color: #333;
  font-family: 'Noto Serif SC', serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
  letter-spacing: 0.02em;
  min-height: 400px; /* 调整编辑器的最小高度 */
}

.ProseMirror p {
  margin-bottom: 1.2em;
  text-align: justify;
}

.ProseMirror h1 {
  font-size: 1.8rem;
  font-weight: 600;
  margin-top: 1.8rem;
  margin-bottom: 1.2rem;
  color: #1A365D;
  border-bottom: 1px solid #eaeaea;
  padding-bottom: 0.3rem;
}

.ProseMirror h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: #1A365D;
}

.ProseMirror h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin-top: 1.2rem;
  margin-bottom: 0.8rem;
  color: #1A365D;
}

.ProseMirror ul,
.ProseMirror ol {
  padding-left: 1.5rem;
  margin-bottom: 1em;
}

.ProseMirror ul li {
  list-style-type: disc;
  margin-bottom: 0.25em;
}

.ProseMirror ol li {
  list-style-type: decimal;
  margin-bottom: 0.25em;
}

.ProseMirror blockquote {
  border-left: 3px solid #4FD1C5;
  padding: 0.5rem 1rem;
  color: #4A5568;
  margin: 1.5rem 0;
  font-style: italic;
  background-color: rgba(79, 209, 197, 0.05);
  border-radius: 0 4px 4px 0;
}

.ProseMirror pre {
  background-color: #F7FAFC;
  padding: 1rem;
  border-radius: 0.25rem;
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  margin: 1.5rem 0;
  overflow-x: auto;
  border: 1px solid #edf2f7;
}

.ProseMirror code {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  background-color: #F7FAFC;
  padding: 0.1em 0.3em;
  border-radius: 0.2em;
  font-size: 0.9em;
}

.ProseMirror mark {
  background-color: rgba(79, 209, 197, 0.2);
  padding: 0.1em 0;
}

.ProseMirror a {
  color: #4FD1C5;
  text-decoration: underline;
  text-underline-offset: 2px;
}

.ProseMirror p.is-editor-empty:first-child::before {
  content: attr(data-placeholder);
  float: left;
  color: #adb5bd;
  pointer-events: none;
  height: 0;
}

/* 编辑器滚动条样式 */
.editor-content-wrapper::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.editor-content-wrapper::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.editor-content-wrapper::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

.editor-content-wrapper::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 内联建议文本样式 */
.inline-suggestion {
  color: #9CA3AF;
  background-color: rgba(156, 163, 175, 0.1);
  font-style: italic;
  pointer-events: none;
  user-select: none;
  position: relative;
  border-radius: 2px;
  padding: 0 2px;
  display: inline;
}

.inline-suggestion::after {
  content: '';
  position: absolute;
  right: -2px;
  top: 50%;
  transform: translateY(-50%);
  width: 1px;
  height: 1em;
  background-color: #9CA3AF;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

/* AI建议控制面板样式 */
.ai-suggestion-controls {
  animation: slideInUp 0.2s ease-out;
  backdrop-filter: blur(8px);
  border: 1px solid #e5e7eb;
  box-shadow: 0 10px 25px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  pointer-events: auto; /* 确保可以点击 */
  white-space: nowrap; /* 防止换行 */
  min-width: 250px; /* 设置最小宽度 */
  max-width: 400px; /* 设置最大宽度 */
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

kbd {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
  font-size: 0.75rem;
  font-weight: 600;
}
</style>