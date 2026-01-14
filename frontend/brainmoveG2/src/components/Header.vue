<script>
import { useRouter, useRoute } from 'vue-router';
import { computed } from 'vue';
import { Bell, X } from 'lucide-vue-next';

export default {
  name: 'Header',
  components: {
    Bell,
    X
  },
  props: {
    currentRound: {
      type: Number,
      default: 1
    },
    totalRounds: {
      type: Number,
      default: 10
    }
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    
    const goBack = () => {
      router.back();
    };

    const stopGame = () => {
      router.push('/dashboard');
    };

    // Check if current page is dashboard
    const isDashboard = computed(() => {
      return route.name === 'dashboard' || route.path === '/dashboard';
    });

    // Check if current page is game (exact match only, not gamesettings)
    const isGame = computed(() => {
      return route.name === 'game';
    });

    return {
      goBack,
      stopGame,
      isDashboard,
      isGame
    };
  }
};
</script>

<template>
  <header class="c-header">
    <!-- Game header layout -->
    <div v-if="isGame" class="c-game-header">
      <button @click="stopGame" class="c-stop-button" aria-label="Stop game">
        <X :size="24" />
        <span>Stoppen</span>
      </button>
      <span class="c-round-counter">{{ currentRound }}/{{ totalRounds }}</span>
    </div>

    <!-- Dashboard header -->
    <button v-else-if="isDashboard" class="c-bell-button" aria-label="Notificaties">
      <Bell />
    </button>

    <!-- Back button for other pages -->
    <button v-else @click="goBack" class="c-back-button" aria-label="Ga terug">
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
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.c-game-header {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.c-stop-button {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--grey-85);
  padding: var(--spacing-03);
  display: flex;
  align-items: center;
  gap: var(--spacing-02);
  font-family: inherit;
  font-size: var(--font-size-3);
  transition: color 0.3s ease;
}

.c-stop-button:hover {
  color: var(--red);
}

.c-round-counter {
  font-size: var(--font-size-3);
  color: var(--grey-85);
  font-weight: var(--font-weight-medium);
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