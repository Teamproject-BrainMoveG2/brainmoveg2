<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';
import { useGameColors } from '../composables/useGameColors';
import SettingContainer from '../components/SettingContainer.vue';
import DifficultyButton from '../components/buttons/DifficultyButton.vue';
import CounterButton from '../components/buttons/CounterButton.vue';
import TextInput from '../components/inputs/TextInput.vue';
import SmallPotjeCard from '../components/cards/SmallPotjeCard.vue';

const route = useRoute();
const gameId = ref(route.params.id);
const selectedDifficulty = ref('relaxed');
const rounds = ref(1);
const colors = ref(4);
const username = ref('');

const difficulties = [
    { id: 'relaxed', label: 'Relaxed', color: 'green' },
    { id: 'challenging', label: 'Challenging', color: 'orange' },
    { id: 'intense', label: 'Intense', color: 'red' }
];

const colorPotjes = ref([
    { id: 1, name: 'Groen', color: '#22c55e', battery: 38 },
    { id: 2, name: 'Rood', color: '#ef4444', battery: 38 },
    { id: 3, name: 'Blauw', color: '#3b82f6', battery: 38 },
    { id: 4, name: 'Geel', color: '#eab308', battery: 38 }
]);


// Use the game colors composable
const { buttonClass, colorVariant, cardBackgroundColor, primaryColor } = useGameColors(gameId);

const selectDifficulty = (difficulty) => {
    selectedDifficulty.value = difficulty;
};

</script>

<template>
    <main class="c-content-wrapper u-justify-center u-viewport-height-80">
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
            <TextInput v-model="username" placeholder="Voer je gebruikersnaam in" />
        </SettingContainer>
        <SettingContainer title="Gebruikte kleuren" layout="grid">
            <SmallPotjeCard 
                v-for="potje in colorPotjes.slice(0, colors)" 
                :key="potje.id"
                :name="potje.name" 
                :color="potje.color"
                :battery="potje.battery"
            />
        </SettingContainer>
        
        <RouterLink :class="buttonClass" :to="`/instructions/${gameId}`">Ga door</RouterLink>
    </main>
</template>

<style scoped>


.c-smallPotjeCard {
    display: flex;
    padding: var(--spacing-baseline);
    background-color: var(--white);
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    border-radius: var(--radius-s);
}

.c-smallPotjeCard__section {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: var(--spacing-03);
}

.c-smallPotjeCard__section--battery {
    gap: var(--spacing-02);
}

.c-smallPotjeCard__color {
    width: 1.5rem;
    height: 1.5rem;
    border-radius: 50%;
}

.c-battery-icon {
    color: var(--grey-85);
    width: 1.5rem;
    height: 1.5rem;
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