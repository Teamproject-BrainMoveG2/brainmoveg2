<script setup>
import { computed } from 'vue';
import { formatSnelheid } from '../../composables/useFormatSnelheid';
const props = defineProps({
  name: { type: String, required: true },
  accuracy: { type: String, required: true },
  reaction: { type: [String, Number], required: true },
  difficulty: { type: String, required: true }
});
const truncatedName = computed(() => {
  if (!props.name) return '';
  return props.name.length > 14 ? props.name.slice(0, 11) + '...' : props.name;
});
</script>

<template>
  <tr class="c-table__row">
    <td>{{ truncatedName }}</td>
    <td>{{ accuracy }}</td>
    <td>{{ formatSnelheid('snelheid', reaction) }}</td>
    <td>{{ difficulty }}</td>
  </tr>
</template>

<style scoped>

.c-table--resultaten td {
  padding: 0;
  width: 25%;
  box-sizing: border-box;
  text-align: left;
}

.c-table__row {
  border-bottom: 1px solid var(--grey-15);
  padding: var(--spacing-04) ;
  gap: 0
}

.c-table__row:hover {
  background-color: var(--grey-5);
}

.c-table__row:last-child {
  border-bottom: none;
}
</style>
