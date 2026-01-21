<script setup>
import { RouterView, useRoute } from 'vue-router';
import { computed, ref } from 'vue';
import Navbar from './components/navigatie/Navbar.vue';
import Header from './components/navigatie/Header.vue';

const route = useRoute();
const showNavbar = computed(() => route.meta.showNavbar !== false);
const showHeader = computed(() => route.meta.showHeader !== false);

</script>


<template>
  <v-app>
    <Header v-if="showHeader" />
    <div :style="showNavbar ? 'padding-bottom: 100px;' : ''">
        <RouterView :key="route.fullPath" />
    </div>
    <Navbar v-if="showNavbar" />
  </v-app>
</template>

<style>
</style>

