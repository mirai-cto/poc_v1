import axios from 'axios'

// Create an Axios instance with default config
const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if needed
    // const token = localStorage.getItem('token')
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`
    // }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    // Handle common errors
    if (error.response) {
      // Server responded with an error status
      console.error('API Error:', error.response.data)
      
      // Handle specific status codes
      switch (error.response.status) {
        case 401:
          // Unauthorized - handle logout or token refresh
          break
        case 404:
          // Not found
          break
        case 500:
          // Server error
          break
        default:
          // Other errors
          break
      }
      
      return Promise.reject(error.response.data)
    } else if (error.request) {
      // Request was made but no response received
      console.error('Network Error:', error.request)
      return Promise.reject({ message: 'Network error. Please check your connection.' })
    } else {
      // Something else happened in making the request
      console.error('Request Error:', error.message)
      return Promise.reject({ message: 'An error occurred. Please try again.' })
    }
  }
)

export default api 