<script setup>
const props = defineProps({
  label: { type: String, required: true },
  icon: { type: Object, required: false },
});
const emit = defineEmits(['click']);
function handleClick(e) {
  emit('click', e);
}
</script>

<template>
  <button class="c-exportButton" @click="handleClick">
    <span v-if="icon" class="c-exportButton__icon"><component :is="icon" size="20px" /></span>
    <span>{{ label }}</span>
  </button>
</template>

<style scoped>
.c-exportButton {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--grey-85);
  padding:  var(--spacing-baseline) var(--spacing-05);
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: var(--spacing-02);
  font-family: inherit;
  font-size: var(--font-size-3);
  transition: color 0.3s ease;
  color: var(--white);
  background-color: var(--primary);
  border-radius: var(--radius-s);
  transition: all 0.3s ease;
}
.c-exportButton:hover {
  background-color: var(--primary-dark);
}
.c-exportButton__icon {
  display: flex;
  align-items: center;
  margin-right: 0.5em;
}
</style>
