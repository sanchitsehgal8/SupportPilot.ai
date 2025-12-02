import axios from 'axios'

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5001/api'

const instance = axios.create({
  baseURL: API_BASE,
  timeout: 15000
})

// Attach token automatically
instance.interceptors.request.use((config) => {
  const token = typeof window !== 'undefined' ? localStorage.getItem('sp_token') : null
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default instance
