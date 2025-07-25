<template>
  <Listbox as="div" v-model="selectedValue">
    <div class="relative mt-1">
      <ListboxButton
        class="relative w-full cursor-default rounded-md bg-white py-1.5 pl-3 pr-10 text-left text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-600 sm:text-sm sm:leading-6"
      >
        <span class="block truncate">{{ selectedValue ? selectedValue[labelKey] : placeholder }}</span>
        <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
          <ChevronUpDownIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
        </span>
      </ListboxButton>

      <transition
        leave-active-class="transition ease-in duration-100"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <ListboxOptions
          class="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
        >
          <ListboxOption
            v-for="option in options"
            :key="option[valueKey]"
            :value="option"
            v-slot="{ active, selected }"
            as="template"
          >
            <li
              :class="[
                active ? 'bg-blue-600 text-white' : 'text-gray-900',
                'relative cursor-default select-none py-2 pl-3 pr-9'
              ]"
            >
              <span :class="[selected ? 'font-semibold' : 'font-normal', 'block truncate']">
                {{ option[labelKey] }}
              </span>

              <span
                v-if="selected"
                :class="[
                  active ? 'text-white' : 'text-blue-600',
                  'absolute inset-y-0 right-0 flex items-center pr-4'
                ]"
              >
                <CheckIcon class="h-5 w-5" aria-hidden="true" />
              </span>
            </li>
          </ListboxOption>
        </ListboxOptions>
      </transition>
    </div>
  </Listbox>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import { Listbox, ListboxButton, ListboxOptions, ListboxOption } from '@headlessui/vue';
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/vue/20/solid';

const props = defineProps({
  modelValue: {
    type: [Object, String, Number],
    default: null
  },
  options: {
    type: Array,
    required: true
  },
  valueKey: {
    type: String,
    default: 'id'
  },
  labelKey: {
    type: String,
    default: 'name'
  },
  placeholder: {
    type: String,
    default: '请选择'
  }
});

const emit = defineEmits(['update:modelValue', 'change']);

// 计算当前选中的值
const selectedValue = computed({
  get() {
    if (!props.modelValue) return null;
    
    // 如果modelValue是对象，直接返回
    if (typeof props.modelValue === 'object') {
      return props.modelValue;
    }
    
    // 否则在options中查找匹配的项
    return props.options.find(option => option[props.valueKey] === props.modelValue) || null;
  },
  set(value) {
    emit('update:modelValue', value);
    emit('change', value);
  }
});
</script>