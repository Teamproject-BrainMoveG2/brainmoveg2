<script setup>
import { computed } from 'vue';
import { formatSnelheid } from '../../composables/useFormatSnelheid';
const props = defineProps({
  name: { type: String, required: true },
  accuracy: { type: String, required: true },
  reaction: { type: [String, Number], required: true },
  difficulty: { type: String, required: true }
});
</script>

<template>
  <tr class="c-table__row">
    <td>{{ name }}</td>
    <td>{{ accuracy }}</td>
    <td>{{ formatSnelheid('reactie', reaction) }}</td>
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
tr td:first-child {
  overflow: hidden;
  text-overflow: ellipsis;
  padding-right: .5rem;
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
