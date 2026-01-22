<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';

const props = defineProps({
  activeTab: {
    type: String,
    required: true
  },
  tabs: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['update:activeTab', 'select']);

const tabRefs = ref([]);
const activeIndicator = ref({ left: 0, width: 0 });

const selectTab = (tabValue) => {
  emit('select', tabValue);
  emit('update:activeTab', tabValue);
};

const updateIndicator = () => {
  const activeIndex = props.tabs.findIndex(tab => tab.value === props.activeTab);
  if (activeIndex !== -1 && tabRefs.value[activeIndex]) {
    const tabElement = tabRefs.value[activeIndex];
    activeIndicator.value = {
      left: tabElement.offsetLeft,
      width: tabElement.offsetWidth
    };
  }
};

watch(() => props.activeTab, () => {
  nextTick(updateIndicator);
});

onMounted(() => {
  nextTick(updateIndicator);
});
</script>

<template>
  <div class="c-overzichttab">
    <button
      v-for="(tab, index) in tabs"
      :key="tab.value"
      :ref="el => tabRefs[index] = el"
      class="c-tab body-large"
      :class="{ 'is-active': activeTab === tab.value }"
      @click="selectTab(tab.value)"
    >
      {{ tab.label }}
    </button>
    <div 
      class="c-tab-indicator" 
      :style="{ 
        left: `${activeIndicator.left}px`, 
        width: `${activeIndicator.width}px` 
      }"/>
  </div>
</template>

<style>
.c-overzichttab {
    position: relative;
    display: flex;
}

.c-tab {
    background: none;
    cursor: pointer;
    outline: inherit;
    padding-bottom: var(--spacing-05);
    border: none;
    text-align: center;
    width: 100%;
    transition: color 0.2s ease; 
    border-bottom: 2px solid var(--grey-15);
}

.c-tab.is-active {
    color: var(--primary);
}

.c-tab-indicator {
    position: absolute;
    bottom: -0px;
    height: 2px;
    background-color: var(--primary);
    transition: all 0.3s ease;
    pointer-events: none;
}
</style>
