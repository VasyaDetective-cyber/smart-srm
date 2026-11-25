import { locale } from './i18n'

export function formatDate(value) {
  if (!value) return '—'

  const [year, month, day] = String(value).slice(0, 10).split('-')
  if (!year || !month || !day) return '—'

  return locale.value === 'en'
    ? `${month}/${day}/${year}`
    : `${day}.${month}.${year}`
}
