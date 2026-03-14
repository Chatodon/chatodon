import type { DropdownMenuItem } from '@nuxt/ui'
import { useOverlaysStore } from '~/stores/overlays'
import type { Message } from '~/types/messages'

export const useMessage = (message: Ref<Message>) => {
  const api = useApi()
  const toast = useToast()
  const { reply } = useChat()
  const overlaysStore = useOverlaysStore()

  const dropdownItems = computed<DropdownMenuItem[][]>(() => {
    const items: DropdownMenuItem[][] = [[
      {
        label: 'Reply',
        icon: 'i-lucide-reply',
        onSelect: setReplying
      },
      {
        label: 'Show raw message',
        icon: 'i-lucide-file-braces',
        onSelect: showRaw
      }
    ]]

    if (!message.value.isDeleted) {
      items[0]?.push({
        label: 'Delete',
        icon: 'i-lucide-trash',
        color: 'error',
        onSelect: deleteMessage
      })
    }

    return items
  })

  const deleteMessage = async (): Promise<boolean> => {
    const res = await api.del(`/messages/${message.value.id}/delete/`)
    if (res?.ok) {
      return true
    }
    toast.add({ title: 'Failed to delete message', color: 'error' })
    return false
  }

  const setReplying = () => {
    reply({
      id: message.value.id,
      content: message.value.content || null
    })
  }

  const showRaw = () => {
    overlaysStore.rawMessage = true
    overlaysStore.rawMessageContent = message.value
  }

  return {
    dropdownItems,
    deleteMessage
  }
}
