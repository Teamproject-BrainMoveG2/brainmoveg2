<script setup>
import { Home, TrendingUp, Info } from 'lucide-vue-next'
import { useRoute } from 'vue-router'
import BellNotification from '../BellNotification.vue';

const route = useRoute()
</script>

<template>
  <nav class="c-navbar">
    <div class="c-navbar__content">
      <div class="c-navbar__logo">
        <h2>Brainmove</h2>
      </div>
      <div class="c-navbar__links">
        <router-link to="/dashboard" class="c-navbar__item small-body" :class="{ active: route.path === '/dashboard' }">
          <Home :size="24" class="c-navbar__icon" />
          <span class="c-navbar__text">Home</span>
        </router-link>
        
        <router-link to="/resultaten" class="c-navbar__item small-body" :class="{ active: route.path === '/resultaten' }">
          <TrendingUp :size="24" class="c-navbar__icon" />
          <span class="c-navbar__text">Resultaten</span>
        </router-link>
        
        <router-link to="/info" class="c-navbar__item small-body" :class="{ active: route.path === '/info' }">
          <Info :size="24" class="c-navbar__icon" />
          <span class="c-navbar__text">Info</span>
        </router-link>
        <div class="c-navbar__notification">
          <BellNotification />
        </div>
    </div>
  </div>
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
  padding-bottom: 0;
  z-index: 100;
  border-radius: var(--radius);

  @media (min-width: 768px) {

    position: relative;
    justify-content: flex-start;
    width: 100%;
    padding: var(--spacing-05) var(--spacing-08);

  }
}
.c-navbar__logo{
display: none;

@media (min-width: 768px) {
  display: inline;
}
}
 

.c-navbar__content {
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: 100%;
  max-width: 26.25rem;

  @media (min-width: 768px) {

    max-width: 100%;
    justify-content: space-between;

  }
}

.c-navbar__links {
  display: flex;
  justify-content: space-around;
  align-items: center;
  width: 100%;

  @media (min-width: 768px) {
    width: auto;
    justify-content: flex-start;
    gap: var(--spacing-06);


  }
}

.c-navbar__notification {
  display: none;

  @media (min-width: 768px) {
    display: inline;
    margin-left: var(--spacing-04);
  }
}


.c-navbar__item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-01);
  text-decoration: none;
  font-size: var(--font-size-3);
  color: var(--grey-80);
  transition: color 0.2s, transform 0.25s cubic-bezier(0.4, 0.2, 0.2, 1);
  padding: var(--spacing-03) var(--spacing-04);
  border-bottom: 3px solid transparent;
  position: relative;
}

.c-navbar__icon {
  @media (min-width: 768px) {
  display: none;
  }
}

/* Add a pseudo-element for the border to allow opacity fade */
.c-navbar__item::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 3px;
  background: var(--primary);
  opacity: 0;
  transition: opacity 0.3s cubic-bezier(0.4, 0.2, 0.2, 1);
  pointer-events: none;
  border-radius: 2px 2px 0 0;
  z-index: 1;
}

.c-navbar__text {
  font-weight: var(--font-weight-medium);
}


.c-navbar__item.active {
  color: var(--primary);
  border-bottom-color: transparent;
  transform: translateY(-8px) scale(1.08);
  z-index: 2;

  @media (min-width: 768px) {
    transform: scale(1);
  }

}
.c-navbar__item.active::after {
  opacity: 1;
}

.c-navbar__item:hover {
  color: var(--primary);
}
</style>
