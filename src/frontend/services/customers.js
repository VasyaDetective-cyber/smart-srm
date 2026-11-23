import { apiRequest } from '../api'

export const customerService = {
  list: (search = '', skip = 0, limit = 21) => apiRequest(`/customers/?skip=${skip}&limit=${limit}${search ? `&search=${encodeURIComponent(search)}` : ''}`),
  get: id => apiRequest(`/customers/${id}`),
  create: data => apiRequest('/customers/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }),
  update: (id, data) => apiRequest(`/customers/${id}`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }),
  remove: id => apiRequest(`/customers/${id}`, { method: 'DELETE' }),
}
