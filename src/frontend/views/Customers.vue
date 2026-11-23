<template>
  <section>
    <div class="customer-actions"><p class="muted">{{ t('customersSubtitle') }}</p><button class="primary-btn add-btn" @click="openCreate">{{ t('add') }}</button></div>
    <div v-if="error" class="feedback error">{{ error }}</div>
    <div class="toolbar"><div class="search-box"><span>⌕</span><input v-model="search" @input="onSearch" :placeholder="t('search')" :aria-label="t('customers')" /></div><span class="result-count">{{ displayedCustomers.length }} {{ displayedCustomers.length === 1 ? t('customer') : t('customersPlural') }}</span></div>
    <div v-if="loading" class="state-card"><span class="spinner"></span><p>{{ t('loading') }}</p></div>
    <div v-else-if="!displayedCustomers.length" class="state-card"><div class="empty-icon">⌁</div><h3>{{ search ? t('noResults') : t('noCustomers') }}</h3><p class="muted">{{ search ? t('tryAgain') : t('manage') }}</p><button v-if="!search" class="primary-btn compact" @click="openCreate">{{ t('addFirst') }}</button></div>
    <div v-else class="table-card"><div class="table-wrap"><table><thead><tr><th>{{ t('company') }}</th><th>{{ t('industry') }}</th><th>{{ t('contact') }}</th><th>{{ t('address') }}</th><th class="actions-col">{{ t('actions') }}</th></tr></thead><tbody><tr v-for="customer in displayedCustomers" :key="customer.id"><td><RouterLink class="company-link" :to="`/customers/${customer.id}`"><span class="company-avatar">{{ initials(customer.name) }}</span><span><strong>{{ customer.name }}</strong><small>{{ t('added') }} {{ formatDate(customer.created_at) }}</small></span></RouterLink></td><td>{{ customer.industry || '—' }}</td><td><span>{{ customer.email || '—' }}</span><small>{{ customer.phone || '' }}</small></td><td>{{ customer.address || '—' }}</td><td class="row-actions"><button @click="openEdit(customer)">{{ t('edit') }}</button><button class="danger-link" @click="confirmDelete(customer)">{{ t('delete') }}</button></td></tr></tbody></table></div><div class="pagination"><span>{{ t('page') }} {{ page }}</span><div><button class="ghost-btn" :disabled="page===1" @click="goPage(page-1)">← {{ t('previous') }}</button><button class="ghost-btn" :disabled="!hasMore" @click="goPage(page+1)">{{ t('next') }} →</button></div></div></div>
    <div v-if="modal" class="modal-backdrop" @click.self="closeModal"><section class="modal-card"><button class="modal-close" @click="closeModal">×</button><span class="eyebrow">{{ modal === 'create' ? t('newCustomer') : t('editCustomer') }}</span><h2>{{ modal === 'create' ? t('add') : t('edit') }}</h2><p class="muted">{{ t('manage') }}</p><CustomerForm :customer="selected" :saving="saving" :error="formError" :submit-label="modal === 'create' ? t('create') : t('save')" @submit="saveCustomer" @cancel="closeModal" /></section></div>
    <div v-if="deleteTarget" class="modal-backdrop" @click.self="deleteTarget=null"><section class="modal-card confirm-card"><div class="warning-icon">!</div><h2>{{ t('deleteQuestion') }}</h2><p class="muted">{{ t('deleteText') }} <strong>{{ deleteTarget.name }}</strong>.</p><div class="form-actions"><button class="ghost-btn" @click="deleteTarget=null">{{ t('cancel') }}</button><button class="danger-btn" :disabled="saving" @click="removeCustomer">{{ saving ? '…' : t('confirmDelete') }}</button></div></section></div>
  </section>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { customerService } from '../services/customers'
import CustomerForm from '../components/customers/CustomerForm.vue'
import { t } from '../i18n'
const route=useRoute(),customers=ref([]),loading=ref(true),error=ref(''),search=ref(''),modal=ref(null),selected=ref(null),deleteTarget=ref(null),saving=ref(false),formError=ref(''),page=ref(1),hasMore=ref(false); let searchTimer
const displayedCustomers=computed(()=>customers.value.slice(0,20))
async function load(showLoading=true){if(showLoading)loading.value=true;error.value='';try{const result=await customerService.list(search.value,(page.value-1)*20,21);customers.value=result;hasMore.value=result.length>20}catch(e){error.value=e.message}finally{loading.value=false}}
function goPage(nextPage){page.value=nextPage;load()}
function onSearch(){clearTimeout(searchTimer);page.value=1;searchTimer=setTimeout(()=>load(false),300)}
onMounted(async()=>{await load();if(route.query.edit){const item=customers.value.find(c=>c.id===route.query.edit);if(item)openEdit(item)}})
function openCreate(){selected.value=null;formError.value='';modal.value='create'} function openEdit(c){selected.value=c;formError.value='';modal.value='edit'} function closeModal(){modal.value=null;selected.value=null}
async function saveCustomer(data){saving.value=true;formError.value='';try{if(modal.value==='create')await customerService.create(data);else await customerService.update(selected.value.id,data);closeModal();await load()}catch(e){formError.value=e.message}finally{saving.value=false}}
function confirmDelete(c){deleteTarget.value=c} async function removeCustomer(){saving.value=true;try{await customerService.remove(deleteTarget.value.id);deleteTarget.value=null;await load()}catch(e){error.value=e.message}finally{saving.value=false}}
function initials(name){return name.split(' ').map(x=>x[0]).join('').slice(0,2).toUpperCase()} function formatDate(v){return v?new Date(v).toLocaleDateString(localeForDate(),{day:'2-digit',month:'short',year:'numeric'}):'—'} function localeForDate(){return localStorage.getItem('smart_crm_locale')==='en'?'en-US':'uk-UA'}
</script>

