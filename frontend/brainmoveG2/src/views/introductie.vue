<script setup>
import PotjeCard from '../components/PotjeCard.vue';
import InstructionList from '../components/InstructionList.vue';

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

</script>

<template>
  <main class="c-content-wrapper">

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
                name="Groen" 
                :batteryPercentage="78" 
                :isConnected="true"
            />
            <PotjeCard 
                name="Rood" 
                :batteryPercentage="78" 
                :isConnected="true"
            />
            <PotjeCard 
                name="Blauw" 
                :batteryPercentage="78" 
                :isConnected="true"
            />
            <PotjeCard 
                name="Geel" 
                :batteryPercentage="78" 
                :isConnected="false"
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

@media (max-width: 395px) {

    h1{
        font-size: var(--font-size-6);
    }

    
}

</style>