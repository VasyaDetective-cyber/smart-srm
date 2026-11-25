import { apiRequest } from '../api'

export const dealService = {
  list: (params = {}) => {
    const query = new URLSearchParams({ skip: params.skip || 0, limit: params.limit || 21 })
    for (const [key, value] of Object.entries(params)) {
      if (key !== 'skip' && key !== 'limit' && value !== '' && value !== null && value !== undefined) query.set(key, value)
    }
    return apiRequest(`/deals/?${query.toString()}`)
  },
  get: id => apiRequest(`/deals/${id}`),
  create: data => apiRequest('/deals/', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }),
  update: (id, data) => apiRequest(`/deals/${id}`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }),
  remove: id => apiRequest(`/deals/${id}`, { method: 'DELETE' }),
}
