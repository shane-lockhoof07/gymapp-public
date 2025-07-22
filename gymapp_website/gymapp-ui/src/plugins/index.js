/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

// Plugins
import vuetify from './vuetify'
import router from '@/router'
import { createPinia } from 'pinia'

export function registerPlugins (app) {
  const pinia = createPinia()
  
  app
    .use(pinia)
    .use(vuetify)
    .use(router)
}