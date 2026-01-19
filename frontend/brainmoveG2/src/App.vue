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
  <Header v-if="showHeader" />
  <div :style="showNavbar ? 'padding-bottom: 100px;' : ''">
    <transition name="page-fade" mode="out-in">
      <RouterView :key="route.fullPath" />
    </transition>
  </div>
  <Navbar v-if="showNavbar" />
</template>

<style>
.page-fade-enter-active, .page-fade-leave-active {
  transition: opacity 0.35s cubic-bezier(0.4, 0.2, 0.2, 1);
}
.page-fade-enter-from, .page-fade-leave-to {
  opacity: 0;
}
.page-fade-enter-to, .page-fade-leave-from {
  opacity: 1;
}
</style>

