<template>
  <section>
    <div v-if="loading" class="state-card"><span class="spinner"></span><p>{{ t('loading') }}</p></div>
    <div v-else-if="error" class="feedback error">{{ error }}</div>
    <template v-else-if="contact">
      <RouterLink class="back-link" to="/contacts">← {{ t('contacts') }}</RouterLink>
      <div class="details-heading"><div><span class="eyebrow">{{ t('contactDetails') }}</span><h1>{{ contact.first_name }} {{ contact.last_name }}</h1><p class="muted">{{ contact.title || t('notSpecified') }}</p></div><div><button class="ghost-btn" @click="modal = true">{{ t('edit') }}</button><button class="danger-btn" @click="showDelete = true">{{ t('delete') }}</button></div></div>
      <div class="details-grid"><article class="detail-card"><span class="detail-label">{{ t('contactInfo') }}</span><h3>{{ contact.first_name }} {{ contact.last_name }}</h3><dl><div><dt>{{ t('jobTitle') }}</dt><dd>{{ contact.title || t('notSpecified') }}</dd></div><div><dt>{{ t('email') }}</dt><dd>{{ contact.email || t('notSpecified') }}</dd></div><div><dt>{{ t('phone') }}</dt><dd>{{ contact.phone || t('notSpecified') }}</dd></div><div><dt>{{ t('contactFor') }}</dt><dd><RouterLink class="inline-link" :to="`/customers/${contact.customer_id}`">{{ customerName }}</RouterLink></dd></div></dl></article><article class="detail-card"><span class="detail-label">{{ t('recordInfo') }}</span><dl><div><dt>{{ t('created') }}</dt><dd>{{ formatDate(contact.created_at) }}</dd></div><div><dt>{{ t('updated') }}</dt><dd>{{ formatDate(contact.updated_at) }}</dd></div><div><dt>{{ t('id') }}</dt><dd class="id-value">{{ contact.id }}</dd></div></dl></article></div>
    </template>
    <div v-if="modal" class="modal-backdrop" @click.self="modal = false"><section class="modal-card"><button class="modal-close" @click="modal = false">×</button><span class="eyebrow">{{ t('editContact') }}</span><h2>{{ t('edit') }}</h2><ContactForm :contact="contact" :customers="customers" :saving="saving" :error="formError" :submit-label="t('save')" @submit="save" @cancel="modal = false" /></section></div>
    <div v-if="showDelete" class="modal-backdrop" @click.self="showDelete = false"><section class="modal-card confirm-card"><div class="warning-icon">!</div><h2>{{ t('contactDeleteQuestion') }}</h2><p class="muted">{{ t('contactDeleteText') }}</p><div class="form-actions"><button class="ghost-btn" @click="showDelete = false">{{ t('cancel') }}</button><button class="danger-btn" :disabled="saving" @click="remove">{{ saving ? '…' : t('confirmDeleteContact') }}</button></div></section></div>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { contactService } from '../services/contacts'
import { customerService } from '../services/customers'
import ContactForm from '../components/contacts/ContactForm.vue'
import { t } from '../i18n'
import { formatDate } from '../date'

const route = useRoute(), router = useRouter(), contact = ref(null), customers = ref([]), loading = ref(true), error = ref(''), modal = ref(false), showDelete = ref(false), saving = ref(false), formError = ref('')
const customerName = computed(() => customers.value.find(customer => customer.id === contact.value?.customer_id)?.name || t('notSpecified'))
async function load() { try { [contact.value, customers.value] = await Promise.all([contactService.get(route.params.id), customerService.list('', 0, 100)]) } catch (e) { error.value = e.message } finally { loading.value = false } }
async function save(data) { saving.value = true; formError.value = ''; try { contact.value = await contactService.update(contact.value.id, data); modal.value = false } catch (e) { formError.value = e.message } finally { saving.value = false } }
async function remove() { saving.value = true; try { await contactService.remove(contact.value.id); router.push('/contacts') } catch (e) { error.value = e.message; showDelete.value = false } finally { saving.value = false } }
onMounted(load)
</script>
