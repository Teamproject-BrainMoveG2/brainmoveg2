<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Clock, RotateCw, Target, Trophy } from 'lucide-vue-next';

const route = useRoute();
const router = useRouter();
const gameId = ref(route.params.id);
const gameStats = ref(null);

onMounted(() => {
    // Get the game stats from navigation state
    if (history.state && history.state.gameStats) {
        gameStats.value = history.state.gameStats;
    }
});

const formatTime = (milliseconds) => {
    const seconds = Math.floor(milliseconds / 1000);
    const ms = milliseconds % 1000;
    return `${seconds}.${ms.toString().padStart(3, '0')}s`;
};

const goToDashboard = () => {
    router.push('/dashboard');
};
</script>

<template>
    <main class="c-content-wrapper">
        <div class="c-title-div">
            <h1>Speloverzicht</h1>
            <p class="body-large"> totale tijd: 5:16</p>
        </div>
        <div class="c-stats-grid">
            <div class="c-stat-card">
                <p class="c-stat-label">Avg. snelheid</p>
                <div class="c-stats-content">
                    <Clock :size="32" class="c-stat-icon" />
                    <p class="c-stat-value">850MS</p>
                </div>
            </div>
            
            <div class="c-stat-card">
                <p class="c-stat-label">Aantal rondes</p>
                <div class="c-stats-content">
                    <RotateCw :size="32" class="c-stat-icon" />
                    <p class="c-stat-value">10</p>
                </div>
                
            </div>
            
            <div class="c-stat-card">
                <p class="c-stat-label">Accuracy</p>
                <div class="c-stats-content">
                    <Target :size="32" class="c-stat-icon" />
                    <p class="c-stat-value">67%</p>
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
    font-size: 32px;
    font-weight: 700;
    line-height: 40px;
    color: var(--text-primary);
    margin: 0;
}
</style>