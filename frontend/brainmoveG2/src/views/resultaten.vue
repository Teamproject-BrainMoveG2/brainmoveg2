<script setup>
  import { Download } from 'lucide-vue-next';

</script>

<template>
    <header class="c-header">
    <div class="c-header__content">
      <div class="c-header__title-wrapper">
        <h1>Resultaten</h1>
        <button class="c-exportButton"><span class="c-exportButton__icon"><Download size="20px" /></span><span>Exporteer</span></button>
      </div>
      <p class="small-body">Bekijk het totale aantal resultaten </p>
    </div>
  </header>
    <main class="c-content-wrapper">
      
        
    </main>
</template>

<style scoped>

.c-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  padding: var(--spacing-06);
  display: flex;
  justify-content: center;
  align-items: center;
}

.c-header__content {
  width: 100%;
  display: flex;
  flex-direction: column;
  max-width: 26.25rem;
  gap: var(--spacing-03);
  color: var(--grey-85);


   @media (min-width: 768px) {

    max-width: 500px;

  }

  @media (min-width: 1024px) {

      max-width: 550px;

  }
}

.c-header__title-wrapper {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  width: 100%;
}

.c-exportButton {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--grey-85);
  padding:  var(--spacing-baseline) var(--spacing-05);
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: var(--spacing-02);
  font-family: inherit;
  font-size: var(--font-size-3);
  transition: color 0.3s ease;
  color: var(--white);
  background-color: var(--primary);
  border-radius: var(--radius-s);
  transition: all 0.3s ease;
}

.c-exportButton:hover {
  background-color: var(--primary-dark);
}
</style>