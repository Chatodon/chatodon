<template>
  <div class="w-full">
    <UForm
      class="flex items-end"
      @submit.prevent="sendMessage"
    >
      <div class="flex-1 overflow-hidden">
        <div
          v-if="replyingTo"
          class="relative max-w-[90%] flex items-center text-xs opacity-70 border-l-2 px-2 py-1 mb-2 bg-linear-to-r from-accented to-transparent to-70%"
        >
          <div
            class="max-w-full pr-10 overflow-hidden text-nowrap text-ellipsis"
            :class="{ italic: !replyingTo.content }"
          >
            {{ replyingTo.content || 'Message deleted' }}
          </div>
          <UIcon
            name="i-lucide-x"
            class="absolute right-2 cursor-pointer"
            @click="reply(null)"
          />
        </div>
        <UTextarea
          ref="messageInputRef"
          v-model="message"
          class="w-full"
          variant="ghost"
          autoresize
          :maxrows="16"
          :loading="messageIsSending"
          :disabled="messageIsSending"
          placeholder="Write a message..."
          autofocus
          @keydown.enter="onEnterKeydown"
        />
      </div>
      <UButton
        type="submit"
        icon="i-lucide-send-horizontal"
        variant="ghost"
        class="h-fit cursor-pointer"
        :loading="messageIsSending"
        :disabled="messageIsSending"
      />
    </UForm>
  </div>
</template>

<script setup lang="ts">
import type { Message } from '~/types/messages'

const { createMessage } = useMessages()
const { currentRoom } = useRooms()
const { replyingTo, reply } = useChat()
const { messageSent } = useEvents()

const message = ref<string>('')
const messageIsSending = ref(false)
const messageInputRef = ref()

const sendMessage = () => {
  if ((!message.value.trim() && !messageIsSending.value) || !currentRoom.value?.id) return
  messageIsSending.value = true
  createMessage({
    room: currentRoom.value.id,
    content: message.value,
    replyTo: replyingTo.value?.id
  }).then((message: Message | null) => {
    if (message) messageSent.emit(message)
  }).finally(() => {
    messageIsSending.value = false
    message.value = ''
    nextTick(() => messageInputRef.value.textareaRef.focus())
    reply(null)
  })
}

// Send by pressing Enter, line break by pressing Shift+Enter
const onEnterKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey) {
    e.preventDefault() // prevent line break
    sendMessage()
  }
}
</script>
