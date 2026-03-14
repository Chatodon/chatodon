import type { Message } from '~/types/messages'

export const useMessagesStore = defineStore('Messages', () => {
  const messages = ref<Message[]>([])

  const addMessage = (message: Message) => {
    messages.value.unshift(message)
  }

  // Update the message in messages
  const updateMessage = (message: Message) => {
    messages.value = messages.value.map((msg: Message) => msg.id === message.id ? message : msg)
  }

  return {
    messages,
    addMessage,
    updateMessage
  }
})
