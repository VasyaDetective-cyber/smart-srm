<template>
  <section>
    <div v-if="loading" class="state-card"><span class="spinner"></span><p>{{ t('loading') }}</p></div>
    <div v-else-if="error" class="feedback error">{{ error }}</div>
    <template v-else-if="customer">
      <RouterLink class="back-link" to="/customers">{{ t('back') }}</RouterLink>
      <div class="details-heading"><div><span class="eyebrow">{{ t('details') }}</span><h1>{{ customer.name }}</h1></div><div><button class="ghost-btn" @click="goEdit">{{ t('edit') }}</button><button class="danger-btn" @click="showDelete = true">{{ t('delete') }}</button></div></div>
      <div class="details-grid"><article class="detail-card"><span class="detail-label">{{ t('companyInfo') }}</span><h3>{{ customer.name }}</h3><dl><div><dt>{{ t('industry') }}</dt><dd>{{ customer.industry || t('notSpecified') }}</dd></div><div><dt>{{ t('email') }}</dt><dd>{{ customer.email || t('notSpecified') }}</dd></div><div><dt>{{ t('phone') }}</dt><dd>{{ customer.phone || t('notSpecified') }}</dd></div><div><dt>{{ t('address') }}</dt><dd>{{ customer.address || t('notSpecified') }}</dd></div></dl></article><article class="detail-card"><span class="detail-label">{{ t('recordInfo') }}</span><dl><div><dt>{{ t('created') }}</dt><dd>{{ formatDate(customer.created_at) }}</dd></div><div><dt>{{ t('updated') }}</dt><dd>{{ formatDate(customer.updated_at) }}</dd></div><div><dt>{{ t('id') }}</dt><dd class="id-value">{{ customer.id }}</dd></div></dl></article></div>
      <div class="related-grid"><article class="related-card"><div class="related-head"><div><span class="detail-label">{{ t('relatedContacts') }}</span><h3>{{ contacts.length }}</h3></div><RouterLink class="ghost-btn" :to="`/contacts?customer_id=${customer.id}`">{{ t('viewAll') }}</RouterLink></div><div v-if="!contacts.length" class="related-empty">{{ t('noRelated') }}</div><RouterLink v-for="contact in contacts.slice(0, 5)" :key="contact.id" class="related-row" :to="`/contacts/${contact.id}`"><span class="company-avatar contact-avatar">{{ initials(contact) }}</span><span><strong>{{ contact.first_name }} {{ contact.last_name }}</strong><small>{{ contact.title || t('notSpecified') }}</small></span><span class="related-arrow">→</span></RouterLink><RouterLink class="related-add" :to="`/contacts?customer_id=${customer.id}&create=1`">＋ {{ t('addRelatedContact') }}</RouterLink></article><article class="related-card"><div class="related-head"><div><span class="detail-label">{{ t('relatedDeals') }}</span><h3>{{ deals.length }}</h3></div><RouterLink class="ghost-btn" :to="`/deals?customer_id=${customer.id}`">{{ t('viewAll') }}</RouterLink></div><div v-if="!deals.length" class="related-empty">{{ t('noRelated') }}</div><RouterLink v-for="deal in deals.slice(0, 5)" :key="deal.id" class="related-row" :to="`/deals/${deal.id}`"><span class="company-avatar deal-avatar">◇</span><span><strong>{{ deal.title }}</strong><small>{{ statusLabel(deal.status) }} · {{ formatAmount(deal.amount) }} {{ t('currency') }}</small></span><span class="related-arrow">→</span></RouterLink><RouterLink class="related-add" :to="`/deals?customer_id=${customer.id}&create=1`">＋ {{ t('addRelatedDeal') }}</RouterLink></article></div>
    </template>
    <div v-if="showDelete" class="modal-backdrop" @click.self="showDelete = false"><section class="modal-card confirm-card"><div class="warning-icon">!</div><h2>{{ t('deleteQuestion') }}</h2><p class="muted">{{ t('deleteText') }} <strong>{{ customer?.name }}</strong>.</p><div class="form-actions"><button class="ghost-btn" @click="showDelete = false">{{ t('cancel') }}</button><button class="danger-btn" :disabled="deleting" @click="remove">{{ deleting ? '…' : t('confirmDelete') }}</button></div></section></div>
  </section>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { customerService } from '../services/customers'
import { contactService } from '../services/contacts'
import { dealService } from '../services/deals'
import { t } from '../i18n'
import { formatDate } from '../date'

const route = useRoute(), router = useRouter(), customer = ref(null), contacts = ref([]), deals = ref([]), loading = ref(true), error = ref(''), showDelete = ref(false), deleting = ref(false)
const statuses = ['New', 'Qualified', 'Proposal', 'Negotiation', 'Won', 'Lost']
async function load() { try { customer.value = await customerService.get(route.params.id); const results = await Promise.allSettled([contactService.list('', customer.value.id, 0, 100), dealService.list({ customer_id: customer.value.id, skip: 0, limit: 100 })]); contacts.value = results[0].status === 'fulfilled' ? results[0].value : []; deals.value = results[1].status === 'fulfilled' ? results[1].value : [] } catch (e) { error.value = e.message } finally { loading.value = false } }
function goEdit() { router.push({ path: '/customers', query: { edit: customer.value.id } }) }
function initials(contact) { return `${contact.first_name?.[0] || ''}${contact.last_name?.[0] || ''}`.toUpperCase() }
function statusLabel(status) { return t(`status${status}`) }
function formatAmount(value) { return Number(value).toLocaleString(localStorage.getItem('smart_crm_locale') === 'en' ? 'en-US' : 'uk-UA', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }
async function remove() { deleting.value = true; try { await customerService.remove(customer.value.id); router.push('/customers') } catch (e) { error.value = e.message; showDelete.value = false } finally { deleting.value = false } }
onMounted(load)
</script>
