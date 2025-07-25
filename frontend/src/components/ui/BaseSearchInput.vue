<template>
  <div class="relative">
    <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
      <MagnifyingGlassIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
    </div>
    <input
      type="text"
      :placeholder="placeholder"
      :value="modelValue"
      @input="handleInput"
      class="block w-full rounded-md border-0 py-1.5 pl-10 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6"
    />
    <button
      v-if="modelValue"
      type="button"
      class="absolute inset-y-0 right-0 flex items-center pr-3"
      @click="clearInput"
    >
      <XMarkIcon class="h-5 w-5 text-gray-400 hover:text-gray-500" aria-hidden="true" />
    </button>
  </div>
</template>

<script setup>
import { MagnifyingGlassIcon, XMarkIcon } from '@heroicons/vue/20/solid';
import { debounce } from 'lodash';
import { onMounted, onUnmounted } from 'vue';

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '搜索...'
  },
  debounceTime: {
    type: Number,
    default: 300
  }
});

const emit = defineEmits(['update:modelValue', 'search']);

// 创建一个防抖函数
const debouncedEmit = debounce((value) => {
  emit('search', value);
}, props.debounceTime);

// 处理输入
const handleInput = (event) => {
  const value = event.target.value;
  emit('update:modelValue', value);
  debouncedEmit(value);
};

// 清除输入
const clearInput = () => {
  emit('update:modelValue', '');
  emit('search', '');
};

// 组件卸载时取消未执行的防抖函数
onUnmounted(() => {
  debouncedEmit.cancel();
});
</script>