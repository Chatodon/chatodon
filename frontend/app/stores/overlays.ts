export const useOverlaysStore = defineStore('Overlays', () => {
  const userSettings = ref<boolean>(false)

  const sidebar = ref<boolean>(false)

  const rawMessage = ref<boolean>(false)
  const rawMessageContent = ref<unknown>()

  const createRoom = ref<boolean>(false)

  return {
    userSettings,
    sidebar,
    rawMessage,
    rawMessageContent,
    createRoom
  }
})
