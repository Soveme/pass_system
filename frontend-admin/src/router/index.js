import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Passes from '../views/Passes.vue'
import Statistics from '../views/Statistics.vue'
import Users from '../views/Users.vue'
import AuditLog from '../views/AuditLog.vue'

const routes = [
  {
    path: '/login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: Dashboard,
    meta: { requiresAuth: true }
  },
  {
    path: '/passes',
    component: Passes,
    meta: { requiresAuth: true }
  },
  {
    path: '/statistics',
    component: Statistics,
    meta: { requiresAuth: true }
  },
  {
    path: '/users',
    component: Users,
    meta: { requiresAuth: true }
  },
  {
    path: '/audit',
    component: AuditLog,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
