import { defineStore } from 'pinia'
import ApiRequests from '@/api/request'
import router from '@/router'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null
  }),

  getters: {
    currentUser: (state) => state.user,
    isLoggedIn: (state) => state.isAuthenticated,
    username: (state) => state.user?.username || '',
    fullName: (state) => {
      if (!state.user) return ''
      return `${state.user.first_name} ${state.user.last_name}`
    }
  },

  actions: {
    setUser(userData) {
      this.user = userData
      this.isAuthenticated = true
      
      localStorage.setItem('user', JSON.stringify(userData))
      localStorage.setItem('isAuthenticated', 'true')
    },

    async login(credentials) {
      this.loading = true
      this.error = null
      try {
        const response = await ApiRequests.loginUser(credentials)
        this.setUser(response.data)
        
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.message
        return { success: false, error: error.message }
      } finally {
        this.loading = false
      }
    },

    async signup(userData) {
      this.loading = true
      this.error = null
      try {
        const response = await ApiRequests.createUser(userData)
        this.setUser(response.data)
        
        return { success: true, data: response.data }
      } catch (error) {
        this.error = error.message
        return { success: false, error: error.message }
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.user = null
      this.isAuthenticated = false
      this.error = null
      
      localStorage.removeItem('user')
      localStorage.removeItem('isAuthenticated')
      
      router.push('/')
    },

    initializeAuth() {
      const storedUser = localStorage.getItem('user')
      const isAuthenticated = localStorage.getItem('isAuthenticated')
      
      if (storedUser && isAuthenticated === 'true') {
        try {
          this.user = JSON.parse(storedUser)
          this.isAuthenticated = true
        } catch (error) {
          console.error('Error parsing stored user data:', error)
          this.logout()
        }
      }
    },

    updateUserData(updates) {
      if (this.user) {
        this.user = { ...this.user, ...updates }
        localStorage.setItem('user', JSON.stringify(this.user))
      }
    }
  }
})