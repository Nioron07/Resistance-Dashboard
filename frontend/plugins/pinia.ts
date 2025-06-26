// plugins/pinia.ts
import { type Pinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

export default ({ $pinia }: { $pinia: Pinia }) => {
  $pinia.use(piniaPluginPersistedstate)
}