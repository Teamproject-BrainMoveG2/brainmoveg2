<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Clock, RotateCw, Target, Trophy } from 'lucide-vue-next';
import { useGameColors } from '../composables/useGameColors';

const route = useRoute();
const router = useRouter();
const gameId = ref(route.params.id);
const gameStats = ref(null);

// Use the game colors composable
const { buttonClass, colorVariant, cardBackgroundColor, primaryColor } = useGameColors(gameId);

onMounted(() => {
    // Get the game stats from navigation state
    if (history.state && history.state.gameStats) {
        gameStats.value = history.state.gameStats;
        console.log('Game stats received:', gameStats.value);
    }
});

const formatTime = (milliseconds) => {
    const seconds = Math.floor(milliseconds / 1000);
    const ms = milliseconds % 1000;
    return `${seconds}.${ms.toString().padStart(3, '0')}s`;
};

const formatTimeMinutes = (milliseconds) => {
    const totalSeconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
};

const accuracy = computed(() => {
    if (!gameStats.value) return 0;
    const total = gameStats.value.correct_hits + gameStats.value.wrong_hits + gameStats.value.missed_hits;
    if (total === 0) return 0;
    return Math.round((gameStats.value.correct_hits / total) * 100);
});

const goToDashboard = () => {
    router.push('/dashboard');
};
</script>

<template>
    <main class="c-content-wrapper">
        <div class="c-title-div">
            <h1>Speloverzicht</h1>
            <p class="body-large">Totale tijd: {{ gameStats ? formatTimeMinutes(gameStats.total_time_ms) : '0:00' }}</p>
        </div>
        <div class="c-stats-grid">
            <div class="c-stat-card">
                <p class="c-stat-label">Avg. snelheid</p>
                <div class="c-stats-content">
                    <Clock :size="32" class="c-stat-icon" />
                    <p class="c-stat-value">{{ gameStats ? Math.round(gameStats.average_reaction_speed_ms) : 0 }}MS</p>
                </div>
            </div>
            
            <div class="c-stat-card">
                <p class="c-stat-label">Aantal rondes</p>
                <div class="c-stats-content">
                    <RotateCw :size="32" class="c-stat-icon" />
                    <p class="c-stat-value">{{ gameStats ? gameStats.total_rounds : 0 }}</p>
                </div>
            </div>
            
            <div class="c-stat-card">
                <p class="c-stat-label">Accuracy</p>
                <div class="c-stats-content">
                    <Target :size="32" class="c-stat-icon" />
                    <p class="c-stat-value">{{ accuracy }}%</p>
                </div>
            </div>
            
            <div class="c-stat-card">
                <p class="c-stat-label">Niveau</p>
                <div class="c-stats-content">
                     <Trophy :size="32" class="c-stat-icon" />
                     <p class="c-stat-value">PRO</p>
                </div>
               
            </div>
        </div>
        <div class="c-results-container">
            <div class="c-result-card c-result-card--correct">
                <p>Correct: {{ gameStats ? gameStats.correct_hits : 0 }}</p>
            </div>
            <div class="c-result-card c-result-card--fout">
                <p>Fout: {{ gameStats ? gameStats.wrong_hits : 0 }}</p>
            </div>
            <div class="c-result-card c-result-card--gemist">
                <p>Gemist: {{ gameStats ? gameStats.missed_hits : 0 }}</p>
            </div>
        </div>
        <RouterLink :class="buttonClass" :to="`/game/${gameId}`">Spel opnieuw spelen!</RouterLink>
    </main>
</template>

<style>
.c-title-div {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-baseline);
}

.c-stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    margin-top: var(--spacing-xlarge);
    width: 100%;
}

.c-stat-card {
    text-align: center;
    background-color: var(--white);
    padding: 16px;
    border-radius: var(--radius-s);
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-height: 140px;
    box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.1);
}

.c-stat-card:nth-child(1),
.c-stat-card:nth-child(4) {
    background-color: var(--primary-light);
}

.c-stats-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex: 1;
    gap: 8px;
    align-items: center;
    gap: 4px;
}


.c-stat-icon {
    width: 32px;
    height: 32px;
    color: var(--text-primary);
}

.c-stat-value {
    font-family: "Bebas Neue", sans-serif;
    font-size: 32px;
    font-weight: 700;
    line-height: 40px;
    color: var(--text-primary);
    margin: 0;
}

.c-results-container {
    display: flex;
    width: 100%;
    flex-wrap: wrap;
}

.c-result-card {
    flex: 1;
    padding: var(--spacing-03);
    text-align: center;
}

.c-result-card p {
    font-size: var(--font-size-3);
    font-weight: var(--font-weight-regular);
    margin: 0;
}

.c-result-card--correct {
    background-color: var(--accent-green-light);
    color: var(--grey-90);
    border-radius: var(--radius-s) 0 0 var(--radius-s);
}

.c-result-card--fout {
    background-color: var(--red-light);
    color: var(--grey-90);
    border-radius: 0;
}

.c-result-card--gemist {
    background-color: var(--accent-orange-light);
    color: var(--grey-90);
    border-radius: 0 var(--radius-s) var(--radius-s) 0;
}
</style>