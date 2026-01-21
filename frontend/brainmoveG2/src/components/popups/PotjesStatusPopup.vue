<script>
import CloseButton from '../buttons/CloseButton.vue';
import SmallPotjeCard from '../cards/SmallPotjeCard.vue';

export default {
  name: 'PotjesStatusPopup',
  components: {CloseButton, SmallPotjeCard },
  props: {
    show: {
      type: Boolean,
      required: true
    },
    warningCones: {
      type: Array,
      required: true
    },
    colorToDutch: {
      type: Object,
      required: true
    }
  },
  emits: ['close'],
  methods: {
    onClose() {
      this.$emit('close');
    }
  }
};
</script>


<template>
  <div v-if="show" class="c-popup-overlay" @click="onClose">
    <div class="c-popup" @click.stop>
      <div class="c-popup__header">
        <h2 class="c-popup__title">Potjes Status</h2>
        <CloseButton @close="onClose" />
      </div>
      <div class="c-popup__content">
        <template v-if="warningCones.length > 0">
          <SmallPotjeCard
            v-for="cone in warningCones"
            :key="cone.cone_id"
            :name="colorToDutch[cone.color] || cone.color"
            :color="cone.color"
            :battery="cone.battery_percentage"
            :isConnected="cone.connected"
          />
        </template>
        <template v-else>
          <p style="text-align:center; font-size: 1.2rem;">Geen problemen</p>
        </template>
      </div>
    </div>
  </div>
</template>



<style scoped>
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
  max-width: 500px;
  width: 75%;
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
