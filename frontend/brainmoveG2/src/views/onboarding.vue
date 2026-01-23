<script>
</script>

<template>
  <main class="c-content-wrapper u-viewport-height u-justify-center">
    
    <div class="c-mascot__container">
      <img src="../assets/img/macot1.png" alt="BrainMove Mascot" class="c-mascot" />
    </div>
      
      <h1>welkom bij brainmove</h1>
      
   
      <p class="body-large">Heeft u hulp nodig bij het opstellen?</p>
      
  
      <section class="c-button__container">
        <RouterLink class="c-btn c-btn--primary" to="/introductie"> Hoe start ik de potjes</RouterLink>
      
        <RouterLink class="c-btn c-btn--secondary" to="/dashboard"> Klaar om te spelen</RouterLink>
      </section>
  </main>
</template>

<style scoped>

.c-button__container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-05);
  width: 100%;
}

</style>