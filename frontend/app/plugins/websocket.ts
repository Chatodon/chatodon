import { useMessagesStore } from '~/stores/messages'
import { useSystemStore } from '~/stores/system'
import type { Message } from '~/types/messages'

interface WsCreatedMessage {
  message: Message
  roomId: string
  type: string
}

export default defineNuxtPlugin(() => {
  const messagesStore = useMessagesStore()
  const systemStore = useSystemStore()
  const { messageReceived } = useEvents()

  let socket: WebSocket | null = null

  let reconnectTimer: ReturnType<typeof setTimeout> | null = null

  const scheduleReconnect = () => {
    if (reconnectTimer) return
    reconnectTimer = setTimeout(() => {
      reconnectTimer = null
      connect()
    }, 3000)
  }

  const connect = () => {
    systemStore.wsConnecting = true
    if (socket) return
    console.debug('WebSocket connecting...')

    const config = useRuntimeConfig()

    socket = new WebSocket(`${config.public.wsBase}`)
    // const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    // const host = window.location.host
    // socket = new WebSocket(`${protocol}//${host}${config.public.wsBase}`)

    console.debug('Socket:', socket)

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data) as WsCreatedMessage
      messageReceived.emit(data.message)

      switch (data.type) {
        case 'message.created':
          messagesStore.addMessage(data.message)
          break
        case 'message.updated':
          messagesStore.updateMessage(data.message)
          break
      }
    }

    socket.onclose = () => {
      socket = null
      systemStore.wsConnecting = true
      console.debug('WebSocket closed.')
      scheduleReconnect()
    }

    socket.onerror = () => {
      socket = null
      systemStore.wsConnecting = true
      console.debug('WebSocket error.')
      scheduleReconnect()
    }

    socket.onopen = () => {
      console.debug('WebSocket connected')
      systemStore.wsConnecting = false
    }
  }

  // onMounted(connect)
  connect()

  return {
    provide: {
      websocket: {
        connect
      }
    }
  }
})
