import { createRouter, createWebHistory } from 'vue-router'
import DetectorView from '@/views/DetectorView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'detector',
      component: DetectorView,
    },
    
  ],
})

export default router
