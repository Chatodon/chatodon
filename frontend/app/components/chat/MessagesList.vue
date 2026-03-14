<template>
  <div>
    <div
      v-if="messages.length"
      ref="scrollContainer"
      class="relative h-full flex flex-col items-end overflow-y-auto overscroll-contain"
      @scroll="onScroll"
    >
      <ChatMessage
        v-for="message in messages"
        :key="message.id"
        :message="message"
      />

      <UButton
        v-if="showScrollToBottomButton"
        icon="i-lucide-chevron-down"
        size="xl"
        class="sticky bottom-1 right-1 cursor-pointer rounded-full shadow"
        @click="scrollToBottomSmooth"
      />
    </div>

    <div
      v-else
      class="h-full w-full flex items-center justify-center"
    >
      <UIcon
        name="svg-spinners:ring-resize"
        width="24"
        height="24"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
const { messages, totalMessages, fetchMessages } = useMessages()
const { currentRoom } = useRooms()
const { user } = useAccount()

const page = ref(1)
const isLoading = ref(false)
const scrollContainer = ref<HTMLElement | null>(null)
const showScrollToBottomButton = ref(false)
const { messageReceived, messageSent } = useEvents()

const scrollToBottomInstant = () => {
  const el = scrollContainer.value
  if (!el) return
  el.scrollTop = el.scrollHeight
}

const scrollToBottomSmooth = () => {
  const el = scrollContainer.value
  if (!el) return

  el.scrollTo({
    top: el.scrollHeight,
    behavior: 'smooth'
  })
}

const isAtBottom = (tolerance = 0) => {
  const el = scrollContainer.value
  if (!el) return true

  return el.scrollHeight - el.scrollTop - el.clientHeight <= tolerance
}

const shouldAutoScroll = ref(true)

const onScroll = async () => {
  const el = scrollContainer.value
  if (!el || isLoading.value) return

  showScrollToBottomButton.value = !isAtBottom(300)

  if (el.scrollTop > 0) return
  if (messages.value.length >= totalMessages.value) return

  isLoading.value = true

  const previousHeight = el.scrollHeight

  page.value += 1
  await fetchMessages(currentRoom.value.id, page.value)

  await nextTick()

  const newHeight = el.scrollHeight

  el.scrollTop = newHeight - previousHeight

  isLoading.value = false
}

onMounted(() => {
  messageReceived.on((event) => {
    if (event.room !== currentRoom.value?.id && event.sender?.id !== user.value?.id) return
    shouldAutoScroll.value = isAtBottom(100)
  })

  messageSent.on(() => {
    scrollToBottomSmooth()
  })

  shouldAutoScroll.value = isAtBottom(100)
})

watch(currentRoom, async () => {
  if (!currentRoom.value) return

  page.value = 1
  await fetchMessages(currentRoom.value.id, page.value, true)

  await nextTick()
  scrollToBottomInstant()
}, { deep: true, immediate: true })

watch(
  () => messages.value.length,
  async () => {
    await nextTick()
    if (!shouldAutoScroll.value) return
    scrollToBottomSmooth()
  }
)
</script>
