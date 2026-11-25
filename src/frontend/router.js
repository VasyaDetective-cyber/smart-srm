import { createRouter, createWebHistory } from 'vue-router'
import { token, getMe } from './api'
import Login from './views/Login.vue'
import CrmLayout from './layouts/CrmLayout.vue'
import Customers from './views/Customers.vue'
import CustomerDetails from './views/CustomerDetails.vue'
import Contacts from './views/Contacts.vue'
import ContactDetails from './views/ContactDetails.vue'
import Deals from './views/Deals.vue'
import DealDetails from './views/DealDetails.vue'
const Placeholder = { template: '<section class="page-card"><span class="eyebrow">SMART CRM</span><h1>{{ $route.name }}</h1><p class="muted">Розділ підготовлено для наступного етапу розробки.</p></section>' }
const router = createRouter({ history: createWebHistory(), routes: [{ path: '/login', component: Login }, { path: '/', component: CrmLayout, children: [{ path: '', name: 'Dashboard', component: Placeholder }, { path: 'customers', name: 'Customers', component: Customers }, { path: 'customers/:id', name: 'Customer Details', component: CustomerDetails }, { path: 'contacts', name: 'Contacts', component: Contacts }, { path: 'contacts/:id', name: 'Contact Details', component: ContactDetails }, { path: 'deals', name: 'Deals', component: Deals }, { path: 'deals/:id', name: 'Deal Details', component: DealDetails }, { path: 'activities', name: 'Activities', component: Placeholder }] }, { path: '/:pathMatch(.*)*', redirect: '/' }] })
router.beforeEach(async (to) => { if (to.path === '/login' && token.get()) return '/' ; if (to.path !== '/login' && !token.get()) return '/login'; if (to.path !== '/login') { try { await getMe() } catch { token.clear(); return '/login' } } })
export default router
