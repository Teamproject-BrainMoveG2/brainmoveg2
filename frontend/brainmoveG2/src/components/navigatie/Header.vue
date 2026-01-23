<script>
import { useRouter, useRoute } from 'vue-router';
import { computed, ref } from 'vue';
import { useCones } from '../../composables/useCones';
import { Bell, X } from 'lucide-vue-next';

import SmallPotjeCard from '../cards/SmallPotjeCard.vue';
import PotjesStatusPopup from '../popups/PotjesStatusPopup.vue';

export default {
  name: 'Header',
  components: {
    Bell,
    X,
    SmallPotjeCard,
    PotjesStatusPopup
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
    const showPopup = ref(false);
    
    const goBack = () => {
      router.back();
    };

    const togglePopup = () => {
      showPopup.value = !showPopup.value;
    };

    const closePopup = () => {
      showPopup.value = false;
    };

    // Check if current page is dashboard
    const isDashboard = computed(() => {
      return route.name === 'dashboard' || route.path === '/dashboard';
    });

    // Use shared composable for cones logic
    const { warningCones, colorToDutch } = useCones();

    return {
      goBack,
      isDashboard,
      showPopup,
      togglePopup,
      closePopup,
      warningCones,
      colorToDutch
    };
  }
};
</script>

<template>
  <header class="c-header">
    <div class="c-header__content">
    <!-- Back button for other pages -->
    <button v-if="!isDashboard" @click="goBack" class="c-back-button" aria-label="Ga terug">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    </button>

    <!-- Dashboard header -->
    <button  @click="togglePopup" class="c-bell-button" aria-label="Notificaties" style="position: relative;">
      <Bell />
      <span v-if="warningCones.length > 0" class="c-bell-notification"></span>
    </button>
    
    <!-- Popup overlay -->
    <PotjesStatusPopup
      :show="showPopup"
      :warningCones="warningCones"
      :colorToDutch="colorToDutch"
      @close="closePopup"
    />
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

  max-width: 26.25rem;
  


  @media (min-width: 768px) {

    max-width: 500px;
    gap: var(--spacing-08);
    

  }

  @media (min-width: 1024px) {

      max-width: 550px;
      gap: var(--spacing-09);
      padding: var(--spacing-06) 0;

  }

}


.c-header__content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;

}

.c-bell-notification {
  position: absolute;
  top: .375rem;
  right: .375rem;
  width: .5rem;
  height: .5rem;
  background: #2196f3;
  border-radius: 50%;
  border: 2px solid white;
  box-shadow: 0 0 0 2px #2196f3;
  z-index: 2;
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