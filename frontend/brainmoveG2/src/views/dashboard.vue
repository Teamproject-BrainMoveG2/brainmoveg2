
<script setup>
import { ref, onMounted } from 'vue';
import GameCard from '../components/cards/GameCard.vue';

const modes = ref([]);
const Ip = `${window.location.hostname}:8000`;


async function fetchGames() {
    try {
        const response = await fetch(`http://${Ip}/modes`);
        if (!response.ok) throw new Error('Failed to fetch modes');
        modes.value = await response.json();
    } catch (e) {
        modes.value = [];
    }
}

onMounted(fetchGames);
</script>

<template>
    <main class="c-content-wrapper">
        <div class="c-title">
            <h1>Kies je gamemode</h1>
        </div>
        
        <div class="c-game-grid">
            <GameCard
                v-for="mode in modes"
                :key="mode.spelmodus_id"
                :title="mode.naam"
                :gameId="mode.spelmodus_id.toString()"
                :description="mode.description"
                :icon="mode.icon"
            />
        </div>
    </main>
</template>

<style scoped>
.c-title {
    text-align: start;
    width: 100%;
}

.c-game-grid {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-06);
    width: 100%;
}

@media (min-width: 768px) {
    .c-game-grid {
        gap: var(--spacing-07);
    }
}
</style>