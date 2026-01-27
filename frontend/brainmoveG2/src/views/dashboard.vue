
<script setup>
import { onMounted } from 'vue';
import GameCard from '../components/cards/GameCard.vue';
import { useGames } from '../composables/useGames';

const { modes, fetchGames } = useGames();

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

    @media (min-width: 768px) {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: 1fr 1fr;
        gap: var(--spacing-06);
    }

}
</style>