/**
 * API client utility for frontend
 * Provides centralized axios configuration and API endpoint functions
 */

import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Create axios instance with base config
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Error interceptor
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

// API Endpoints
export const apiClient = {
  // Trips
  getTrips: (skip = 0, limit = 100) => 
    api.get(`/api/trips?skip=${skip}&limit=${limit}`),
  getTrip: (id) => 
    api.get(`/api/trips/${id}`),
  createTrip: (data) => 
    api.post('/api/trips', data),
  updateTrip: (id, data) => 
    api.put(`/api/trips/${id}`, data),
  completeTrip: (id) => 
    api.post(`/api/trips/${id}/complete`),
  getHighRiskTrips: () => 
    api.get('/api/trips/active/high-risk'),

  // Bilties
  getBilties: (skip = 0, limit = 100) => 
    api.get(`/api/bilty?skip=${skip}&limit=${limit}`),
  getBilty: (id) => 
    api.get(`/api/bilty/${id}`),
  createBilty: (data) => 
    api.post('/api/bilty/create', data),
  updateBilty: (id, data) => 
    api.put(`/api/bilty/${id}`, data),
  deleteBilty: (id) => 
    api.delete(`/api/bilty/${id}`),

  // ML Predictions
  predictDelay: (features) => 
    api.post('/api/ml/predict', features),
  calculateHealthScore: (data) => 
    api.post('/api/ml/health-score', data),
  analyzeCascadeRisk: (tripId, riskScore) => 
    api.post(`/api/ml/cascade-analysis/${tripId}`, { risk_score: riskScore }),
  detectAnomalies: () => 
    api.post('/api/ml/anomaly-detection'),

  // Decision Support
  getSimulation: (tripId) => 
    api.post(`/api/simulation/${tripId}`),
  chatCopilot: (tripId, message, context) => 
    api.post('/api/copilot/chat', { trip_id: tripId, message, context }),

  // Demo
  initDemo: () => 
    api.post('/api/demo/init'),
}

export default api
