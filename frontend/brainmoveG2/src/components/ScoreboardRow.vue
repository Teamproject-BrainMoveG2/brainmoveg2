<script setup>
import { Trophy, Medal } from 'lucide-vue-next';
import { computed } from 'vue';

const props = defineProps({
  position: {
    type: Number,
    required: true
  },
  name: {
    type: String,
    required: true
  },
  score: {
    type: Number,
    required: true
  },
  isPlayer: {
    type: Boolean,
    default: false
  }
});
</script>

<template>
  <tr :class="['c-table__row', { 'c-table__row--player': isPlayer }]">
    <td>
      <div :class="['c-table__trophy', { 'c-table__trophy--player': isPlayer }]">
        <component :is="isPlayer ? Medal : Trophy" class="c-table__trophy-icon"  />
        <span>{{ position }}</span>
      </div>
    </td>
    <td>{{ name }}</td>
    <td>{{ score }}</td>
  </tr>
</template>

