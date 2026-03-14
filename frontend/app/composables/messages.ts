import { useMessagesStore } from '~/stores/messages'
import type { PaginatedResponse } from '~/types/api'
import type { Message, MessageToSend } from '~/types/messages'

export const useMessages = () => {
  const api = useApi()
  const toast = useToast()
  const messagesStore = useMessagesStore()

  const messages = computed<Message[]>(() => messagesStore.messages.slice().reverse())
  const totalMessages = ref<number>(0)

  const fetchMessages = async (roomId: string, page: number = 1, clear: boolean = false) => {
    // clear - set current messages list to []
    const res = await api.get(`/messages/${roomId}/?page=${page}`)
    if (res?.ok) {
      const msgs = res.data as PaginatedResponse
      totalMessages.value = msgs.count || 0
      if (clear) {
        messagesStore.messages = []
      }
      messagesStore.messages = [
        ...messagesStore.messages,
        ...msgs.results as Message[]
      ]
    } else {
      toast.add({ title: 'Failed to load messages', color: 'error' })
    }
  }

  const createMessage = async (message: MessageToSend): Promise<Message | null> => {
    const res = await api.post('/messages/', message)
    if (res?.ok) {
      const msg = res.data as Message
      return msg
    }
    toast.add({ title: 'Failed to send message', color: 'error' })
    return null
  }

  const deleteMessage = async (message: Message): Promise<Message | null> => {
    const res = await api.del(`/messages/${message.id}/delete/`)
    if (res?.ok) {
      return res.data as Message
    }
    toast.add({ title: 'Failed to delete message', color: 'error' })
    return null
  }

  return {
    messages,
    totalMessages,
    fetchMessages,
    createMessage,
    deleteMessage
  }
}
