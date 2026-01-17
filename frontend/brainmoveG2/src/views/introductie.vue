<script setup>
import PotjeCard from '../components/cards/PotjeCard.vue';
import InstructionList from '../components/lijst/InstructionList.vue';
import { ref, onMounted } from 'vue';

const Ip = `${window.location.hostname}:8000`;

//hard coded instructions for setting up the potjes
const instructions = [
    {
        number: 1,
        text: 'Zet de schakelaar aan van alle potjes.'
    },
    {
        number: 2,
        text: 'Zet de potjes in een vierkant van 2m op 2m. Als je minder dan 4 potjes gebruikt, laat dan sommige hoeken leeg.'
    }
];

const cones = ref([]);

// Color mapping from English to Dutch
const colorToDutch = {
    'red': 'Rood',
    'blue': 'Blauw',
    'green': 'Groen',
    'yellow': 'Geel',
    'orange': 'Oranje'
};

const fetchCones = async () => {
    try {
        const response = await fetch(`http://${Ip}/cones`);
        const data = await response.json();
        cones.value = data;
    } catch (error) {
        console.error('Error fetching cones:', error);
    }
};

onMounted(() => {
    fetchCones();
});

</script>

<template>
  <main class="c-content-wrapper u-justify-center u-viewport-height-80">

    <div class="c-mascot__container">
      <img src="../assets/img/macot2.png" alt="BrainMove Mascot" class="c-mascot" />
    </div>
    <div class="c-title">
        <h1>POTJES OPSTELLEN</h1> 
    </div>
   
    <InstructionList :instructions="instructions" />
    
    <div class="c-cardcontainer">
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
    </div>
    <RouterLink class="c-btn c-btn--primary" to="/dashboard">Ga door</RouterLink>
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