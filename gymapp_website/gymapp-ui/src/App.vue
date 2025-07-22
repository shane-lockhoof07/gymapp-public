<template>
    <v-app>
      <v-app-bar app>
        <v-toolbar-title>Jacked Up</v-toolbar-title>
        <v-btn to="/" text>
          Personal Dashboard
        </v-btn>
        
        <v-btn to="/workouts" text>
          Workouts
        </v-btn>
        
        <v-btn to="/analysis" text>
          Analysis
        </v-btn>
        
        <v-spacer></v-spacer>
        
        <!-- User status in navbar -->
        <div v-if="userStore.isLoggedIn" class="d-flex align-center">
          <v-chip class="mr-2">
            <v-icon start>mdi-account</v-icon>
            {{ userStore.username }}
          </v-chip>
          <v-btn icon @click="userStore.logout">
            <v-icon>mdi-logout</v-icon>
          </v-btn>
        </div>
      </v-app-bar>
  
      <v-main>
        <router-view />
      </v-main>
    </v-app>
  </template>
  
<script>
import { useUserStore } from '@/stores/user';
import { useRouter } from 'vue-router';

export default {
    name: 'App',
    
    setup() {
        const userStore = useUserStore()
        const router = useRouter();
        
        userStore.initializeAuth()
        
        return {
            userStore
        }
    }
}
</script>