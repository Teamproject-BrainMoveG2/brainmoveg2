<script>

import { useRouter, useRoute } from 'vue-router';
import { computed } from 'vue';
import { X } from 'lucide-vue-next';
import BellNotification from '../BellNotification.vue';
import SmallPotjeCard from '../cards/SmallPotjeCard.vue';

export default {
  name: 'Header',
  components: {
    BellNotification,
    X,
    SmallPotjeCard
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

    const isDashboard = computed(() => {
      return route.name === 'dashboard' || route.path === '/dashboard';
    });

    const isGameOverzicht = computed(() => {
      return route.name === 'gameoverzicht' || /^\/gameoverzicht\/.*/.test(route.path);
    });

    return {
      goBack,
      isDashboard,
      isGameOverzicht
    };
  }
};
</script>

<template>
  <header class="c-header">
    <div class="c-header__content">
    <button v-if="!isDashboard && !isGameOverzicht" @click="goBack" class="c-back-button" aria-label="Ga terug">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>
    <div class="c-header__bell">
      <BellNotification  />
    </div>
    
  </div>
  </header>
</template>

<style scoped>
.c-header {
  display: flex;
  align-items: center;
  padding: var(--spacing-06);
  margin-left: auto;
  margin-right: auto;
  max-width: 34.375rem;

  @media (min-width: 768px) {
    max-width: 75%;
   
  }

  @media (min-width: 1024px) {
    max-width: 60%;
    padding: var(--spacing-06) 0;
  }

}


.c-header__content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;

}

.c-header__bell{
  display: inline;
  width: 100%;

  @media (min-width: 768px) {
    display: none;
  }
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