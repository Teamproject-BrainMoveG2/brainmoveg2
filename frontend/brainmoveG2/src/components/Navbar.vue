<script setup>
import { Home, TrendingUp, Info } from 'lucide-vue-next'
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <nav class="c-navbar">
    <router-link to="/dashboard" class="c-navbar__item small-body" :class="{ active: route.path === '/dashboard' }">
      <Home :size="24" />
      <span class="c-navbar__text">Home</span>
    </router-link>
    
    <router-link to="/resultaten" class="c-navbar__item small-body" :class="{ active: route.path === '/resultaten' }">
      <TrendingUp :size="24" />
      <span class="c-navbar__text">Resultaten</span>
    </router-link>
    
    <router-link to="/info" class="c-navbar__item small-body" :class="{ active: route.path === '/info' }">
      <Info :size="24" />
      <span class="c-navbar__text">Info</span>
    </router-link>
  </nav>
</template>

<style scoped>
.c-navbar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  align-items: center;
  background: var(--white);
  padding: var(--spacing-04) 0;
  z-index: 100;
}

.c-navbar__item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-01);
  text-decoration: none;
  color: var(--grey-40);
  transition: color 0.2s;
  padding: var(--spacing-03) var(--spacing-06);
  border-bottom: 3px solid transparent;
  position: relative;
}

.c-navbar__text {
  font-weight: var(--font-weight-medium);
}

.c-navbar__item.active {
  color: var(--primary);
  border-bottom-color: var(--primary);
}

.c-navbar__item:hover {
  color: var(--primary);
}
</style>
