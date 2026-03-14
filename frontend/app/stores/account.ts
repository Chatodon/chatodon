import type { User, UserSettings } from '~/types/account'

export const useAccountStore = defineStore('Account', () => {
  const user = ref<User>()
  const userSettings = ref<UserSettings>()

  const setUser = (u: User) => {
    user.value = u
  }

  return {
    user,
    userSettings,
    setUser
  }
})
