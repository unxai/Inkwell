<template>
  <TabGroup :defaultIndex="defaultIndex" @change="$emit('change', $event)">
    <TabList class="flex space-x-1 rounded-xl bg-blue-50 p-1">
      <Tab
        v-for="tab in tabs"
        :key="tab.id"
        v-slot="{ selected }"
        as="template"
      >
        <button
          :class="[
            'w-full rounded-lg py-2.5 text-sm font-medium leading-5',
            'ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2',
            selected
              ? 'bg-white text-blue-700 shadow'
              : 'text-blue-500 hover:bg-white/[0.12] hover:text-blue-600'
          ]"
        >
          {{ tab.name }}
        </button>
      </Tab>
    </TabList>
    <TabPanels class="mt-2">
      <TabPanel
        v-for="tab in tabs"
        :key="tab.id"
        :class="[
          'rounded-xl bg-white p-3',
          'ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2'
        ]"
      >
        <slot :name="tab.id"></slot>
      </TabPanel>
    </TabPanels>
  </TabGroup>
</template>

<script setup>
import { TabGroup, TabList, Tab, TabPanels, TabPanel } from '@headlessui/vue';

defineProps({
  tabs: {
    type: Array,
    required: true,
    // 每个tab应该有 { id: 'unique-id', name: '标签名称' }
  },
  defaultIndex: {
    type: Number,
    default: 0
  }
});

defineEmits(['change']);
</script>