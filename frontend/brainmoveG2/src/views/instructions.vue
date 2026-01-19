<script setup>

import { onMounted, ref } from 'vue';
import { useRoute, RouterLink } from 'vue-router';
import InstructionList from '../components/lijst/InstructionList.vue';
import { useGameColors } from '../composables/useGameColors';

const route = useRoute();
const gameId = ref(route.params.id);
const tutorial = ref({steps: [] });

const Ip = `${window.location.hostname}:8000`;

async function fetchTutorial() {
    try {
        const response = await fetch(`http://${Ip}/modes/${gameId.value}/tutorial`);
        if (!response.ok) throw new Error('Failed to fetch tutorial');
        tutorial.value = await response.json();
    } catch (e) {
        tutorial.value = {steps: [] };
    }
}

onMounted(fetchTutorial);

// Use the game colors composable
const { buttonClass, colorVariant, cardBackgroundColor, primaryColor } = useGameColors(gameId);

</script>

<template>
    <main class="c-content-wrapper u-justify-center u-viewport-height-80">
        <div class="c-mascot__container">
            <img src="../assets/img/mascot3.png" alt="BrainMove Mascot" class="c-mascot" />
        </div>
         <div class="c-title">
             <h1>hoe te spelen</h1>
         </div>
        <InstructionList :instructions="tutorial.steps" :color="colorVariant" />
        <RouterLink :class="buttonClass" :to="`/game/${gameId}`">Spel starten!</RouterLink>
    </main>

</template>

<style scoped>

.c-title{
    text-align: left;
    width: 100%;
  }

.c-mascot{
    width: 125%;
}

</style>