<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { useGameColors } from '../composables/useGameColors';
import SettingContainer from '../components/SettingContainer.vue';
import DifficultyButton from '../components/buttons/DifficultyButton.vue';
import CounterButton from '../components/buttons/CounterButton.vue';

const route = useRoute();
const gameId = ref(route.params.id);
const selectedDifficulty = ref('relaxed');
const rounds = ref(1);
const colors = ref(4);

const difficulties = [
    { id: 'relaxed', label: 'Relaxed', color: 'green' },
    { id: 'challenging', label: 'Challenging', color: 'orange' },
    { id: 'intense', label: 'Intense', color: 'red' }
];

// Use the game colors composable
const { buttonClass, colorVariant, cardBackgroundColor, primaryColor } = useGameColors(gameId);

const selectDifficulty = (difficulty) => {
    selectedDifficulty.value = difficulty;
};

</script>

<template>
    <main class="c-content-wrapper">
        <div class="c-title">
            <h1>Game</h1>
            <p>Description</p>
        </div>
        <SettingContainer title="Kies je moeilijkheidsgraad">
                <DifficultyButton
                    v-for="difficulty in difficulties"
                    :key="difficulty.id"
                    :difficulty="difficulty"
                    :is-active="selectedDifficulty === difficulty.id"
                    @select="selectDifficulty(difficulty.id)"
                />
        </SettingContainer>
        <div class="c-setting-section--extra">
            <SettingContainer title="Aantal Rondes">
                <CounterButton v-model="rounds" :min="1" />
            </SettingContainer>
            <SettingContainer title="Aantal kleuren">
                <CounterButton v-model="colors" :min="1" :max="4"/>
            </SettingContainer>
        </div>
        <SettingContainer title="Gebruikersnaam">
            <form action="#" class="c-form">
                <input type="text" class="c-input small-body" placeholder="Voer je gebruikersnaam in" />
            </form>
        </SettingContainer>
        
        <RouterLink :class="buttonClass" :to="`/instructions/${gameId}`">Ga door</RouterLink>
    </main>
</template>

<style scoped>

.c-form{
    width: 100%;
}

.c-input{
    width: 100%;
    padding: var(--spacing-05) var(--spacing-05);
    border: 1px solid var(--grey-15);
    border-radius: var(--radius);
    font-size: var(--font-size-base);
    transition: border 0.3s ease;
    color: var(--grey-70);
    box-sizing: border-box;
}

.c-input:focus, .c-input:hover, .c-input:active {
    outline: none;
    border-color: var(--primary);
}

.c-setting-section--extra {
    display: flex;
    gap: var(--spacing-04);
    width: 100%;
}

.c-title{
    text-align: left;
    display: flex;
    flex-direction: column;
    width: 100%;
    gap: var(--spacing-05);
}
</style>