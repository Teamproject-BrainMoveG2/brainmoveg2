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

  <footer class="c-footer">
    <div class="c-footer__content">
      <img src="../assets/img/Howes_logo.jpg" alt="Mascot Left" class="c-footer__img" />
      <span class="c-footer__text">Howest MCT 2026</span>
      <img src="../assets/img/sport_innovatie.webp" alt="Mascot Right" class="c-footer__img" />
    </div>
  </footer>
</template>

<style scoped>

.c-button__container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-05);
  width: 100%;

  @media (min-width: 768px) {
    max-width: 26.25rem;
  }
}


.c-footer {
  position: fixed;
  left: 0;
  bottom: 0;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--white);
  padding: 0.5rem 0;
  z-index: 100;

}

.c-footer__content {

  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;


  @media (min-width: 768px) {
    max-width: 75%;
  }

  @media (min-width: 1024px) {
    max-width: 60%;
    padding: 0;
  }

}

.c-footer__img {
  padding: var(--spacing-baseline);
  height: 3rem;
  width: auto;
}
.c-footer__text {
  font-size:  var(--font-size-2);
  font-weight: 600;
  color: var(--primary);
  letter-spacing: 0.05em;
  text-align: center;

  @media (min-width: 1024px) {
    font-size:  var(--font-size-4);
  }
}
</style>