<template>
  <section>
    <div v-if="loading" class="state-card"><span class="spinner"></span><p>{{ t('loading') }}</p></div>
    <div v-else-if="error" class="feedback error">{{ error }}</div>
    <template v-else-if="deal">
      <RouterLink class="back-link" to="/deals">← {{ t('deals') }}</RouterLink>
      <div class="details-heading"><div><span class="eyebrow">{{ t('dealDetails') }}</span><h1>{{ deal.title }}</h1><p class="muted">{{ customerName }}</p></div><div><button class="ghost-btn" @click="modal = true">{{ t('edit') }}</button><button class="danger-btn" @click="showDelete = true">{{ t('delete') }}</button></div></div>
      <div class="details-grid"><article class="detail-card"><span class="detail-label">{{ t('dealInfo') }}</span><h3>{{ deal.title }}</h3><div class="deal-hero-status"><span class="status-chip" :class="statusClass(deal.status)"><i></i>{{ statusLabel(deal.status) }}</span><span>{{ deal.probability }}% {{ t('probability').toLowerCase() }}</span></div><dl><div><dt>{{ t('amount') }}</dt><dd class="big-value">{{ formatAmount(deal.amount) }} {{ t('currency') }}</dd></div><div><dt>{{ t('expectedCloseDate') }}</dt><dd>{{ formatDate(deal.expected_close_date) }}</dd></div><div><dt>{{ t('dealCustomer') }}</dt><dd><RouterLink class="inline-link" :to="`/customers/${deal.customer_id}`">{{ customerName }}</RouterLink></dd></div></dl></article><article class="detail-card"><span class="detail-label">{{ t('recordInfo') }}</span><dl><div><dt>{{ t('created') }}</dt><dd>{{ formatDate(deal.created_at) }}</dd></div><div><dt>{{ t('updated') }}</dt><dd>{{ formatDate(deal.updated_at) }}</dd></div><div><dt>{{ t('id') }}</dt><dd class="id-value">{{ deal.id }}</dd></div><div><dt>{{ t('status') }}</dt><dd>{{ statusLabel(deal.status) }}</dd></div></dl></article></div>
    </template>
    <div v-if="modal" class="modal-backdrop" @click.self="modal = false"><section class="modal-card"><button class="modal-close" @click="modal = false">×</button><span class="eyebrow">{{ t('editDeal') }}</span><h2>{{ t('edit') }}</h2><p class="muted">{{ t('dealsSubtitle') }}</p><DealForm :deal="deal" editing :customers="customers" :status-options="nextStatuses(deal.status)" :saving="saving" :error="formError" :submit-label="t('saveDeal')" @submit="save" @cancel="modal = false" /></section></div>
    <div v-if="showDelete" class="modal-backdrop" @click.self="showDelete = false"><section class="modal-card confirm-card"><div class="warning-icon">!</div><h2>{{ t('deleteDealQuestion') }}</h2><p class="muted">{{ t('deleteDealText') }}</p><div class="form-actions"><button class="ghost-btn" @click="showDelete = false">{{ t('cancel') }}</button><button class="danger-btn" :disabled="saving" @click="remove">{{ saving ? '…' : t('confirmDeleteDeal') }}</button></div></section></div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { customerService } from '../services/customers'
import { dealService } from '../services/deals'
import DealForm from '../components/deals/DealForm.vue'
import { t } from '../i18n'
import { formatDate } from '../date'

const transitions = { New: ['Qualified'], Qualified: ['Proposal'], Proposal: ['Negotiation'], Negotiation: ['Won', 'Lost'], Won: [], Lost: [] }
const route = useRoute(), router = useRouter(), deal = ref(null), customers = ref([]), loading = ref(true), error = ref(''), modal = ref(false), showDelete = ref(false), saving = ref(false), formError = ref('')
const customerName = computed(() => customers.value.find(customer => customer.id === deal.value?.customer_id)?.name || t('notSpecified'))
function nextStatuses(status) { return transitions[status] || [] }
function statusLabel(status) { return t(`status${status}`) }
function statusClass(status) { return status.toLowerCase() }
function formatAmount(value) { return Number(value).toLocaleString(localStorage.getItem('smart_crm_locale') === 'en' ? 'en-US' : 'uk-UA', { minimumFractionDigits: 2, maximumFractionDigits: 2 }) }
async function load() { try { [deal.value, customers.value] = await Promise.all([dealService.get(route.params.id), customerService.list('', 0, 100)]) } catch (e) { error.value = e.message } finally { loading.value = false } }
async function save(data) { saving.value = true; formError.value = ''; try { deal.value = await dealService.update(deal.value.id, data); modal.value = false } catch (e) { formError.value = e.message } finally { saving.value = false } }
async function remove() { saving.value = true; try { await dealService.remove(deal.value.id); router.push('/deals') } catch (e) { error.value = e.message; showDelete.value = false } finally { saving.value = false } }
onMounted(load)
</script>
