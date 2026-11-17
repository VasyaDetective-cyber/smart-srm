import { createRouter, createWebHistory } from 'vue-router'
import { token, getMe } from './api'
import Login from './views/Login.vue'
import CrmLayout from './layouts/CrmLayout.vue'
const Placeholder = { template: '<section class="page-card"><span class="eyebrow">SMART CRM</span><h1>{{ $route.name }}</h1><p class="muted">Розділ підготовлено для наступного етапу розробки.</p></section>' }
const router = createRouter({ history: createWebHistory(), routes: [{ path: '/login', component: Login }, { path: '/', component: CrmLayout, children: ['Dashboard','Customers','Contacts','Deals','Activities'].map(name => ({ path: name === 'Dashboard' ? '' : name.toLowerCase(), name, component: Placeholder })) }, { path: '/:pathMatch(.*)*', redirect: '/' }] })
router.beforeEach(async (to) => { if (to.path === '/login' && token.get()) return '/' ; if (to.path !== '/login' && !token.get()) return '/login'; if (to.path !== '/login') { try { await getMe() } catch { token.clear(); return '/login' } } })
export default router
