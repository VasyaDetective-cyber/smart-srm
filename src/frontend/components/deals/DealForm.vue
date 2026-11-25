<template>
  <form class="entity-form" @submit.prevent="submit">
    <div class="form-grid">
      <label class="wide">{{ t('dealTitle') }} <span>*</span><input v-model.trim="form.title" required maxlength="255" /></label>
      <label>{{ t('amount') }} <span>*</span><input v-model="form.amount" type="number" min="0.01" step="0.01" required /></label>
      <label>{{ t('probability') }} <span>*</span><input v-model="form.probability" type="number" min="0" max="100" required /><small class="field-hint">0–100%</small></label>
      <label>{{ t('expectedCloseDate') }} <span>*</span><input v-model="form.expected_close_date" type="date" lang="uk-UA" :min="editing ? undefined : tomorrow" required /></label>
      <label>{{ t('dealCustomer') }} <span>*</span><select v-model="form.customer_id" required><option value="" disabled>{{ t('selectCustomer') }}</option><option v-for="customer in customers" :key="customer.id" :value="customer.id">{{ customer.name }}</option></select></label>
      <label v-if="statusOptions.length">{{ t('nextStatus') }}<select v-model="form.status"><option value="">{{ t('changeStatus') }}</option><option v-for="status in statusOptions" :key="status" :value="status">{{ statusLabel(status) }}</option></select></label>
    </div>
    <p v-if="error" class="form-error">{{ error }}</p>
    <div class="form-actions"><button type="button" class="ghost-btn" @click="$emit('cancel')">{{ t('cancel') }}</button><button class="primary-btn compact" :disabled="saving">{{ saving ? '…' : submitLabel }} <span>→</span></button></div>
  </form>
</template>

<script setup>
import { computed, reactive, watch } from 'vue'
import { t } from '../../i18n'

const props = defineProps({ deal: { type: Object, default: null }, editing: Boolean, customers: { type: Array, default: () => [] }, statusOptions: { type: Array, default: () => [] }, saving: Boolean, error: String, submitLabel: { type: String, default: 'Save' } })
const emit = defineEmits(['submit', 'cancel'])
const form = reactive({ title: '', amount: '', probability: 0, expected_close_date: '', customer_id: '', status: '' })
const tomorrow = computed(() => { const date = new Date(); date.setDate(date.getDate() + 1); return date.toISOString().slice(0, 10) })
watch(() => props.deal, value => Object.assign(form, { title: value?.title || '', amount: value?.amount || '', probability: value?.probability ?? 0, expected_close_date: value?.expected_close_date || '', customer_id: value?.customer_id || '', status: '' }), { immediate: true })
function statusLabel(status) { return t(`status${status}`) }
function submit() { const data = { title: form.title, amount: form.amount, probability: Number(form.probability), customer_id: form.customer_id }; if (!props.editing || form.expected_close_date !== props.deal?.expected_close_date) data.expected_close_date = form.expected_close_date; if (form.status) data.status = form.status; emit('submit', data) }
</script>
