<script setup>
import { ChevronDown } from 'lucide-vue-next';
const props = defineProps({
  modelValue: { type: String, required: true },
  options: { type: Array, required: true }, 
});
import { ref } from 'vue';
const emit = defineEmits(['update:modelValue']);
const isOpen = ref(false);
function onChange(e) {
  emit('update:modelValue', e.target.value);
  isOpen.value = false;
}

function onFocus() {
  isOpen.value = true;
}
function onBlur() {
  isOpen.value = false;
}
</script>

<template>
  <div class="c-resultaten-select-wrapper">
    <select :value="modelValue" @change="onChange" class="c-resultaten-select" @focus="onFocus" @blur="onBlur">
      <option v-for="opt in options" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
    </select>
    <span class="chevron-icon" :class="{ open: isOpen }" aria-hidden="true">
      <ChevronDown :size="20" />
    </span>
  </div>
</template>

<style scoped>
.c-resultaten-select-wrapper {
  position: relative;
  width: 100%;
}
.c-resultaten-select {
  width: 100%;
  border-radius: var(--radius);
  border: 1px solid var(--grey-15);
  outline: none;
  background: var(--white);
  font-size: 1rem;
  font-family: "source-sans-pro", sans-serif;
  font-size: var(--font-size-3);
  line-height: 1.5rem;
  font-weight: var(--font-weight-regular);
  color: var(--grey-85);
  box-sizing: border-box;
  transition: all 0.3s ease;
  padding: var(--spacing-04);
  appearance: none;
  letter-spacing: 0;
}

.c-resultaten-select:hover, .c-resultaten-select:focus, .c-resultaten-select:focus-visible {
  border-color: var(--primary) !important;
}
.chevron-icon {
  position: absolute;
  right: var(--font-size-3);
  top: 50%;
  transform: translateY(-50%) rotate(0deg);
  pointer-events: none;
  display: flex;
  align-items: center;
  height: 100%;
  color: var(--grey-90);
  transition: transform 0.3s cubic-bezier(0.4,0,0.2,1);
}
.chevron-icon.open {
  transform: translateY(-50%) rotate(180deg);
}

.c-resultaten-select option {
    background: var(--white);
    color: var(--grey-85);
    font-size: var(--font-size-3);
    font-family: "source-sans-pro", sans-serif;
    padding: var(--spacing-baseline) var(--spacing-03);
    
}
.c-resultaten-select option:checked, .c-resultaten-select option:hover {
    background: var(--primary-light);
    color: var(--primary);
}
</style>
