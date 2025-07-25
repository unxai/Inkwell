<template>
  <div :class="['flex items-center justify-center', fullScreen ? 'fixed inset-0 bg-gray-900/50 z-50' : '']">
    <div class="flex flex-col items-center">
      <svg
        class="animate-spin"
        :class="sizeClasses"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          :stroke="color"
          stroke-width="4"
        ></circle>
        <path
          class="opacity-75"
          :fill="color"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        ></path>
      </svg>
      <span v-if="text" class="mt-2 text-sm font-medium" :class="textColorClass">{{ text }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg', 'xl'].includes(value)
  },
  color: {
    type: String,
    default: 'currentColor'
  },
  text: {
    type: String,
    default: ''
  },
  fullScreen: {
    type: Boolean,
    default: false
  }
});

const sizeClasses = computed(() => {
  const sizes = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
    xl: 'h-16 w-16'
  };
  return sizes[props.size];
});

const textColorClass = computed(() => {
  if (props.color === 'currentColor') return '';
  if (props.color.startsWith('#')) return '';
  
  // 从颜色名称提取类名
  const colorMatch = props.color.match(/^(text-|bg-|border-)?([a-z]+-[0-9]+)$/);
  if (colorMatch) {
    return `text-${colorMatch[2]}`;
  }
  
  return '';
});
</script>