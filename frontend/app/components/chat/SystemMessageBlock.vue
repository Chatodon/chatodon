<template>
  <UTooltip
    :text="createdAt"
    :content="{ side: 'top', sideOffset: 0 }"
    arrow
  >
    <div class="text-xs bg-gray-100 dark:bg-gray-800 px-3 py-1 rounded-full cursor-default">
      {{ text }}
    </div>
  </UTooltip>
</template>

<script setup lang="ts">
import type { SystemMessage } from '~/types/messages'

const props = defineProps<{
  message: SystemMessage
}>()

const text = computed(() => {
  switch (props.message.payload.action) {
    case 'room_created':
      return 'Room created'
    case 'user_joined':
      return `User ${props.message.sender?.name || 'Deleted account'} joined`
    default:
      return ''
  }
})

const createdAt = computed(() => {
  const date = new Date(props.message.createdAt)
  return String(date.toLocaleString())
})
</script>
