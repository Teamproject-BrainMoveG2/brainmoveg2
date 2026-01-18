<script setup>
defineProps({
  score: {
    type: Number,
    required: true
  }
});
</script>

<template>
  <div class="c-scoreCircle">
    <div class="c-scoreCircle__inner">
      <h1 class="c-scoreCircle__number">{{ score }}</h1>
      <h2 class="c-scoreCircle__text">uw score</h2>
    </div>
  </div>
</template>

<style scoped>
    
.c-scoreCircle {
  width: 11.25rem;
  height: 11.25rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-04);
  border: 3px solid var(--primary);
  padding: 1.5625rem;
}

.c-scoreCircle__inner {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background-color: var(--primary-light);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.c-scoreCircle__number {
  font-size: var(--font-size-10);
  line-height: var(--font-size-11);
  margin-top: 2rem;
  color: var(--primary);
}
</style>