import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Reservations from '../views/Reservations.vue'
import Calendar from '../views/Calendar.vue'
import Rooms from '../views/Rooms.vue'
import Customers from '../views/Customers.vue'
import Revenue from '../views/Revenue.vue'
import Cleaning from '../views/Cleaning.vue'
import Admins from '../views/Admins.vue'

console.log('Router initializing...')

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/reservations',
    name: 'Reservations',
    component: Reservations
  },
  {
    path: '/calendar',
    name: 'Calendar',
    component: Calendar
  },
  {
    path: '/rooms',
    name: 'Rooms',
    component: Rooms
  },
  {
    path: '/customers',
    name: 'Customers',
    component: Customers
  },
  {
    path: '/revenue',
    name: 'Revenue',
    component: Revenue
  },
  {
    path: '/cleaning',
    name: 'Cleaning',
    component: Cleaning
  },
  {
    path: '/admins',
    name: 'Admins',
    component: Admins
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

