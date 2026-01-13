import { createRouter, createWebHistory } from 'vue-router';
import onboarding from '../views/onboarding.vue';
import introductie from '../views/introductie.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Welkom',
      component: onboarding,
      meta: { showNavbar: false, }, 
    },
    {
      path: '/introductie',
      name: 'introductie',
      component: introductie,
      meta: { showNavbar: false, showHeader: true }, 
    },
  ],
})

export default router;