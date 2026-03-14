import { useEventBus } from '@vueuse/core'
import type { Message } from '~/types/messages'

export const useEvents = () => {
  const messageSent = useEventBus<Message>('chat:message:sending')
  const messageReceived = useEventBus<Message>('chat:message:received')

  return {
    messageSent,
    messageReceived
  }
}
