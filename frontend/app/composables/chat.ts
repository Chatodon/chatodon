import { useChatStore } from '~/stores/chat'
import type { UserMessageBrief } from '~/types/messages'

export const useChat = () => {
  const chatStore = useChatStore()

  const replyingTo = computed(() => chatStore.replyingTo)

  const reply = (replyTo: UserMessageBrief | null) => {
    chatStore.replyingTo = replyTo
  }

  return {
    replyingTo,
    reply
  }
}
