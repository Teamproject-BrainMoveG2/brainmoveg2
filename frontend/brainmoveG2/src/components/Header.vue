<script>
import { useRouter } from 'vue-router';

export default {
  name: 'Header',
  setup() {
    const router = useRouter();
    
    const goBack = () => {
      router.back();
    };

    return {
      goBack
    };
  }
};
</script>

<template>
  <header class="c-header">
    <button @click="goBack" class="c-back-button" aria-label="Ga terug">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
  </header>
</template>

<style scoped>
.c-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: var(--spacing-06);
}

.c-back-button {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--grey-85);
  padding: var(--spacing-03);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.3s ease;
}

.c-back-button:hover {
  color: var(--primary);
}

.c-back-button svg {
  width: 24px;
  height: 24px;
}
</style>