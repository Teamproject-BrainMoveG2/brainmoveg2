<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import InstructionList from '../components/InstructionList.vue';

const route = useRoute();
const gameId = ref(route.params.id);

// Instructions for different games
const gameInstructions = {
    '1': {
        steps: [
            {
                number: 1,
                text: 'Een kleur verschijnt op je scherm'
            },
            {
                number: 2,
                text: 'Tik zo snel mogelijk het bijbehorende potje aan'
            },
            {
                number: 3,
                text: 'De tijd wordt steeds korter - hoe lang houd je vol?'
            }
        ]
    },
    '2': {
        title: 'Memory game',
        steps: [
            {
                number: 1,
                text: 'Onthoud de volgorde van de oplichtende potjes'
            },
            {
                number: 2,
                text: 'Herhaal de volgorde door de potjes aan te tikken'
            },
            {
                number: 3,
                text: 'De volgorde wordt steeds langer - hoeveel kun je onthouden?'
            }
        ],
    },
    '3': {
        title: 'Calm game',
        steps: [
            {
                number: 1,
                text: 'Een kleur verschijnt op je scherm'
            },
            {
                number: 2,
                text: 'Tik zo snel mogelijk het bijbehorende potje aan'
            },
            {
                number: 3,
                text: 'Er is geen tijdslimiet - Doe je best om rustig en gefocust te blijven'
            }
        ],
    }
    // Add more games here as needed
};

// Get the instructions for the current game based on game ID
const currentGame = computed(() => {
    return gameInstructions[gameId.value] 
});

// Get the color variant based on game ID
const colorVariant = computed(() => {
    const colorMap = {
        '1': 'green',
        '2': 'orange',
        '3': 'primary'
    };
    return colorMap[gameId.value] || 'primary'; // Default to blue
});

// Get the button class based on game ID
const buttonClass = computed(() => {
    return `c-btn c-btn--${colorVariant.value}`;
});

</script>

<template>
    <main class="c-content-wrapper">
        <div class="c-mascot__container">
            <img src="../assets/img/mascot3.png" alt="BrainMove Mascot" class="c-mascot" />
        </div>
         <div class="c-title">
             <h1>hoe te spelen</h1>
         </div>
        <InstructionList :instructions="currentGame.steps" :color="colorVariant" />
        <RouterLink :class="buttonClass" to="/dashboard">Ga door</RouterLink>
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