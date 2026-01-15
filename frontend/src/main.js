// Force console output
window.addEventListener('error', (e) => {
  console.error('Global error:', e.error, e.message, e.filename, e.lineno)
})

console.log('=== main.js START ===')
console.log('Current URL:', window.location.href)
console.log('Document ready state:', document.readyState)
console.log('App element exists:', !!document.getElementById('app'))

import { createApp } from 'vue'
console.log('Vue imported')

import { createPinia } from 'pinia'
console.log('Pinia imported')

import App from './App.vue'
console.log('App component imported')

import router from './router'
console.log('Router imported')

console.log('Creating Vue app instance...')
const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

console.log('Mounting Vue app to #app...')
const appElement = document.getElementById('app')
console.log('App element:', appElement)

app.mount('#app')
console.log('=== Vue app mounted successfully ===')

