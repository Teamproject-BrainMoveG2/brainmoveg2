<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const gameId = ref(route.params.id);

</script>

<template>
    <main class="c-content-wrapper">
        <h1>Game Settings</h1>
        <RouterLink class="c-btn c-btn--primary" :to="`/instructions/${gameId}`">Ga door</RouterLink>
    </main>

</template>

<style scoped>

</style>