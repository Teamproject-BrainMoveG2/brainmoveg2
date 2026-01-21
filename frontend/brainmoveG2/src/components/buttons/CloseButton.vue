<script setup>
import { X } from 'lucide-vue-next';
const emit = defineEmits(['close']);
</script>

<template>
  <button @click="$emit('close')" class="c-popup__close" aria-label="Sluit popup">
    <X :size="24" />
  </button>
</template>

<style scoped>
.c-popup__close {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--grey-85);
  padding: var(--spacing-02);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.3s ease;
  border-radius: var(--radius-s);
}
.c-popup__close:hover {
  color: var(--primary);
  background-color: var(--grey-15);
}
</style>
