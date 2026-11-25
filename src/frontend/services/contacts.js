import { apiRequest } from '../api'

export const contactService = {
  list: (search = '', customerId = '', skip = 0, limit = 21) => {
    const params = new URLSearchParams({ skip, limit })
    if (search) params.set('search', search)
    if (customerId) params.set('customer_id', customerId)
    return apiRequest(`/contacts/?${params.toString()}`)
  },
  get: id => apiRequest(`/contacts/${id}`),
  create: data => apiRequest('/contacts/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }),
  update: (id, data) => apiRequest(`/contacts/${id}`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }),
  remove: id => apiRequest(`/contacts/${id}`, { method: 'DELETE' }),
}
