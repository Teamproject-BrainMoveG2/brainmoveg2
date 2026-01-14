<script setup>
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const gameId = ref(route.params.id);

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

</script>

<template>
    <main class="c-content-wrapper">
        <h1>Game Settings</h1>
        <RouterLink :class="buttonClass" :to="`/instructions/${gameId}`">Ga door</RouterLink>
    </main>

</template>

<style scoped>

</style>