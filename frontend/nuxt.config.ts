// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },
  modules: [
    'vuetify-nuxt-module',
    '@pinia/nuxt'
  ],
  vuetify: {   
    vuetifyOptions: {
      theme: {
        defaultTheme: 'dark'
      }
    }
  }
})
