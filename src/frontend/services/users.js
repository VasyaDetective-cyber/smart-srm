import { apiRequest } from '../api'

export const userService = {
  list: () => apiRequest('/users/?skip=0&limit=100'),
}
