/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

console.log('main.js: Starting app initialization')

// Plugins
import { registerPlugins } from '@/plugins'

// Components
import App from './App.vue'

// Composables
import { createApp } from 'vue'

// Styles
// import 'unfonts.css'  // Commented out to test

console.log('main.js: Imports completed')

const app = createApp(App)
console.log('main.js: Vue app created')

try {
    registerPlugins(app)
    console.log('main.js: Plugins registered successfully')
} catch (error) {
    console.error('main.js: Error registering plugins:', error)
}

try {
    app.mount('#app')
    console.log('main.js: App mounted successfully')
} catch (error) {
    console.error('main.js: Error mounting app:', error)
}