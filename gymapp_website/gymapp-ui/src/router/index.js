import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

import WorkoutsPage from '@/pages/workouts.vue'
import AnalysisPage from '@/pages/analysis.vue'
import UsersPage from '@/pages/users.vue'

const routes = [
  {
    path: '/',
    name: 'Users',
    component: UsersPage
  },
  {
    path: '/workouts',
    name: 'Workouts',
    component: WorkoutsPage,
    meta: { requiresAuth: true }
  },
  {
    path: '/workouts/summary/:id',
    name: 'WorkoutSummary',
    component: () => import('@/pages/workout-summary.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: AnalysisPage,
    meta: { requiresAuth: true }
  }  
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/')
  } else {
    next()
  }
})

export default router