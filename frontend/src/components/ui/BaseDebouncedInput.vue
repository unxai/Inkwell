<template>
  <div>
    <label v-if="label" :for="id" class="block text-sm font-medium text-gray-700 mb-1">{{ label }}</label>
    <div class="relative rounded-md shadow-sm">
      <div v-if="icon" class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
        <component :is="icon" class="h-5 w-5 text-gray-400" aria-hidden="true" />
      </div>
      <input
        :id="id"
        :type="type"
        :value="modelValue"
        @input="handleInput"
        :placeholder="placeholder"
        :class="[
          'block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-blue-600 sm:text-sm sm:leading-6',
          icon ? 'pl-10' : 'pl-3',
          error ? 'ring-red-500 focus:ring-red-500' : ''
        ]"
        :disabled="disabled"
      />
    </div>
    <p v-if="error" class="mt-1 text-sm text-red-600">{{ error }}</p>
    <p v-else-if="hint" class="mt-1 text-sm text-gray-500">{{ hint }}</p>
  </div>
</template>

<script setup>
import { debounce } from 'lodash';
import { onMounted, onUnmounted } from 'vue';

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'text'
  },
  debounceTime: {
    type: Number,
    default: 300
  },
  icon: {
    type: [Object, Function],
    default: null
  },
  id: {
    type: String,
    default: () => `input-${Math.random().toString(36).substring(2, 9)}`
  },
  error: {
    type: String,
    default: ''
  },
  hint: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['update:modelValue', 'change']);

// 创建一个防抖函数
const debouncedEmit = debounce((value) => {
  emit('change', value);
}, props.debounceTime);

// 处理输入
const handleInput = (event) => {
  const value = event.target.value;
  emit('update:modelValue', value);
  debouncedEmit(value);
};

// 组件卸载时取消未执行的防抖函数
onUnmounted(() => {
  debouncedEmit.cancel();
});
</script>