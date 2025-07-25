<template>
  <div
    class="pointer-events-auto w-full max-w-sm overflow-hidden rounded-lg bg-white shadow-lg ring-1 ring-black ring-opacity-5"
  >
    <div class="p-4">
      <div class="flex items-start">
        <div class="flex-shrink-0">
          <CheckCircleIcon v-if="type === 'success'" class="h-6 w-6 text-green-400" aria-hidden="true" />
          <ExclamationTriangleIcon v-else-if="type === 'warning'" class="h-6 w-6 text-yellow-400" aria-hidden="true" />
          <XCircleIcon v-else-if="type === 'error'" class="h-6 w-6 text-red-400" aria-hidden="true" />
          <InformationCircleIcon v-else class="h-6 w-6 text-blue-400" aria-hidden="true" />
        </div>
        <div class="ml-3 w-0 flex-1 pt-0.5">
          <p class="text-sm font-medium text-gray-900">{{ title }}</p>
          <p class="mt-1 text-sm text-gray-500">{{ message }}</p>
        </div>
        <div class="ml-4 flex flex-shrink-0">
          <button
            type="button"
            class="inline-flex rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            @click="onClose"
          >
            <span class="sr-only">关闭</span>
            <XMarkIcon class="h-5 w-5" aria-hidden="true" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  CheckCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XCircleIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline';

defineProps({
  type: {
    type: String,
    default: 'info',
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
  },
  title: {
    type: String,
    default: '通知'
  },
  message: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['close']);

const onClose = () => {
  emit('close');
};
</script>