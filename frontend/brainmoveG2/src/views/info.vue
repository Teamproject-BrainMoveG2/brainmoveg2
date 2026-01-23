<script setup>
import PotjeCard from '../components/cards/PotjeCard.vue';
import InstructionList from '../components/lijst/InstructionList.vue';

import { useCones } from '../composables/useCones';

//hard coded instructions for setting up the potjes
const instructions = [
    {
        number: 1,
        description: 'Zet de schakelaar aan van alle potjes.'
    },
    {
        number: 2,
        description: 'Zet de potjes in een vierkant van 2m op 2m. Als je minder dan 4 potjes gebruikt, laat dan sommige hoeken leeg.'
    }
];

const { cones, colorToDutch } = useCones();

</script>

<template>
  <main class="c-content-wrapper">
     <div class="c-title">
        <h1>POTJES OPSTELLEN</h1> 
    </div>
    <div class="c-mascot__container">
      <img src="../assets/img/macot2.png" alt="BrainMove Mascot" class="c-mascot" />
    </div>
   
    <InstructionList :instructions="instructions" />
    
    <section class="c-cardcontainer">
        <h2>Status Potjes</h2>
        <div class="c-cardgrid">
            <PotjeCard 
                v-for="cone in cones" 
                :key="cone.cone_id"
                :name="colorToDutch[cone.color] || cone.color" 
                :batteryPercentage="cone.battery_percentage" 
                :isConnected="cone.connected"
            />
        </div>
    </section>
  </main>
</template>

<style scoped>

.c-title{
    text-align: left;
    width: 100%;
  }


.c-cardcontainer{
 width: 100%;
 flex-direction: column;
 gap: var(--spacing-04);
 display: flex;
 text-align: left;
 
}
.c-cardcontainer{
 width: 100%;
 flex-direction: column;
 gap: var(--spacing-04);
 display: flex;
 text-align: left;
 
}

.c-cardgrid{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-04);
}


</style>