import { createRouter, createWebHistory } from 'vue-router'
import DetectorView from '@/views/DetectorView.vue'
import FallacyView from '@/views/FallacyView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'detector',
      component: DetectorView,
    },
    {
      path: '/',
      name: 'fallacies',
      component: FallacyView,
    },
    
  ],
})

export default router
