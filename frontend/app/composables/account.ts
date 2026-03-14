import { useAccountStore } from '~/stores/account'
import type { User, UserSettings } from '~/types/account'

export const useAccount = () => {
  const api = useApi()
  const toast = useToast()
  const accountStore = useAccountStore()
  const user = computed(() => accountStore.user)
  const userSettings = computed(() => accountStore.userSettings)

  const login = async (username: string, password: string): Promise<boolean> => {
    try {
      const res = await api.post('/account/login/', { username, password })
      if (!res) {
        toast.add({ title: 'Login request error', color: 'error' })
        return false
      }

      if (res.ok) {
        const data = res.data as { user: User }
        accountStore.setUser(data.user)
        return true
      }

      toast.add({ title: 'Invalid credentials', color: 'error' })
      return false
    } catch (err: unknown) {
      toast.add({ title: 'Unknown error happened', description: String(err) })
      return false
    }
  }

  const logout = async (): Promise<void> => {
    try {
      const res = await api.post('/account/logout/', {})
      if (res?.ok) accountStore.setUser({} as User)
    } catch {
      // silent fail
    }
  }

  const getMe = async (): Promise<boolean> => {
    try {
      const res = await api.get('/account/me/')
      if (!res) {
        return false
      }

      if (res.ok) {
        const data = res.data as { user: User, settings: UserSettings }
        accountStore.setUser(data.user)
        console.debug('Login successful')
        return true
      }
      return false
    } catch (err: unknown) {
      console.error(err)
      return false
    }
  }

  const updateUser = async (usr: FormData | Partial<User>): Promise<boolean> => {
    const res = await api.patch('/account/me/', usr)
    if (res?.ok) {
      return true
    }
    return false
  }

  const updateUserSettings = async (usrStgs: FormData | Partial<UserSettings>): Promise<boolean> => {
    const res = await api.patch('/account/settings/', usrStgs)
    if (res?.ok) {
      return true
    }
    return false
  }

  return {
    user,
    userSettings,

    login,
    logout,
    getMe,
    updateUser,
    updateUserSettings
  }
}
