import { defineStore } from 'pinia'
import ApiRequests from '@/api/request'

export const useAnalysisStore = defineStore('analysis', {
  state: () => ({
    messages: [],
    dailyMessageCount: 0,
    lastMessageDate: null,
    hasActiveConversation: false,
    lastSelectedOption: null,
    loading: false,
    error: null
  }),

  getters: {
    remainingMessages: (state) => {
      const MAX_DAILY_MESSAGES = 5
      return Math.max(0, MAX_DAILY_MESSAGES - state.dailyMessageCount)
    },
    
    hasReachedMessageLimit: (state) => {
      const MAX_DAILY_MESSAGES = 100
      return state.dailyMessageCount >= MAX_DAILY_MESSAGES
    },
    
    conversationHistory: (state) => {
      return state.messages.map(msg => ({
        role: msg.role === 'user' ? 'Human' : 'Assistant',
        content: msg.content
      }))
    }
  },

  actions: {
    initializeStore() {
      const savedData = localStorage.getItem('analysisStore')
      if (savedData) {
        const parsed = JSON.parse(savedData)
        
        const today = new Date().toDateString()
        if (parsed.lastMessageDate !== today) {
          this.dailyMessageCount = 0
          this.lastMessageDate = today
          this.clearConversation()
        } else {
          this.messages = parsed.messages || []
          this.dailyMessageCount = parsed.dailyMessageCount || 0
          this.lastMessageDate = parsed.lastMessageDate
          this.hasActiveConversation = parsed.hasActiveConversation || false
          this.lastSelectedOption = parsed.lastSelectedOption
        }
      } else {
        this.lastMessageDate = new Date().toDateString()
      }
      
      this.persistState()
    },
    
    persistState() {
      const dataToSave = {
        messages: this.messages,
        dailyMessageCount: this.dailyMessageCount,
        lastMessageDate: this.lastMessageDate,
        hasActiveConversation: this.hasActiveConversation,
        lastSelectedOption: this.lastSelectedOption
      }
      localStorage.setItem('analysisStore', JSON.stringify(dataToSave))
    },
    
    addMessage(message) {
      this.messages.push({
        ...message,
        timestamp: new Date().toISOString()
      })
      
      if (message.role === 'user') {
        this.dailyMessageCount++
        this.hasActiveConversation = true
      }
      
      this.persistState()
    },
    
    async sendAnalysisRequest(payload) {
      this.loading = true
      this.error = null
      
      try {
        console.log('Sending analysis request:', payload.option)
        
        const response = await ApiRequests.post('/analysis/chat', {
          option: payload.option,
          userData: payload.userData,
          workouts: payload.workouts,
          conversationHistory: this.conversationHistory
        })
        
        console.log('Analysis response:', response.data)
        
        if (response.data.success) {
          this.addMessage({
            role: 'assistant',
            content: response.data.message
          })
          
          return { success: true }
        } else {
          throw new Error(response.data.error || 'Failed to get response')
        }
      } catch (error) {
        this.error = error.message
        console.error('Analysis request error:', error)
        
        this.addMessage({
          role: 'assistant',
          content: 'I apologize, but I encountered an error. Please try again.'
        })
        
        return { success: false, error: error.message }
      } finally {
        this.loading = false
      }
    },
    
    async sendMessage(payload) {
      this.loading = true
      this.error = null
      
      try {
        const response = await ApiRequests.post('/analysis/chat', {
          message: payload.message,
          userData: payload.userData,
          workouts: payload.workouts,
          conversationHistory: this.conversationHistory
        })
        
        if (response.data.success) {
          this.addMessage({
            role: 'assistant',
            content: response.data.message
          })
          
          return { success: true }
        } else {
          throw new Error(response.data.error || 'Failed to get response')
        }
      } catch (error) {
        this.error = error.message
        console.error('Message send error:', error)
        return { success: false, error: error.message }
      } finally {
        this.loading = false
      }
    },
    
    clearConversation() {
      this.messages = []
      this.hasActiveConversation = false
      this.lastSelectedOption = null
      this.error = null
      this.persistState()
    },
    
    resetDailyLimit() {
      this.dailyMessageCount = 0
      this.lastMessageDate = new Date().toDateString()
      this.persistState()
    }
  }
})