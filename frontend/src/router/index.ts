import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home-simple.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: {
      title: 'GitHub Trending Reporter'
    }
  },
  {
    path: '/projects/:date',
    name: 'ProjectList',
    component: () => import('../views/ProjectList.vue'),
    meta: {
      title: '项目列表 - GitHub Trending Reporter'
    }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue'),
    meta: {
      title: '关于我们 - GitHub Trending Reporter'
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

// 路由守卫 - 设置页面标题
router.beforeEach((to) => {
  document.title = to.meta.title as string || 'GitHub Trending Reporter'
})

export default router