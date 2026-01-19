<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Clock, RotateCw, Target, Trophy, Info, Medal } from 'lucide-vue-next';
import { useGameColors } from '../composables/useGameColors';
import StatCard from '../components/cards/StatCard.vue';
import ScoreboardRow from '../components/ScoreboardRow.vue';
import ScoreCircle from '../components/ScoreCircle.vue';

const route = useRoute();
const router = useRouter();
const gameId = ref(route.params.id);
const gameStats = ref(null);
const activeTab = ref('speloverzicht');
const scoreboardData = ref([
  { position: 1, name: 'Alice', score: 6500, isPlayer: false },
  { position: 2, name: 'Bob', score: 6200, isPlayer: false },
  { position: 3, name: 'Charlie', score: 6000, isPlayer: false },
  { position: 4, name: 'You', score: 5454, isPlayer: true },
]);

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

const playerScore = computed(() => {
    const player = scoreboardData.value.find(row => row.isPlayer);
    return player ? player.score : 0;
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
    <main v-show="activeTab === 'speloverzicht'" class="c-content-wrapper">
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
    <main v-show="activeTab === 'scoreboard'" class="c-content-wrapper ">
        <div class="c-title-div">
            <h1>Game name</h1>
        </div>
        <ScoreCircle :score="playerScore" />
        <div class="c-leaderboard">
            <div class="c-leaderboard__head">
                <p class="c-leaderboard__head-title">scoreboard</p>
                <Info class="c-leaderboard__head-icon"/>
            </div>
            <table class="c-table">
                <thead>
                    <tr class="c-table__headings">
                        <th >POS.</th>
                        <th >Naam</th>
                        <th >score</th>
                    </tr>
                </thead>
                <tbody>
                    <ScoreboardRow
                      v-for="(row, index) in scoreboardData"
                      :key="index"
                      :position="row.position"
                      :name="row.name"
                      :score="row.score"
                      :is-player="row.isPlayer"
                    />
                </tbody>
            </table>
        </div>
        <RouterLink :class="buttonClass" :to="``">Opnieuw spelen</RouterLink>
    </main>
</template>

<style>

.c-table{

    display: flex;
    flex-direction: column;
    width: 100%;
}

.c-table__headings {
    display: flex;
    justify-content: space-between;
    padding: var(--spacing-04);
    border-bottom: 2px solid var(--grey-95);
    font-size: var(--font-size-5);
    line-height: var(--font-size-6);
    font-family: "Bebas Neue", sans-serif;
    gap: var(--spacing-07);
    text-decoration: none;
}

th {
    font-weight: normal;
}

th:nth-child(1),
th:nth-child(3) {
    width: auto;
    flex-shrink: 0;
}

th:nth-child(2) {
    flex-grow: 1;
    text-align: left;
}

td:nth-child(1),
td:nth-child(3) {
    width: auto;
    flex-shrink: 0;
}

td:nth-child(2) {
    flex-grow: 1;
    text-align: left;
}

.c-table__row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-05) var(--spacing-04) ;
    border-bottom: 2px solid var(--grey-15);
    gap: var(--spacing-04);

    font-family: "Source Sans Pro", sans-serif;
    font-size: var(--font-size-3); 
    line-height: 1.5rem;
    font-weight: var(--font-weight-regular);
    letter-spacing: 0;
}

.c-table__row:nth-child(3) {
    border: none;
}

.c-table__row:nth-child(1) .c-table__trophy, .c-table__row:nth-child(1) .c-table__trophy-icon {

    border-color: var(--accent-orange);
    color: var(--accent-orange);
}

.c-table__row:nth-child(3) .c-table__trophy, .c-table__row:nth-child(3) .c-table__trophy-icon {

    border-color: var(--accent-orange-dark);
    color: var(--accent-orange-dark);
}

.c-table__row--player{

    background-color: var(--primary-light);
    border-radius: var(--radius);
    border: none;

}

.c-table__trophy {
    display: flex;
    align-items: center;
    gap: var(--spacing-02);
    border: 1px solid var(--grey-85);
    padding: var(--spacing-02) var(--spacing-03);
    border-radius: var(--radius-s);
}

.c-table__trophy--player {
    border: none;
    
}

.c-table__trophy-icon {
    width: .875rem;
    height: .875rem;
} 

.c-leaderboard {
    display: flex;
    flex-direction: column;
    text-align: start;
    width: 100%;
    box-sizing: border-box;
    gap: var(--spacing-04);
    border-radius: var(--radius-s);
}

.c-leaderboard__head {
   display: flex;
   flex-direction: row;
   justify-content: space-between;
    padding: 0 var(--spacing-04);
}

.c-leaderboard__head-title{
    font-size: var(--font-size-5);
    line-height: var(--font-size-6);
    font-family: "Bebas Neue", sans-serif;

}

.c-leaderboard__head-icon{
    width: 1.5rem;
    height: 1.5rem;
    
}

.c-overzichttab {
    padding: 0 var(--spacing-06);
  display: flex;
  flex-direction: row;
  align-items: center;
  max-width: 26.25rem;
  margin: 0 auto;
  padding-top: 2rem;
  margin-bottom: 2rem;
  


  @media (min-width: 768px) {

    max-width: 500px;
   

  }

  @media (min-width: 1024px) {

      max-width: 550px;
    

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