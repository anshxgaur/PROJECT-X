/**
 * Utility functions for risk and health calculations
 */

export const getRiskColor = (probability) => {
  if (probability < 0.2) return 'green'
  if (probability < 0.4) return 'yellow'
  if (probability < 0.6) return 'orange'
  return 'red'
}

export const getRiskLabel = (probability) => {
  const level = getRiskColor(probability)
  return level.charAt(0).toUpperCase() + level.slice(1)
}

export const formatCurrency = (value) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
  }).format(value)
}

export const formatDistance = (km) => {
  return `${km.toFixed(1)} km`
}

export const formatDuration = (hours) => {
  const h = Math.floor(hours)
  const m = Math.round((hours - h) * 60)
  return `${h}h ${m}m`
}

export const formatDateTime = (date) => {
  return new Date(date).toLocaleString('en-IN', {
    dateStyle: 'medium',
    timeStyle: 'short',
  })
}

export const calculateProgress = (completed, total) => {
  return Math.round((completed / total) * 100)
}

export const getHealthRating = (score) => {
  if (score >= 90) return { text: 'Excellent', color: 'emerald' }
  if (score >= 75) return { text: 'Good', color: 'green' }
  if (score >= 60) return { text: 'Fair', color: 'yellow' }
  return { text: 'Poor', color: 'red' }
}
