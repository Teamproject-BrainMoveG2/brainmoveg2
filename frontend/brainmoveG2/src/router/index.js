import { createRouter, createWebHistory } from 'vue-router';
import onboarding from '../views/onboarding.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Welkom',
      component: onboarding,
    },
  ],
})

export default router
