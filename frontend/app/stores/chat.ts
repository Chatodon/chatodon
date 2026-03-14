import type { UserMessageBrief } from '~/types/messages'

export const useChatStore = defineStore('Chat', () => {
  const replyingTo = ref<UserMessageBrief | null>(null)
  return {
    replyingTo
  }
})
