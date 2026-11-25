<template>
  <section class="workspace-page">
    <div class="customer-actions action-only"><button class="primary-btn add-btn" @click="openCreate">{{ t('addContact') }}</button></div>
    <div v-if="error" class="feedback error">{{ error }}</div>
    <div class="filter-bar"><div class="search-box"><span aria-hidden="true"><Icon name="search" /></span><input v-model="search" @input="onSearch" :placeholder="t('searchContacts')" :aria-label="t('searchContacts')" /></div><select v-model="customerFilter" @change="refresh"><option value="">{{ t('allCustomers') }}</option><option v-for="customer in customers" :key="customer.id" :value="customer.id">{{ customer.name }}</option></select><span class="result-count">{{ displayedContacts.length }} {{ contactsLabel(displayedContacts.length) }}</span></div>
    <div v-if="loading" class="state-card"><span class="spinner"></span><p>{{ t('loading') }}</p></div>
    <div v-else-if="!displayedContacts.length" class="state-card"><div class="empty-icon">◎</div><h3>{{ search ? t('noContactResults') : t('noContacts') }}</h3><p class="muted">{{ search ? t('tryAgain') : t('manage') }}</p><button v-if="!search" class="primary-btn compact" @click="openCreate">{{ t('addFirstContact') }}</button></div>
    <div v-else class="table-card"><div class="table-wrap"><table><thead><tr><th>{{ t('contact') }}</th><th>{{ t('jobTitle') }}</th><th>{{ t('company') }}</th><th>{{ t('email') }}</th><th class="actions-col">{{ t('actions') }}</th></tr></thead><tbody><tr v-for="contact in displayedContacts" :key="contact.id"><td><RouterLink class="company-link" :to="`/contacts/${contact.id}`"><span class="company-avatar contact-avatar">{{ initials(contact) }}</span><span><strong>{{ contact.first_name }} {{ contact.last_name }}</strong><small>{{ t('added') }} {{ formatDate(contact.created_at) }}</small></span></RouterLink></td><td>{{ contact.title || '—' }}</td><td>{{ customerName(contact.customer_id) }}</td><td><span>{{ contact.email || '—' }}</span><small>{{ contact.phone || '' }}</small></td><td class="row-actions"><button @click="openEdit(contact)"><span aria-hidden="true">✎</span> {{ t('edit') }}</button><button class="danger-link" @click="confirmDelete(contact)"><span aria-hidden="true">⌫</span> {{ t('delete') }}</button></td></tr></tbody></table></div><div class="pagination"><span>{{ t('page') }} {{ page }}</span><div><button class="ghost-btn" :disabled="page === 1" @click="goPage(page - 1)">← {{ t('previous') }}</button><button class="ghost-btn" :disabled="!hasMore" @click="goPage(page + 1)">{{ t('next') }} →</button></div></div></div>
    <div v-if="modal" class="modal-backdrop" @click.self="closeModal"><section class="modal-card"><button class="modal-close" @click="closeModal">×</button><span class="eyebrow">{{ modal === 'create' ? t('newContact') : t('editContact') }}</span><h2>{{ modal === 'create' ? t('createContact') : t('edit') }}</h2><p class="muted">{{ t('contactsSubtitle') }}</p><ContactForm :contact="selected" :customer="customers.find(customer => customer.id === customerFilter) || null" :customers="customers" :saving="saving" :error="formError" :submit-label="modal === 'create' ? t('createContact') : t('save')" @submit="saveContact" @cancel="closeModal" /></section></div>
    <div v-if="deleteTarget" class="modal-backdrop" @click.self="deleteTarget = null"><section class="modal-card confirm-card"><div class="warning-icon">!</div><h2>{{ t('contactDeleteQuestion') }}</h2><p class="muted">{{ t('contactDeleteText') }} <strong>{{ deleteTarget.first_name }} {{ deleteTarget.last_name }}</strong>.</p><div class="form-actions"><button class="ghost-btn" @click="deleteTarget = null">{{ t('cancel') }}</button><button class="danger-btn" :disabled="saving" @click="removeContact">{{ saving ? '…' : t('confirmDeleteContact') }}</button></div></section></div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { customerService } from '../services/customers'
import { contactService } from '../services/contacts'
import ContactForm from '../components/contacts/ContactForm.vue'
import { locale, t } from '../i18n'
import Icon from '../components/Icon.vue'
import { formatDate } from '../date'

const route = useRoute()
const contacts = ref([]), customers = ref([]), loading = ref(true), error = ref(''), search = ref(''), customerFilter = ref(''), page = ref(1), hasMore = ref(false), modal = ref(null), selected = ref(null), deleteTarget = ref(null), saving = ref(false), formError = ref('')
let searchTimer
const displayedContacts = computed(() => contacts.value.slice(0, 20)); let requestId = 0

async function loadCustomers() { customers.value = await customerService.list('', 0, 100) }
async function load(showLoading = true) { const currentRequest = ++requestId; if (showLoading) loading.value = true; error.value = ''; try { const result = await contactService.list(search.value, customerFilter.value, (page.value - 1) * 20, 21); if (currentRequest !== requestId) return; contacts.value = result; hasMore.value = result.length > 20 } catch (e) { if (currentRequest === requestId) error.value = e.message } finally { if (currentRequest === requestId) loading.value = false } }
async function refresh() { page.value = 1; await load() }
function onSearch() { clearTimeout(searchTimer); page.value = 1; searchTimer = setTimeout(() => load(false), 300) }
function goPage(nextPage) { page.value = nextPage; load() }
function customerName(id) { return customers.value.find(customer => customer.id === id)?.name || '—' }
function contactsLabel(count) { if (locale.value === 'en') return count === 1 ? 'contact' : 'contacts'; const mod10 = count % 10; const mod100 = count % 100; if (mod10 === 1 && mod100 !== 11) return 'контакт'; if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) return 'контакти'; return 'контактів' }
function initials(contact) { return `${contact.first_name?.[0] || ''}${contact.last_name?.[0] || ''}`.toUpperCase() }
function openCreate() { selected.value = null; formError.value = ''; modal.value = 'create' }
function openEdit(contact) { selected.value = contact; formError.value = ''; modal.value = 'edit' }
function closeModal() { modal.value = null; selected.value = null }
async function saveContact(data) { saving.value = true; formError.value = ''; try { if (modal.value === 'create') await contactService.create(data); else await contactService.update(selected.value.id, data); closeModal(); await load() } catch (e) { formError.value = e.message } finally { saving.value = false } }
function confirmDelete(contact) { deleteTarget.value = contact }
async function removeContact() { saving.value = true; try { await contactService.remove(deleteTarget.value.id); deleteTarget.value = null; await load() } catch (e) { error.value = e.message } finally { saving.value = false } }
onMounted(async () => { try { await loadCustomers(); if (route.query.customer_id) customerFilter.value = route.query.customer_id; await load(); if (route.query.edit) { const item = contacts.value.find(contact => contact.id === route.query.edit); if (item) openEdit(item) } else if (route.query.create) openCreate() } catch (e) { error.value = e.message; loading.value = false } })
</script>
