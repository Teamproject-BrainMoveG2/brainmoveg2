<script setup>
    import PotjeCard from '../components/PotjeCard.vue';
</script>

<template>
  <main class="c-content-wrapper">

    <div class="c-mascot__container">
      <img src="../assets/img/macot2.png" alt="BrainMove Mascot" class="c-mascot" />
    </div>
    <div class="c-title">
        <h1>POTJES OPSTELLEN</h1> 
    </div>
   
    
    <div class="c-instructions">
      <div class="c-instruction-item">
        <span class="c-instruction-number">1</span>
        <p class="c-instruction-text">Zet de schakelaar aan van alle potjes.</p>
      </div>
      
      <div class="c-instruction-item">
        <span class="c-instruction-number">2</span>
        <p class="c-instruction-text">Zet de potjes in een vierkant van 2m op 2m. Als je minder dan 4 potjes gebruikt, laat dan sommige hoeken leeg.</p>
      </div>
    </div>
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

.c-instructions {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-06);
  text-align: left;
}

.c-instruction-item {
  display: flex;
  gap: var(--spacing-05);
  flex-direction: row;
  justify-content: start;
  align-items: center;
}

.c-instruction-number {
  width: 2.5rem;
  height: 2.5rem;
  min-width: 2.5rem;
  border-radius: 50%;
  background-color: var(--primary-light-5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.c-instruction-text {
  font-size: var(--font-size-3);
  line-height: 24px;
  margin: 0;
  color: var(--grey-85);
}

@media (min-width: 768px) {
  
  .c-instruction-text {
    font-size: var(--font-size-4);
    line-height: 28px;
  }
}

@media (min-width: 1024px) {
  
  .c-instruction-number {
    font-size: var(--font-size-8);
  }
  
  .c-instruction-text {
    font-size: var(--font-size-5);
    line-height: 32px;
  }
}
</style>