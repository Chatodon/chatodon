export const useOverlaysStore = defineStore('Overlays', () => {
  const userSettings = ref<boolean>(false)

  const sidebar = ref<boolean>(false)

  const rawMessage = ref<boolean>(false)
  const rawMessageContent = ref<unknown>()

  return {
    userSettings,
    sidebar,
    rawMessage,
    rawMessageContent
  }
})
