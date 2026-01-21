<script setup>
import { useCones } from '../composables/useCones';
import { useGameColors } from '../composables/useGameColors';
import { useRoute, RouterLink } from 'vue-router';
import { ref,onMounted, computed } from 'vue';
import SettingContainer from '../components/SettingContainer.vue';
import DifficultyButton from '../components/buttons/DifficultyButton.vue';
import CounterButton from '../components/buttons/CounterButton.vue';
import TextInput from '../components/inputs/TextInput.vue';
import SmallPotjeCard from '../components/cards/SmallPotjeCard.vue';
import { useGames } from '../composables/useGames';

const getColorValue = (color) => {
    const colorMap = {
        'red': 'var(--red)',
        'blue': 'var(--blue)',
        'green': 'var(--accent-green)',
        'yellow': 'var(--yellow)',
        'orange': 'var(--accent-orange)'
    };
    return colorMap[color] || 'var(--accent-green)';
};

const route = useRoute();
const gameId = ref(route.params.id);
const selectedDifficulty = ref('relaxed');
const rounds = ref(10);
const colors = ref(4);
const username = ref('');

const difficulties = [
    { id: 'relaxed', label: 'Relaxed', color: 'green' },
    { id: 'challenging', label: 'Challenging', color: 'orange' },
    { id: 'intense', label: 'Intense', color: 'red' }
];

const { cones, colorToDutch } = useCones();
const { modes, fetchGames } = useGames();

const { buttonClass, colorVariant, cardBackgroundColor, primaryColor } = useGameColors(gameId);

const selectDifficulty = (difficulty) => {
    selectedDifficulty.value = difficulty;
};

onMounted(fetchGames);

function getInstructionsRoute() {
    return {
        name: 'instructions',
        params: { id: gameId.value },
        query: {
            username: username.value,
            mode_id: Number(gameId.value),
            difficulty_id: difficulties.findIndex(d => d.id === selectedDifficulty.value) + 1,
            aantal_rondes: rounds.value,
            aantal_kleuren: colors.value
        }
    };
}

function printInstructionsRoute(e) {
    const routeObj = getInstructionsRoute();
    console.log('RouterLink to:', JSON.stringify(routeObj, null, 2));
}

const limitedCones = computed(() => {
    if (!Array.isArray(cones.value)) return [];
    const num = typeof colors.value === 'number' ? colors.value : 0;
    const sorted = [...cones.value].sort((a, b) => (b.connected ? 1 : 0) - (a.connected ? 1 : 0));
    return sorted.slice(0, num);
});

</script>

<template>
    <main class="c-content-wrapper">
        <div class="c-title">
            <h1>{{ modes.find(mode => mode.spelmodus_id.toString() === gameId)?.naam || '' }}</h1>
            <p>{{ modes.find(mode => mode.spelmodus_id.toString() === gameId)?.description || '' }}</p>
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
                v-for="cone in limitedCones" 
                :key="cone.cone_id"
                :name="colorToDutch[cone.color] || cone.color" 
                :color="getColorValue(cone.color)"
                :battery="cone.battery_percentage"
                :isConnected="cone.connected"
            />
        </SettingContainer>
        
        <RouterLink
            :class="buttonClass"
            :to="getInstructionsRoute()"
            @click.native="printInstructionsRoute"
        >
            Ga door
        </RouterLink>
    
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