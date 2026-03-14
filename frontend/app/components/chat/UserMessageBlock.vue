<template>
  <!-- Avatar (only for incoming) -->
  <UAvatar
    v-if="!isOwn"
    :src="message.sender?.avatar || ''"
    :alt="message.sender?.name"
    size="sm"
    class="mr-1 mt-1"
  />

  <div class="max-w-[90%] flex flex-col">
    <!-- Sender name -->
    <div
      v-if="!isOwn"
      class="text-xs text-gray-500 mb-1"
    >
      {{ message.sender?.name || message.sender?.username }}
    </div>

    <!-- Bubble -->
    <div
      class="px-3 py-2 rounded-lg text-sm wrap-break-word"
      :class="bubbleClass"
      @click.right.prevent="dropdownOpen = true"
    >
      <!-- Reply block -->
      <div
        v-if="message.replyTo"
        class="text-xs opacity-70 border-l-2 pl-2 py-1 mb-2 line-clamp-4"
      >
        <div
          v-if="message.replyTo.isDeleted"
          class="italic opacity-60"
        >
          Message deleted
        </div>
        <div v-else>
          {{ message.replyTo.content }}
        </div>
      </div>

      <!-- Deleted -->
      <div
        v-if="message.isDeleted"
        class="italic opacity-60"
      >
        Message deleted
      </div>

      <!-- Content -->
      <p
        v-else
        class="whitespace-pre-wrap"
      >
        {{ message.content }}
      </p>

      <!-- Meta and controls -->
      <div
        class="w-full flex items-center gap-1 text-[10px] mt-1 opacity-60 justify-between"
        :class="{ 'flex-row-reverse': isOwn }"
      >
        <div class="flex gap-1 items-center select-none">
          <span>{{ formattedTime }}</span>
          <UIcon
            v-if="message.isEdited"
            name="i-lucide-pencil"
          />
        </div>

        <UDropdownMenu
          v-model:open="dropdownOpen"
          :items="dropdownItems"
        >
          <UIcon
            name="i-lucide-ellipsis-vertical"
            class="cursor-pointer"
          />
        </UDropdownMenu>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Message } from '~/types/messages'

const props = defineProps<{
  message: Message
}>()

const compMsg = computed(() => props.message)

const { user } = useAccount()
const { dropdownItems } = useMessage(compMsg)

const isOwn = computed(() =>
  props.message.sender?.id === user.value?.id
)

const bubbleClass = computed(() => {
  if (isOwn.value) {
    return 'bg-primary-200 dark:bg-primary-800 rounded-br-xs'
  }
  return 'bg-neutral-100 dark:bg-neutral-800 rounded-bl-xs'
})

const formattedTime = computed(() => {
  const date = new Date(props.message.createdAt)
  return date.toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  })
})

const dropdownOpen = ref(false)
</script>
