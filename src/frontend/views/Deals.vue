<template>
  <section class="workspace-page">
    <div class="customer-actions action-only deals-body-actions"><button class="primary-btn add-btn" @click="openCreate">{{ t('addDeal') }}</button></div>
    <div v-if="error" class="feedback error">{{ error }}</div>
    <div class="filter-bar deal-filters"><div class="search-box"><span aria-hidden="true"><Icon name="search" /></span><input v-model="filters.search" @input="onSearch" :placeholder="t('searchDeals')" :aria-label="t('searchDeals')" /></div><select v-model="filters.status" @change="refresh"><option value="">{{ t('allStatuses') }}</option><option v-for="status in statuses" :key="status" :value="status">{{ statusLabel(status) }}</option></select><select v-model="filters.customer_id" @change="refresh"><option value="">{{ t('allCustomers') }}</option><option v-for="customer in customers" :key="customer.id" :value="customer.id">{{ customer.name }}</option></select><select v-if="isAdmin" v-model="filters.owner_id" @change="refresh"><option value="">{{ t('allOwners') }}</option><option v-for="owner in owners" :key="owner.id" :value="owner.id">{{ owner.full_name }}</option></select></div>
    <div class="deal-advanced-filters"><label><span>{{ t('minAmountShort') }}</span><input v-model.number="filters.min_amount" type="number" min="0" step="0.01" /></label><label><span>{{ t('maxAmountShort') }}</span><input v-model.number="filters.max_amount" type="number" min="0" step="0.01" /></label><label><span>{{ t('minProbabilityShort') }}</span><input v-model.number="filters.min_probability" type="number" min="0" max="100" /></label><label><span>{{ t('maxProbabilityShort') }}</span><input v-model.number="filters.max_probability" type="number" min="0" max="100" /></label><label><span>{{ t('dateFrom') }}</span><input v-model="filters.date_from" type="date" lang="uk-UA" /></label><label><span>{{ t('dateTo') }}</span><input v-model="filters.date_to" type="date" lang="uk-UA" /></label><button class="ghost-btn filter-apply" @click="refresh">{{ t('applyFilters') }}</button><button v-if="hasFilters()" class="ghost-btn filter-clear" @click="clearFilters">{{ t('clearFilters') }}</button></div>
    <div v-if="loading" class="state-card"><span class="spinner"></span><p>{{ t('loading') }}</p></div>
    <div v-else-if="!displayedDeals.length" class="state-card"><div class="empty-icon">◇</div><h3>{{ hasFilters() ? t('noDealResults') : t('noDeals') }}</h3><p class="muted">{{ filters.search ? t('tryAgain') : t('manage') }}</p><button v-if="!hasFilters()" class="primary-btn compact" @click="openCreate">{{ t('addFirstDeal') }}</button></div>
    <div v-else class="table-card"><div class="table-wrap"><table><thead><tr><th>{{ t('dealTitle') }}</th><th>{{ t('dealCustomer') }}</th><th>{{ t('amount') }}</th><th>{{ t('probability') }}</th><th>{{ t('status') }}</th><th>{{ t('expectedCloseColumn') }}</th><th class="actions-col">{{ t('actions') }}</th></tr></thead><tbody><tr v-for="deal in displayedDeals" :key="deal.id"><td><RouterLink class="company-link" :to="`/deals/${deal.id}`"><span class="company-avatar deal-avatar">◇</span><span><strong>{{ deal.title }}</strong><small>{{ t('added') }} {{ formatDate(deal.created_at) }}</small></span></RouterLink></td><td>{{ customerName(deal.customer_id) }}</td><td class="amount-value">{{ formatAmount(deal.amount) }} {{ t('currency') }}</td><td><span class="probability-chip">{{ deal.probability }}%</span></td><td><span class="status-chip" :class="statusClass(deal.status)"><i></i>{{ statusLabel(deal.status) }}</span></td><td>{{ formatDate(deal.expected_close_date) }}</td><td class="row-actions"><button @click="openEdit(deal)"><span aria-hidden="true">✎</span> {{ t('edit') }}</button><button class="danger-link" @click="confirmDelete(deal)"><span aria-hidden="true">⌫</span> {{ t('delete') }}</button></td></tr></tbody></table></div><div class="pagination"><span>{{ t('page') }} {{ page }}</span><div><button class="ghost-btn" :disabled="page === 1" @click="goPage(page - 1)">← {{ t('previous') }}</button><button class="ghost-btn" :disabled="!hasMore" @click="goPage(page + 1)">{{ t('next') }} →</button></div></div></div>
    <div v-if="modal" class="modal-backdrop" @click.self="closeModal"><section class="modal-card"><button class="modal-close" @click="closeModal">×</button><span class="eyebrow">{{ modal === 'create' ? t('newDeal') : t('editDeal') }}</span><h2>{{ modal === 'create' ? t('createDeal') : t('edit') }}</h2><p class="muted">{{ t('dealsSubtitle') }}</p><DealForm :deal="selected || (modal === 'create' && filters.customer_id ? { customer_id: filters.customer_id } : null)" :editing="modal === 'edit'" :customers="customers" :status-options="modal === 'edit' ? nextStatuses(selected?.status) : []" :saving="saving" :error="formError" :submit-label="modal === 'create' ? t('createDeal') : t('saveDeal')" @submit="saveDeal" @cancel="closeModal" /></section></div>
    <div v-if="deleteTarget" class="modal-backdrop" @click.self="deleteTarget = null"><section class="modal-card confirm-card"><div class="warning-icon">!</div><h2>{{ t('deleteDealQuestion') }}</h2><p class="muted">{{ t('deleteDealText') }} <strong>{{ deleteTarget.title }}</strong>.</p><div class="form-actions"><button class="ghost-btn" @click="deleteTarget = null">{{ t('cancel') }}</button><button class="danger-btn" :disabled="saving" @click="removeDeal">{{ saving ? '…' : t('confirmDeleteDeal') }}</button></div></section></div>
  </section>
</template>

<script setup>
import { computed, onMounted, onUnmounted, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getMe } from '../api'
import { customerService } from '../services/customers'
import { dealService } from '../services/deals'
import { userService } from '../services/users'
import DealForm from '../components/deals/DealForm.vue'
import { t } from '../i18n'
import Icon from '../components/Icon.vue'
import { formatDate } from '../date'

const statuses = ['New', 'Qualified', 'Proposal', 'Negotiation', 'Won', 'Lost']
const route = useRoute()
const transitions = { New: ['Qualified'], Qualified: ['Proposal'], Proposal: ['Negotiation'], Negotiation: ['Won', 'Lost'], Won: [], Lost: [] }
const deals = ref([]), customers = ref([]), owners = ref([]), user = ref(null), loading = ref(true), error = ref(''), page = ref(1), hasMore = ref(false), modal = ref(null), selected = ref(null), deleteTarget = ref(null), saving = ref(false), formError = ref('')
const filters = reactive({ search: '', status: '', customer_id: '', owner_id: '', min_amount: '', max_amount: '', min_probability: '', max_probability: '', date_from: '', date_to: '' })
const isAdmin = computed(() => user.value?.role === 'Admin')
let searchTimer
const displayedDeals = computed(() => deals.value.slice(0, 20)); let requestId = 0

async function loadCustomers() { customers.value = await customerService.list('', 0, 100) }
async function load(showLoading = true) { const currentRequest = ++requestId; if (showLoading) loading.value = true; error.value = ''; try { const result = await dealService.list({ ...filters, skip: (page.value - 1) * 20, limit: 21 }); if (currentRequest !== requestId) return; deals.value = result; hasMore.value = result.length > 20 } catch (e) { if (currentRequest === requestId) error.value = e.message } finally { if (currentRequest === requestId) loading.value = false } }
async function refresh() { page.value = 1; await load() }
function onSearch() { clearTimeout(searchTimer); page.value = 1; searchTimer = setTimeout(() => load(false), 300) }
function hasFilters() { return Object.values(filters).some(value => value !== '' && value !== null && value !== undefined) }
function clearFilters() { Object.keys(filters).forEach(key => { filters[key] = '' }); refresh() }
function goPage(nextPage) { page.value = nextPage; load() }
function customerName(id) { return customers.value.find(customer => customer.id === id)?.name || '—' }
function statusLabel(status) { return t(`status${status}`) }
function statusClass(status) { return status.toLowerCase() }
function nextStatuses(status) { return transitions[status] || [] }
function formatAmount(value) { return Number(value).toLocaleString(localStorage.getItem('smart_crm_locale') === 'en' ? 'en-US' : 'uk-UA', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }
function openCreate() { selected.value = null; formError.value = ''; modal.value = 'create' }
function openEdit(deal) { selected.value = deal; formError.value = ''; modal.value = 'edit' }
function closeModal() { modal.value = null; selected.value = null }
async function saveDeal(data) { saving.value = true; formError.value = ''; try { if (modal.value === 'create') await dealService.create(data); else await dealService.update(selected.value.id, data); closeModal(); await load() } catch (e) { formError.value = e.message } finally { saving.value = false } }
function confirmDelete(deal) { deleteTarget.value = deal }
async function removeDeal() { saving.value = true; try { await dealService.remove(deleteTarget.value.id); deleteTarget.value = null; await load() } catch (e) { error.value = e.message } finally { saving.value = false } }
onMounted(async () => { try { user.value = await getMe(); if (isAdmin.value) owners.value = await userService.list(); await loadCustomers(); if (route.query.customer_id) filters.customer_id = route.query.customer_id; await load(); if (route.query.create) openCreate() } catch (e) { error.value = e.message; loading.value = false } })
onMounted(() => window.addEventListener('crm:open-create-deal', openCreate))
onUnmounted(() => window.removeEventListener('crm:open-create-deal', openCreate))
</script>
