const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
export const token = { get: () => localStorage.getItem('smart_crm_token'), set: v => localStorage.setItem('smart_crm_token', v), clear: () => localStorage.removeItem('smart_crm_token') }
async function request(path, options = {}) {
  const headers = { ...(options.headers || {}) }
  const t = token.get(); if (t) headers.Authorization = `Bearer ${t}`
  const response = await fetch(`${API_URL}${path}`, { ...options, headers })
  if (!response.ok) { const body = await response.json().catch(() => ({})); throw new Error(body.detail || 'Не вдалося виконати запит') }
  return response.status === 204 ? null : response.json()
}
export async function login(email, password) {
  const body = new URLSearchParams({ username: email, password })
  const result = await request('/api/auth/login', { method: 'POST', body, headers: { 'Content-Type': 'application/x-www-form-urlencoded' } })
  token.set(result.access_token); return result
}
export const getMe = () => request('/api/auth/me')
