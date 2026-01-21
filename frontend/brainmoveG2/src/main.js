import './style.css'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css' // Import Material Design Icons CSS

import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // Import the router
import { createVuetify } from 'vuetify'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

const vuetify = createVuetify({
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
})

const app = createApp(App)

app.use(router) // Use the router
app.use(vuetify)

app.mount('#app')