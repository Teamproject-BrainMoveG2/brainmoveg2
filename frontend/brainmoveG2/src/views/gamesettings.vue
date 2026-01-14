<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const gameId = ref(route.params.id);
const selectedDifficulty = ref('relaxed');

const difficulties = [
    { id: 'relaxed', label: 'Relaxed', color: 'green' },
    { id: 'challenging', label: 'Challenging', color: 'orange' },
    { id: 'intense', label: 'Intense', color: 'red' }
];

// Get the color variant based on game ID
const colorVariant = computed(() => {
    const colorMap = {
        '1': 'green',
        '2': 'orange',
        '3': 'primary'
    };
    return colorMap[gameId.value] || 'primary'; // Default to blue
});

// Get the button class based on game ID
const buttonClass = computed(() => {
    return `c-btn c-btn--${colorVariant.value}`;
});

const selectDifficulty = (difficulty) => {
    selectedDifficulty.value = difficulty;
};

</script>

<template>
    <main class="c-content-wrapper">
        <div class="c-title">
            <h1>Game</h1>
        </div>
        <div>
            <p>Description</p>
        </div>
        <div class="c-difficulty-selector">
            <p>Selecteer moeilijkheid</p>
            <div class="c-difficulty-options">
                <button 
                    v-for="difficulty in difficulties" 
                    :key="difficulty.id"
                    :class="['c-difficulty-option', `c-difficulty--${difficulty.color}`, { 'is-active': selectedDifficulty === difficulty.id }]"
                    @click="selectDifficulty(difficulty.id)"
                >
                    <p>{{ difficulty.label }}</p>
                    <div class="c-difficulty-bars">
                        <span class="c-bar c-bar--first" :class="[`c-bar--${difficulty.color}`, { 'is-filled': true }]"></span>
                        <span class="c-bar c-bar--middle" :class="[`c-bar--${difficulty.color}`, { 'is-filled': difficulty.id === 'challenging' || difficulty.id === 'intense' }]"></span>
                        <span class="c-bar c-bar--last" :class="[`c-bar--${difficulty.color}`, { 'is-filled': difficulty.id === 'intense' }]"></span>
                    </div>
                </button>
            </div>
        </div>
        <div class="c-settingOptions">

        </div>
        <RouterLink :class="buttonClass" :to="`/instructions/${gameId}`">Ga door</RouterLink>
    </main>
</template>

<style scoped>

.c-title{
    text-align: left;
    width: 100%;
  }

.c-settingOptions{
    display: flex;
    flex-direction: column;
    gap: var(--spacing-05);
    width: 100%;
    margin-bottom: var(--spacing-06);
}

.c-difficulty-selector {
    width: 100%;
    gap: var(--spacing-baseline);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

.c-difficulty-options {
    display: flex;
    gap: var(--spacing-04);
    width: 100%;
}

.c-difficulty-option {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-03);
    padding: var(--spacing-03) var(--spacing-05);
    background-color: var(--grey-2);
    border: 2px solid transparent;
    border-radius: var(--radius-s);
    cursor: pointer;
    transition: all 0.3s ease;
    color: var(--grey-85);
}

.c-difficulty-option.is-active {
    border-color: currentColor;
}

.c-difficulty--green.is-active {
    color: var(--accent-green);
}

.c-difficulty--orange.is-active {
    color: var(--accent-orange);
}

.c-difficulty--red.is-active {
    color: var(--red);
}

.c-difficulty-bars {
    display: flex;
    gap: var(--spacing-02);
}

.c-bar {
    width: 20px;
    height: 5px;
    background: var(--white);
    border-radius: 0;
}

.c-bar--first {
    border-radius: 999px 0 0 999px;
}

.c-bar--middle {
    border-radius: 0;
}

.c-bar--last {
    border-radius: 0 999px 999px 0;
}

.c-bar--green {
    border: 2px solid var(--accent-green);
}

.c-bar--orange {
    border: 2px solid var(--accent-orange);
}

.c-bar--red {
    border: 2px solid var(--red);
}

.c-bar--green.is-filled {
    background: var(--accent-green);
}

.c-bar--orange.is-filled {
    background: var(--accent-orange);
}

.c-bar--red.is-filled {
    background: var(--red);
}

/* Wrap difficulty options on small screens */
@media (max-width: 410px) {
    .c-difficulty-options {
        flex-wrap: wrap;
    }
}

</style>