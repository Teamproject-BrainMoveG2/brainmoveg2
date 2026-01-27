<script setup>
const props = defineProps({
  show: Boolean,
  customStyle: {
    type: Object,
    default: () => ({})
  }
});
</script>

<template>
  <transition name="fade">
    <div v-if="show" class="c-tooltip" :style="customStyle">
      <slot />
    </div>
  </transition>
</template>

<style scoped>
.c-tooltip {
  position: absolute;
  top: 2.2rem;
  right: 0;
  background-color: var(--white);
  color: var(--grey-90, #222);
  border: 1px solid var(--grey-80);
  border-radius: 6px;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  z-index: 10;
  min-width: 220px;
  max-width: 300px;
  pointer-events: auto;
  font-weight: 500;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
