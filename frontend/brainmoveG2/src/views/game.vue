<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const gameId = ref(route.params.id);

</script>

<template>
    <main class="c-content-wrapper">
        <h1>Game {{ gameId }}</h1>
    </main>
</template>

<style scoped>

</style>