<template>
    <v-container fluid>
      <!-- Debug Panel -->
      <v-row v-if="showDebug">
        <v-col cols="12">
          <v-alert type="info" variant="outlined">
            <div>Messages Count: {{ analysisStore.messages.length }}</div>
            <div>Has Active Conversation: {{ analysisStore.hasActiveConversation }}</div>
            <div>Loading: {{ loading }}</div>
            <div>Store Loading: {{ analysisStore.loading }}</div>
          </v-alert>
        </v-col>
      </v-row>
  
      <v-row>
        <v-col cols="12">
          <h1 class="text-h4 mb-4">AI Workout Analysis</h1>
          <v-alert v-if="userStore.fullName" type="info" variant="tonal" class="mb-4">
            Analyzing progress for {{ userStore.fullName }}
          </v-alert>
        </v-col>
      </v-row>
  
      <!-- Initial Options -->
      <v-row v-if="!analysisStore.hasActiveConversation">
        <v-col cols="12">
          <v-card>
            <v-card-title>Choose an Analysis Option</v-card-title>
            <v-card-text>
              <p class="mb-4">Select what you'd like me to help you with today:</p>
              <v-row>
                <v-col v-for="option in initialOptions" :key="option.value" cols="12" md="4">
                  <v-card 
                    variant="outlined" 
                    :loading="loading"
                    @click="selectOption(option)"
                    class="pa-4 text-center cursor-pointer hover-card"
                  >
                    <v-icon size="48" :color="option.color" class="mb-2">
                      {{ option.icon }}
                    </v-icon>
                    <h3 class="text-h6">{{ option.title }}</h3>
                    <p class="text-body-2 mt-2">{{ option.description }}</p>
                  </v-card>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
  
      <!-- Chat Interface -->
      <v-row v-else>
        <v-col cols="12">
          <v-card height="600" class="d-flex flex-column">
            <v-card-title class="d-flex align-center">
              <v-btn icon variant="text" @click="resetConversation" class="mr-2">
                <v-icon>mdi-arrow-left</v-icon>
              </v-btn>
              AI Workout Assistant
              <v-spacer></v-spacer>
              <v-chip color="primary" variant="outlined">
                {{ analysisStore.remainingMessages }} messages remaining today
              </v-chip>
            </v-card-title>
            
            <v-divider></v-divider>
  
            <!-- Messages Area -->
            <v-card-text 
              ref="messagesContainer"
              class="flex-grow-1 overflow-y-auto messages-container"
              style="height: 100%"
            >
              <!-- Debug: Show raw messages -->
              <div v-if="showDebug" class="mb-4 pa-2 bg-grey-lighten-4">
                <strong>Raw Messages:</strong>
                <pre>{{ JSON.stringify(analysisStore.messages, null, 2) }}</pre>
              </div>
  
              <div v-for="(message, index) in analysisStore.messages" :key="`msg-${index}-${message.timestamp}`" class="mb-4">
                <div :class="message.role === 'user' ? 'text-right' : ''">
                  <v-chip 
                    :color="message.role === 'user' ? 'primary' : 'secondary'"
                    variant="flat"
                    class="mb-2"
                  >
                    {{ message.role === 'user' ? 'You' : 'AI Assistant' }}
                  </v-chip>
                  <v-card 
                    :color="message.role === 'user' ? 'primary' : 'grey-lighten-4'"
                    :variant="message.role === 'user' ? 'flat' : 'tonal'"
                    class="pa-3"
                    :class="message.role === 'user' ? 'ml-auto' : 'mr-auto'"
                    style="max-width: 80%"
                  >
                    <div v-html="formatMessage(message.content)"></div>
                  </v-card>
                </div>
              </div>
              
              <!-- Loading indicator -->
              <div v-if="loading" class="text-center">
                <v-progress-circular indeterminate color="primary"></v-progress-circular>
                <p class="mt-2">AI is thinking...</p>
              </div>
            </v-card-text>
  
            <v-divider></v-divider>
  
            <!-- Input Area -->
            <v-card-actions class="pa-4">
              <v-row v-if="!analysisStore.hasReachedMessageLimit">
                <!-- Quick Action Buttons -->
                <v-col cols="12" v-if="showQuickActions && !userInput">
                  <div class="mb-2">
                    <v-chip 
                      v-for="action in availableQuickActions" 
                      :key="action.value"
                      @click="selectOption(action)"
                      class="mr-2 mb-2"
                      variant="outlined"
                      :disabled="loading"
                    >
                      {{ action.title }}
                    </v-chip>
                  </div>
                </v-col>
  
                <!-- Text Input -->
                <v-col cols="12">
                  <v-textarea
                    v-model="userInput"
                    :disabled="loading"
                    placeholder="Type your message or question..."
                    rows="2"
                    auto-grow
                    variant="outlined"
                    @keydown.enter.prevent="handleKeyPress"
                    hide-details
                  ></v-textarea>
                </v-col>
                
                <v-col cols="12" class="text-right">
                  <v-btn
                    color="primary"
                    :disabled="!userInput.trim() || loading"
                    @click="sendMessage"
                    append-icon="mdi-send"
                  >
                    Send
                  </v-btn>
                </v-col>
              </v-row>
              
              <v-row v-else>
                <v-col cols="12">
                  <v-alert type="warning" variant="tonal">
                    You've reached your daily message limit. Please come back tomorrow!
                  </v-alert>
                </v-col>
              </v-row>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
  
      <!-- Debug Toggle Button -->
      <v-btn
        color="secondary"
        variant="outlined"
        @click="showDebug = !showDebug"
        class="mt-4"
      >
        Toggle Debug Info
      </v-btn>
    </v-container>
  </template>
  
  <script>
  import { ref, computed, onMounted, nextTick, watch } from 'vue'
  import { useUserStore } from '@/stores/user'
  import { useAnalysisStore } from '@/stores/analysis'
  import { useWorkoutStore } from '@/stores/workout'
  
  export default {
    name: 'AnalysisPage',
    
    setup() {
      const userStore = useUserStore()
      const analysisStore = useAnalysisStore()
      const workoutStore = useWorkoutStore()
      
      const userInput = ref('')
      const loading = ref(false)
      const messagesContainer = ref(null)
      const showDebug = ref(false)
      
      const initialOptions = [
        {
          value: 'analyze_recent',
          title: 'Analyze My Recent Workouts',
          description: 'Get insights and recommendations based on your workout history',
          icon: 'mdi-chart-line',
          color: 'primary'
        },
        {
          value: 'plan_workout',
          title: 'Plan a Workout for Me',
          description: 'Get a personalized workout plan for your next session',
          icon: 'mdi-dumbbell',
          color: 'success'
        },
        {
          value: 'make_plan',
          title: 'Make a Workout Plan',
          description: 'Create a structured workout program to achieve your goals',
          icon: 'mdi-calendar-check',
          color: 'warning'
        }
      ]
      
      const showQuickActions = computed(() => {
        return analysisStore.messages.length > 0 && !analysisStore.hasReachedMessageLimit
      })
      
      const availableQuickActions = computed(() => {
        const lastSelected = analysisStore.lastSelectedOption
        return initialOptions.filter(opt => opt.value !== lastSelected)
      })
      
      const scrollToBottom = async () => {
        await nextTick()
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      }
      
      const formatMessage = (content) => {
        if (!content) return ''
        return content
          .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
          .replace(/\*(.*?)\*/g, '<em>$1</em>')
          .replace(/\n/g, '<br>')
          .replace(/• (.*?)(?=<br>|$)/g, '• $1<br>')
      }
      
      const handleKeyPress = (event) => {
        if (event.shiftKey) {
          return
        }
        sendMessage()
      }
      
      const selectOption = async (option) => {
        console.log('selectOption called with:', option)
        
        if (loading.value || analysisStore.hasReachedMessageLimit) {
          console.log('Blocked: loading or message limit reached')
          return
        }
        
        loading.value = true
        analysisStore.lastSelectedOption = option.value
        
        try {
          analysisStore.addMessage({
            role: 'user',
            content: option.title
          })
          
          console.log('Messages after adding user message:', analysisStore.messages)
          
          await nextTick()
          await scrollToBottom()
          
          const userData = userStore.currentUser
          console.log('User data:', userData)
          
          const recentWorkouts = await workoutStore.fetchUserWorkouts(userData.item_id)
          console.log('Fetched workouts:', recentWorkouts.data?.length || 0, 'workouts')
          
          console.log('Calling sendAnalysisRequest...')
          const response = await analysisStore.sendAnalysisRequest({
            option: option.value,
            userData: userData,
            workouts: recentWorkouts.data || []
          })
          
          console.log('Analysis response:', response)
          console.log('Messages after API call:', analysisStore.messages)
          
          await nextTick()
          
          if (response.success) {
            console.log('Response successful, scrolling to bottom')
            await scrollToBottom()
          } else {
            console.error('Response not successful:', response)
          }
        } catch (error) {
          console.error('Error in selectOption:', error)
          analysisStore.addMessage({
            role: 'assistant',
            content: 'I apologize, but I encountered an error. Please try again.'
          })
          await nextTick()
          await scrollToBottom()
        } finally {
          loading.value = false
          console.log('selectOption completed. Final messages:', analysisStore.messages)
        }
      }
      
      const sendMessage = async () => {
        if (!userInput.value.trim() || loading.value || analysisStore.hasReachedMessageLimit) return
        
        const message = userInput.value
        userInput.value = ''
        loading.value = true
        
        try {
          analysisStore.addMessage({
            role: 'user',
            content: message
          })
          
          await nextTick()
          await scrollToBottom()
          
          const userData = userStore.currentUser
          const recentWorkouts = await workoutStore.fetchUserWorkouts(userData.item_id)
          
          const response = await analysisStore.sendMessage({
            message: message,
            userData: userData,
            workouts: recentWorkouts.data || []
          })
          
          await nextTick()
          
          if (response.success) {
            await scrollToBottom()
          }
        } catch (error) {
          console.error('Error:', error)
          analysisStore.addMessage({
            role: 'assistant',
            content: 'I apologize, but I encountered an error. Please try again.'
          })
          await nextTick()
          await scrollToBottom()
        } finally {
          loading.value = false
        }
      }
      
      const resetConversation = () => {
        analysisStore.clearConversation()
      }
      
      watch(() => analysisStore.messages.length, async (newLength, oldLength) => {
        console.log('Messages length changed from', oldLength, 'to', newLength)
        if (newLength > oldLength) {
          await nextTick()
          await scrollToBottom()
        }
      })
      
      watch(() => analysisStore.messages, async (newMessages) => {
        console.log('Messages array changed:', newMessages)
        await nextTick()
        await scrollToBottom()
      }, { deep: true })
      
      onMounted(() => {
        console.log('Analysis page mounted')
        analysisStore.initializeStore()
        workoutStore.initializeWorkoutStore()
        
        console.log('Initial messages:', analysisStore.messages)
        console.log('Has active conversation:', analysisStore.hasActiveConversation)
      })
      
      return {
        userStore,
        analysisStore,
        workoutStore,
        userInput,
        loading,
        messagesContainer,
        showDebug,
        initialOptions,
        showQuickActions,
        availableQuickActions,
        formatMessage,
        handleKeyPress,
        selectOption,
        sendMessage,
        resetConversation
      }
    }
  }
  </script>
  
  <style scoped>
  .hover-card {
    transition: all 0.3s ease;
    cursor: pointer;
  }
  
  .hover-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  }
  
  .messages-container {
    background-color: #f5f5f5;
  }
  
  .messages-container::-webkit-scrollbar {
    width: 8px;
  }
  
  .messages-container::-webkit-scrollbar-track {
    background: #f1f1f1;
  }
  
  .messages-container::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
  }
  
  .messages-container::-webkit-scrollbar-thumb:hover {
    background: #555;
  }
  </style>