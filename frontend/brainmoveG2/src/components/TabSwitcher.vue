<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  activeTab: {
    type: String,
    required: true
  },
  tabs: {
    type: Array,
    required: true
    // Example: [{ label: 'Scoreboard', value: 'scoreboard' }, { label: 'Speloverzicht', value: 'speloverzicht' }]
  }
});

const emit = defineEmits(['update:activeTab']);

const selectTab = (tabValue) => {
  emit('update:activeTab', tabValue);
};
</script>

<template>
  <div class="c-overzichttab">
    <button
      v-for="tab in tabs"
      :key="tab.value"
      class="c-tab body-large"
      :class="{ 'c-tab--active': activeTab === tab.value }"
      @click="selectTab(tab.value)"
    >
      {{ tab.label }}
    </button>
  </div>
</template>

<style>
    .c-tab{
    background: none;
    cursor: pointer;
    outline: inherit;
    padding-bottom: var(--spacing-05);
    border: none;
    border-bottom: 2px solid var(--grey-15);
    text-align: center;
    width: 100%;
    transition: border-color 0.2s ease;
}

.c-tab--active{
    border-bottom: 2px solid var(--primary);
}

</style>
