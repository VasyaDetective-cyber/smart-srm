<template>
  <svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <template v-if="name === 'dashboard'"><path d="m3 10 9-7 9 7"/><path d="M5 9.5V21h14V9.5"/><path d="M9 21v-6h6v6"/></template>
    <template v-else-if="name === 'customers'"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></template>
    <template v-else-if="name === 'contacts'"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2.5"/><path d="M5.5 16a4 4 0 0 1 7 0M15 9h3M15 13h3M15 17h3"/></template>
    <template v-else-if="name === 'deals'"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 12h18M10 12v2h4v-2"/></template>
    <template v-else-if="name === 'activities'"><rect x="3" y="4" width="18" height="17" rx="2"/><path d="M16 2v4M8 2v4M3 9h18M12 13v4l2.5 1.5"/></template>
    <template v-else-if="name === 'search'"><circle cx="10.8" cy="10.8" r="6.8"/><path d="m16 16 5 5"/></template>
  </svg>
</template>

<script setup>
defineProps({ name: { type: String, required: true } })
</script>
