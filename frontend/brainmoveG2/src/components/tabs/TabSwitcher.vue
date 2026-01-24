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
  padding: 0 var(--spacing-06);
  display: flex;
  flex-direction: row;
  align-items: center;
  max-width: 26.25rem;
  margin: 0 auto;
  margin-bottom: 2rem;
  width: 100%;
  @media (min-width: 768px) {
    max-width: 75%;
  }
  @media (min-width: 1024px) {
    max-width: 60%;
    padding: 0;
  }
}

.c-tab {
    background: none;
    cursor: pointer;
    outline: inherit;
    padding-bottom: var(--spacing-05);
    border: none;
    text-align: center;
    width: 100%;
    transition: color 0.3s ease; 
    border-bottom: 2px solid var(--grey-15);

    @media (min-width: 768px) {
    padding-bottom: var(--spacing-06);
    }
}

.c-tab.is-active {
  color: var(--primary);
}

.c-tab-indicator {
  position: absolute;
  bottom: 0;
  height: 2px;
  background-color: var(--primary);
  pointer-events: none;
  z-index: 0;
  transition: all 0.3s ease;
}
</style>
