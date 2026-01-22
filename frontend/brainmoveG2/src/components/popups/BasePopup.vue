<script setup>
import CloseButton from '../buttons/CloseButton.vue';

defineProps({
  show: {
    type: Boolean,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  maxWidth: {
    type: String,
    default: '700px'
  }
});

const emit = defineEmits(['close']);

function onClose() {
  emit('close');
}
</script>

<template>
  <transition name="fade">
    <div v-if="show" class="c-popup-overlay" @click="onClose">
      <transition name="slide-up">
        <div v-if="show" class="c-popup" @click.stop :style="{ maxWidth }">
          <div class="c-popup__header">
            <h2 class="c-popup__title">{{ title }}</h2>
            <CloseButton @close="onClose" />
          </div>
          <div class="c-popup__content">
            <slot></slot>
          </div>
        </div>
      </transition>
    </div>
  </transition>
</template>

<style scoped>

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}


.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.2s ease;
}

.slide-up-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.slide-up-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.c-popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: start;
  justify-content: center;
  z-index: 1000;
  padding: var(--spacing-04);
}

.c-popup {
  background: var(--white);
  border-radius: var(--radius-s);
  padding: var(--spacing-05);
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.c-popup__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-05);
}

.c-popup__title {
  font-size: var(--font-size-5);
  font-weight: var(--font-weight-bold);
  color: var(--grey-85);
  margin: 0;
}

.c-popup__content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-03);
}
</style>
