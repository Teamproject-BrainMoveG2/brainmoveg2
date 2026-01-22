<script>
import BasePopup from './BasePopup.vue';
import SmallPotjeCard from '../cards/SmallPotjeCard.vue';

export default {
  name: 'PotjesStatusPopup',
  components: { BasePopup, SmallPotjeCard },
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
  <BasePopup 
    :show="show" 
    title="Potjes Status"
    max-width="500px"
    @close="onClose"
  >
    <SmallPotjeCard
      v-for="cone in warningCones"
      v-if="warningCones.length > 0"
      :key="cone.cone_id"
      :name="colorToDutch[cone.color] || cone.color"
      :color="cone.color"
      :battery="cone.battery_percentage"
      :isConnected="cone.connected"
    />
    <p v-else style="text-align:center; font-size: 1.2rem;">Geen problemen</p>
  </BasePopup>
</template>



<style scoped>

</style>
