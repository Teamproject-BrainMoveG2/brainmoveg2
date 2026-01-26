<script setup>
import { RouterView, useRoute } from 'vue-router';
import { computed, ref, onMounted, onUnmounted } from 'vue';
import Navbar from './components/navigatie/Navbar.vue';
import Header from './components/navigatie/Header.vue';

const route = useRoute();
const showNavbar = computed(() => route.meta.showNavbar !== false);
const showHeader = computed(() => route.meta.showHeader !== false);

const isMobileOrTablet = ref(window.innerWidth <= 1024);
const updateWidth = () => {
  isMobileOrTablet.value = window.innerWidth <= 1024;
};
onMounted(() => {
  window.addEventListener('resize', updateWidth);
});
onUnmounted(() => {
  window.removeEventListener('resize', updateWidth);
});

const contentStyle = computed(() => {
  return showNavbar.value && isMobileOrTablet.value
    ? 'padding-bottom: 80px;'
    : '';
});
</script>

<template>
  <Navbar v-if="showNavbar" />
  <transition name="fade" mode="out-in">
    <div :key="route.fullPath" class="page-content">
      <Header v-if="showHeader" />
      <div :style="contentStyle">
        <RouterView />
      </div>
    </div>
  </transition>
</template>

<style>
.page-content {
  width: 100%;
  height: 100%;
  background-color: var(--grey-2);
  flex-grow: 1;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
