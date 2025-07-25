import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'ClassicEditor',
    component: () => import('../views/Editor.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router