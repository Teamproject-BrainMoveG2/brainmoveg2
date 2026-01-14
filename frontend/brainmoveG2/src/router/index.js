import { createRouter, createWebHistory } from 'vue-router';
import onboarding from '../views/onboarding.vue';
import introductie from '../views/introductie.vue';
import dashboard from '../views/dashboard.vue';
import gamesettings from '../views/gamesettings.vue';
import instructions from '../views/instructions.vue';
import Game from '../views/Game.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Welkom',
      component: onboarding,
      meta: { showNavbar: false, showHeader: false }, 
    },
    {
      path: '/introductie',
      name: 'introductie',
      component: introductie,
      meta: { showNavbar: false, showHeader: true }, 
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: dashboard,
      meta: { showNavbar: true, showHeader: true }, 
    },
    {
      path: '/gamesettings/:id',
      name: 'gamesettings',
      component: gamesettings,
      meta: { showNavbar: true, showHeader: true }, 
    },
    {
      path: '/instructions/:id',
      name: 'instructions',
      component: instructions,
      meta: { showNavbar: false, showHeader: true }, 
    },
    {
      path: '/game/:id',
      name: 'game',
      component: Game,
      meta: { showNavbar: false, showHeader: true }, 
    },
  ],
})

export default router;