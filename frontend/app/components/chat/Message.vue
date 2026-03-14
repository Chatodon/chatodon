<template>
  <div
    class="w-full flex items-end mb-2"
    :class="rowClass"
  >
    <!-- SYSTEM MESSAGE -->
    <template v-if="isSystem">
      <ChatSystemMessageBlock :message="systemMessage" />
    </template>

    <!-- USER MESSAGE -->
    <template v-else>
      <ChatUserMessageBlock :message="message" />
    </template>
  </div>
</template>

<script setup lang="ts">
import type { Message, SystemMessage } from '~/types/messages'

const { user } = useAccount()

const props = defineProps<{
  message: Message
}>()

const isSystem = computed(() => props.message.messageType === 'system')

const isOwn = computed(() =>
  props.message.sender?.id === user.value?.id
)

const systemMessage = ref<SystemMessage>(props.message as SystemMessage)

const rowClass = computed(() => {
  if (isSystem.value) return 'justify-center'
  return isOwn.value ? 'justify-end' : 'justify-start'
})
</script>
