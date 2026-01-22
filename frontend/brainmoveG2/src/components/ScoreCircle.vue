
<script setup>
import { ref, watch, onMounted } from 'vue';

const props = defineProps({
  score: {
    type: Number,
    required: true
  }
});

const animatedScore = ref(0);

const animateScore = (target) => {
  const duration = 1350; // ms
  const frameRate = 30; // fps
  const totalFrames = Math.round((duration / 1000) * frameRate);
  const increment = target / totalFrames;
  let frame = 0;
  animatedScore.value = 0;
  const interval = setInterval(() => {
    frame++;
    animatedScore.value = Math.round(frame * increment);
    if (frame >= totalFrames) {
      animatedScore.value = Math.round(target);
      clearInterval(interval);
    }
  }, 1000 / frameRate);
};

onMounted(() => {
  animateScore(props.score);
});

watch(() => props.score, (newScore) => {
  animateScore(newScore);
});
</script>

<template>
  <div class="c-scoreCircle">
    <div class="c-scoreCircle__inner">
      <h1 class="c-scoreCircle__number">{{ animatedScore }}</h1>
      <h2 class="c-scoreCircle__text">uw score</h2>
    </div>
  </div>
</template>

<style scoped>
    

.c-scoreCircle {
  width: 11.50rem;
  height: 11.50rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-04);
  border: 3px solid var(--primary);
  padding: 1.5625rem;
  position: relative;
}

.c-scoreCircle::before {
  content: '';
  position: absolute;
  left: 50%;
  top: 50%;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  border: 3px solid var(--primary);
  transform: translate(-50%, -50%) scale(1);
  opacity: 0.6;
  pointer-events: none;
  animation: borderPulse 1.5s infinite;
  z-index: 0;
}

@keyframes borderPulse {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 0.6;
  }

  100% {
    transform: translate(-50%, -50%) scale(1.28);
    opacity: 0;
  }
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
  margin-top: 0.5rem;
  color: var(--primary);
}
</style>