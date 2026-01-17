<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Clock, RotateCw, Target, Trophy } from 'lucide-vue-next';
import { useGameColors } from '../composables/useGameColors';
import StatCard from '../components/cards/StatCard.vue';

const route = useRoute();
const router = useRouter();
const gameId = ref(route.params.id);
const gameStats = ref(null);
const activeTab = ref('speloverzicht');

// Use the game colors composable
const { buttonClass, colorVariant, cardBackgroundColor, primaryColor } = useGameColors(gameId);

onMounted(() => {
    // Get the game stats from navigation state
    if (history.state && history.state.gameStats) {
        gameStats.value = history.state.gameStats;
        console.log('Game stats received:', gameStats.value);
    }
});

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


const openContent = (tabName) => {
    activeTab.value = tabName;
};

</script>

<template>
    <div class="c-overzichttab">
        <button 
            class="c-tabGame body-large" 
            :class="{ 'c-tabGame--active': activeTab === 'scoreboard' }"
            @click="openContent('scoreboard')"
        >
            Scoreboard
        </button>
        <button 
            class="c-tabGame body-large" 
            :class="{ 'c-tabGame--active': activeTab === 'speloverzicht' }"
            @click="openContent('speloverzicht')"
        >
            Speloverzicht
        </button>
    </div>
    <main v-show="activeTab === 'speloverzicht'" class="c-content-wrapper u-justify-center u-viewport-height-80">
        <div class="c-title-div">
            <h1>Speloverzicht</h1>
            <p class="body-large">Totale tijd: {{ gameStats ? formatTimeMinutes(gameStats.total_time_ms) : '0:00' }}</p>
        </div>
        <div class="c-stats-grid">
            <StatCard 
                label="Avg. snelheid" 
                :value="`${gameStats ? Math.round(gameStats.average_reaction_speed_ms) : 0}MS`"
                :icon="Clock"
            />
            
            <StatCard 
                label="Aantal rondes" 
                :value="gameStats ? gameStats.total_rounds : 0"
                :icon="RotateCw"
            />
            
            <StatCard 
                label="Accuracy" 
                :value="`${accuracy}%`"
                :icon="Target"
            />
            
            <StatCard 
                label="Niveau" 
                value="PRO"
                :icon="Trophy"
            />
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
    <main v-show="activeTab === 'scoreboard'" class="c-content-wrapper u-justify-center u-viewport-height-80">
        <div class="c-title-div">
            <h1>Game name</h1>
        </div>
        <div class="c-scoreCircle">
            <div class="c-scoreCircle__inner">
                <h1 class="c-scoreCircle__number">5454</h1>
                <h2 class="c-scoreCircle__text">uw score</h2>
            </div>
            
        </div>
    </main>
</template>

<style>

.c-scoreCircle {
    width: 11.25rem;
    height: 11.25rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-04);
    border: 3px solid var(--primary);
    margin: 2rem auto;
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

.c-overzichttab {
    padding: 0 var(--spacing-06);
  display: flex;
  flex-direction: row;
  align-items: center;
  max-width: 26.25rem;
  margin: 0 auto;
  margin-top: 2rem;


  @media (min-width: 768px) {

    max-width: 500px;
    gap: var(--spacing-08);

  }

  @media (min-width: 1024px) {

      max-width: 550px;
      gap: var(--spacing-09);

  }
}

.c-tabGame{
    background: none;
    cursor: pointer;
    outline: inherit;
    padding-bottom: var(--spacing-05);
    border: none;
    border-bottom: 3px solid var(--grey-15);
    text-align: center;
    width: 100%;
    transition: border-color 0.2s ease;
}

.c-tabGame--active{
    border-bottom: 3px solid var(--primary);
}

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