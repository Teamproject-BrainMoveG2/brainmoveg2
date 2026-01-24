<script>
import { ref } from 'vue';
import { Bell } from 'lucide-vue-next';
import PotjesStatusPopup from './popups/PotjesStatusPopup.vue';
import { useCones } from './../composables/useCones';

export default {
  name: 'BellNotification',
  components: {
    Bell,
    PotjesStatusPopup
  },
  setup() {
    const showPopup = ref(false);
    const togglePopup = () => {
      showPopup.value = !showPopup.value;
    };
    const closePopup = () => {
      showPopup.value = false;
    };
    const { warningCones, colorToDutch } = useCones();
    return {
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
  <button @click="togglePopup" class="c-bell-button" aria-label="Notificaties" style="position: relative;">
    <Bell />
    <span v-if="warningCones.length > 0" class="c-bell-notification"></span>
  </button>
  <PotjesStatusPopup
    :show="showPopup"
    :warningCones="warningCones"
    :colorToDutch="colorToDutch"
    @close="closePopup"
  />
</template>

<style scoped>
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
</style>
