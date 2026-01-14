<script>
import { useRouter, useRoute } from 'vue-router';
import { computed } from 'vue';
import { Bell } from 'lucide-vue-next';

export default {
  name: 'Header',
  components: {
    Bell
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    
    const goBack = () => {
      router.back();
    };

    // Check if current page is dashboard
    const isDashboard = computed(() => {
      return route.name === 'dashboard' || route.path === '/dashboard';
    });

    return {
      goBack,
      isDashboard
    };
  }
};
</script>

<template>
  <header class="c-header">
    <!-- Show back button only when NOT on dashboard -->
    <button v-if="!isDashboard" @click="goBack" class="c-back-button" aria-label="Ga terug">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <!-- Show bell icon on the right when on dashboard -->
    <button v-if="isDashboard" class="c-bell-button" aria-label="Notificaties">
      <Bell />
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
  display: flex;
  justify-content: space-between;
  align-items: center;
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

.c-bell-button {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--grey-85);
  padding: var(--spacing-03);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.3s ease;
  margin-left: auto;
}

.c-bell-button:hover {
  color: var(--primary);
}
</style>