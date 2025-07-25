import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'IntegratedEditor',
    component: () => import('../views/IntegratedEditor.vue')
  },
  {
    path: '/classic-editor',
    name: 'ClassicEditor',
    component: () => import('../views/Editor.vue')
  },
  {
    path: '/outline',
    name: 'Outline',
    component: () => import('../views/Outline.vue')
  },
  {
    path: '/reference',
    name: 'Reference',
    component: () => import('../views/Reference.vue')
  },
  {
    path: '/academic',
    name: 'AcademicStructure',
    component: () => import('../views/AcademicStructure.vue')
  },
  {
    path: '/style',
    name: 'StyleAdjustment',
    component: () => import('../views/StyleAdjustment.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router