<script setup>
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'
import Navbar from './components/navigatie/Navbar.vue'
import Header from './components/navigatie/Header.vue'


const route = useRoute()
const showNavbar = computed(() => route.meta.showNavbar !== false)
const showHeader = computed(() => route.meta.showHeader !== false)
</script>

<template>
  <Header v-if="showHeader" />
  <RouterView />
  <Navbar v-if="showNavbar" />
</template>

<style scoped>

</style>
