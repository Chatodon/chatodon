export const useSystemStore = defineStore('System', () => {
  const wsConnecting = ref<boolean>(false)
  return {
    wsConnecting
  }
})
