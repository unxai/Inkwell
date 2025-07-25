<template>
  <TransitionRoot appear :show="modelValue" as="template">
    <Dialog as="div" class="relative z-10" @close="$emit('update:modelValue', false)">
      <TransitionChild
        as="template"
        enter="duration-300 ease-out"
        enter-from="opacity-0"
        enter-to="opacity-100"
        leave="duration-200 ease-in"
        leave-from="opacity-100"
        leave-to="opacity-0"
      >
        <div class="fixed inset-0 bg-black bg-opacity-25" />
      </TransitionChild>

      <div class="fixed inset-0 overflow-y-auto">
        <div class="flex min-h-full items-center justify-center p-4 text-center">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <DialogPanel
              class="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
              :class="{ 'max-w-lg': size === 'lg', 'max-w-xl': size === 'xl', 'max-w-2xl': size === '2xl' }"
            >
              <DialogTitle
                as="h3"
                class="text-lg font-medium leading-6 text-gray-900 flex justify-between items-center"
              >
                {{ title }}
                <button
                  v-if="showCloseButton"
                  type="button"
                  class="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none"
                  @click="$emit('update:modelValue', false)"
                >
                  <span class="sr-only">关闭</span>
                  <XMarkIcon class="h-6 w-6" aria-hidden="true" />
                </button>
              </DialogTitle>
              
              <div class="mt-2">
                <slot></slot>
              </div>

              <div v-if="$slots.footer" class="mt-4">
                <slot name="footer"></slot>
              </div>
              <div v-else-if="showDefaultFooter" class="mt-4 flex justify-end space-x-3">
                <button
                  type="button"
                  class="inline-flex justify-center rounded-md border border-transparent bg-gray-100 px-4 py-2 text-sm font-medium text-gray-900 hover:bg-gray-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-gray-500 focus-visible:ring-offset-2"
                  @click="$emit('update:modelValue', false)"
                >
                  {{ cancelText }}
                </button>
                <button
                  type="button"
                  class="inline-flex justify-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                  @click="$emit('confirm')"
                >
                  {{ confirmText }}
                </button>
              </div>
            </DialogPanel>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { Dialog, DialogPanel, DialogTitle, TransitionChild, TransitionRoot } from '@headlessui/vue';
import { XMarkIcon } from '@heroicons/vue/24/outline';

defineProps({
  modelValue: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    default: '对话框'
  },
  showCloseButton: {
    type: Boolean,
    default: true
  },
  showDefaultFooter: {
    type: Boolean,
    default: true
  },
  confirmText: {
    type: String,
    default: '确认'
  },
  cancelText: {
    type: String,
    default: '取消'
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['md', 'lg', 'xl', '2xl'].includes(value)
  }
});

defineEmits(['update:modelValue', 'confirm']);
</script>