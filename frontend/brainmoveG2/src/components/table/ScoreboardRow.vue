<script setup>
import { Trophy, Medal } from 'lucide-vue-next';

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

<style>

  .c-table__row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-05) var(--spacing-04) ;
    border-bottom: 2px solid var(--grey-15);
    gap: var(--spacing-04);

    font-family: "source-sans-pro", sans-serif;
    font-size: var(--font-size-3); 
    line-height: 1.5rem;
    font-weight: var(--font-weight-regular);
    letter-spacing: 0;
}


.c-table__row:nth-child(1) .c-table__trophy, .c-table__row:nth-child(1) .c-table__trophy-icon {

    border-color: var(--accent-orange);
    color: var(--accent-orange);
}

.c-table__row:nth-child(3) .c-table__trophy, .c-table__row:nth-child(3) .c-table__trophy-icon {

    border-color: var(--accent-orange-dark);
    color: var(--accent-orange-dark);
}

.c-table__row--player{

    background-color: var(--primary-light);
   

}

.c-table__trophy {
    display: flex;
    align-items: center;
    gap: var(--spacing-02);
    border: 1px solid var(--grey-85);
    padding: var(--spacing-02) var(--spacing-03);
    border-radius: var(--radius-s);
}

.c-table__trophy--player {
    border: none;
    
}

.c-table__trophy-icon {
    width: .875rem;
    height: .875rem;
} 

</style>
