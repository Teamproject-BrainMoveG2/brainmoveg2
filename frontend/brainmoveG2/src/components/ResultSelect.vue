<script setup>
const props = defineProps({
  modelValue: { type: String, required: true },
  options: { type: Array, required: true }, // [{ label, value }]
});
const emit = defineEmits(['update:modelValue']);
function onChange(e) {
  emit('update:modelValue', e.target.value);
}
</script>

<template>
  <select :value="modelValue" @change="onChange" class="c-resultaten-select">
    <option v-for="opt in options" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
  </select>
</template>

<style scoped>
.c-resultaten-select {
  width: 100%;
  border-radius: var(--radius);
  border: 1px solid var(--grey-15);
  background: var(--white);
  font-size: 1rem;
  font-family: "Source Sans Pro", sans-serif;
  font-size: var(--font-size-3);
  line-height: 1.5rem;
  font-weight: var(--font-weight-regular);
  color: var(--grey-85);
  box-sizing: border-box;
  transition: all 0.3s ease;
  padding: var(--spacing-04);
  appearance: none;
  letter-spacing: 0;
  margin-bottom: 0.5rem;
  cursor: pointer;
}
.c-resultaten-select:hover, .c-resultaten-select:focus {
  border-color: var(--primary);
}
</style>
