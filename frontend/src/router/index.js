import { createRouter, createWebHistory } from 'vue-router'
import DetectorView from '@/views/DetectorView.vue'
import FallacyView from '@/views/FallacyView.vue'
import GameView from '@/views/GameView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'detector',
      component: DetectorView,
    },
    {
      path: '/logical-fallacies',
      name: 'fallacies',
      component: FallacyView,
    },
    {
      path: '/game',
      name: 'game',
      component: GameView,
    },
  ],
})

export default router
