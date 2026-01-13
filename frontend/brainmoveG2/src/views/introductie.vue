<script setup>
    import { BatteryMedium } from 'lucide-vue-next';
    import { Wifi } from 'lucide-vue-next';
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
            <div class="c-cardpotje">
                <div class="c-cardpotje__title">
                    <div class="c-cardpotje__circle"></div> <p class="small-body">Groen</p>
                </div>
                <div class="c-cardpotje__content">
                    <div class="c-cardpotje__status">
                        <p class="c-cardpotje__percentage">78%</p>
                        <BatteryMedium class="c-cardpotje__icon" />
                    </div>
                    <Wifi class="c-cardpotje__icon" />
                </div>
            </div>
            

        </div>
    </div>
    <RouterLink class="c-btn c-btn--primary" to="/Dashboard">Ga door</RouterLink>
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

.c-cardpotje{
    border-radius: var(--radius-s);
    padding: var(--spacing-05);
    background-color: var(--white);
    display: flex;
    flex-direction: column;
    color: var(--grey-85);
    gap: var(--spacing-baseline);
}

.c-cardpotje__circle{
    width: .9375rem;
    height: .9375rem;
    border-radius: 50%;
    background-color: var(--accent-green);
}

.c-cardpotje__title{
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: var(--spacing-04);
}

.c-cardpotje__content{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

.c-cardpotje__status{
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: var(--spacing-03);
}

.c-cardpotje__percentage{
    font-family: bebas-neue, sans-serif;
    font-size: var(--font-size-8);
    font-weight: var(--font-weight-bold);
    line-height: 2.5rem;
}

.c-cardpotje__icon {
  width: 1.875rem;
  height: 1.875rem;
  line-height: 2rem;
}

.c-title {
  text-align: start;
  width: 100%;
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