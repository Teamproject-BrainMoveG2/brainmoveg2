<script setup>
import GameCard from '../components/cards/GameCard.vue';
</script>

<template>
    <main class="c-content-wrapper">
        <div class="c-title">
            <h1>Kies je gamemode</h1>
        </div>
        
        <div class="c-game-grid">
            <GameCard 
                title="Speed reflex game"
                gameId= "1"
                description="Raak de juiste kleur aan binnen het tijdslimiet"
                backgroundColor="var(--accent-green-light)"
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