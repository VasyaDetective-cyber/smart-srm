<template>
  <form class="entity-form" @submit.prevent="submit">
    <div class="form-grid">
      <label>{{ t('firstName') }} <span>*</span><input v-model.trim="form.first_name" required maxlength="100" autocomplete="given-name" /></label>
      <label>{{ t('lastName') }} <span>*</span><input v-model.trim="form.last_name" required maxlength="100" autocomplete="family-name" /></label>
      <label>{{ t('jobTitle') }}<input v-model.trim="form.title" maxlength="100" /></label>
      <label>{{ t('email') }}<input v-model.trim="form.email" type="email" autocomplete="email" /></label>
      <label>{{ t('phone') }}<input v-model.trim="form.phone" minlength="5" maxlength="20" autocomplete="tel" /></label>
      <label>{{ t('contactFor') }} <span>*</span><select v-model="form.customer_id" required :disabled="Boolean(contact)"><option value="" disabled>{{ t('selectCustomer') }}</option><option v-for="customer in customers" :key="customer.id" :value="customer.id">{{ customer.name }}</option></select></label>
    </div>
    <p v-if="error" class="form-error">{{ error }}</p>
    <div class="form-actions"><button type="button" class="ghost-btn" @click="$emit('cancel')">{{ t('cancel') }}</button><button class="primary-btn compact" :disabled="saving">{{ saving ? '…' : submitLabel }} <span>→</span></button></div>
  </form>
</template>

<script setup>
import { reactive, watch } from 'vue'
import { t } from '../../i18n'

const props = defineProps({ customer: { type: Object, default: null }, customers: { type: Array, default: () => [] }, contact: { type: Object, default: null }, saving: Boolean, error: String, submitLabel: { type: String, default: 'Save' } })
const emit = defineEmits(['submit', 'cancel'])
const form = reactive({ first_name: '', last_name: '', title: '', email: '', phone: '', customer_id: '' })

watch(() => props.contact, value => Object.assign(form, { first_name: value?.first_name || '', last_name: value?.last_name || '', title: value?.title || '', email: value?.email || '', phone: value?.phone || '', customer_id: value?.customer_id || props.customer?.id || '' }), { immediate: true })
watch(() => props.customer, value => { if (!props.contact && value) form.customer_id = value.id }, { immediate: true })
function submit() { emit('submit', { ...form, title: form.title || null, email: form.email || null, phone: form.phone || null }) }
</script>
