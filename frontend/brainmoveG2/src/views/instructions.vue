<script setup>
import { onMounted, onUnmounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useGameColors } from '../composables/useGameColors';
import InstructionList from '../components/lijst/InstructionList.vue';
import { TriangleAlert } from 'lucide-vue-next';


const route = useRoute();
const router = useRouter();
const gameId = ref(route.params.id);
const tutorial = ref({steps: [] });
const settings = route.query;
const gameInProgress = ref(false);

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

async function CheckForGame(){
     try {
        const response = await fetch(`http://${Ip}/games/status`);
        const status = await response.json();
        if (status && status.game_in_progress) {
            gameInProgress.value = true;
        } else {
            gameInProgress.value = false;
        }
    } catch (error) {
        gameInProgress.value = false;
    }
}


let intervalId = null;
onMounted(() => {
    fetchTutorial();
    CheckForGame();
    intervalId = setInterval(CheckForGame, 5000);
    console.log('Route params:', route.params);
    console.log('Route query:', route.query);
});

onUnmounted(() => {
    if (intervalId) clearInterval(intervalId);
});

function startGameAndGo() {
    router.push({
        name: 'game',
        params: { id: gameId.value },
        query: settings
    });
}

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
        <div v-if="gameInProgress" class="c-warning">
            <TriangleAlert size="30px" />
            <h2>Er is een spel bezig, even geduld!</h2>
        </div>
        <button v-else :class="buttonClass" @click="startGameAndGo">Spel starten!</button>
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

.c-warning{
    background-color: var(--red-light);
    border: 1px solid var(--red);
    border-radius: var(--radius);
    padding: var(--spacing-06);
    margin-top: var(--spacing-06);
    margin-bottom: var(--spacing-06);
    width: 100%;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: var(--spacing-03);
}

</style>