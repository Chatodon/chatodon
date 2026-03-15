<template>
  <div class="h-full flex flex-col">
  <div class="p-2">
    <UButton
      icon="i-lucide-plus"
      block
      variant="soft"
      @click="overlaysStore.createRoom = true"
    >
      New room
    </UButton>
  </div>
  <div
    ref="scrollContainer"
    class="flex-1 overflow-y-auto"
    @scroll="onScroll"
  >
    <template v-if="rooms.length">
      <UCard
        v-for="room in rooms"
        :key="room.id"
        :ui="{ body: 'p-2!' }"
        variant="soft"
        class="not-hover:bg-transparent cursor-pointer"
        @click="openRoom(room)"
      >
        <UUser
          :name="room.name"
          :avatar="{
            src: room.avatar || '',
            alt: room.name
          }"
          :ui="{
            description: 'text-nowrap overflow-hidden text-ellipsis',
            wrapper: 'flex-1'
          }"
        />
        <!-- TODO: Display the last message in the room via description prop -->
      </UCard>

      <div
        v-if="isLoading"
        class="p-3 text-center text-sm opacity-60"
      >
        <UIcon name="svg-spinners:ring-resize" />
      </div>
    </template>

    <UEmpty
      v-else
      title="No rooms found"
    />
  </div>
  </div>
</template>

<script setup lang="ts">
import { useOverlaysStore } from '~/stores/overlays'
import type { Room } from '~/types/rooms'

const overlaysStore = useOverlaysStore()
const { rooms, roomsTotal, setCurrentRoom, fetchRooms } = useRooms()

const page = ref(1)
const isLoading = ref(false)
const scrollContainer = ref<HTMLElement | null>(null)

const openRoom = (room: Room) => {
  overlaysStore.sidebar = false
  setCurrentRoom(room)
}

const loadMore = async () => {
  if (isLoading.value) return
  if (rooms.value.length >= roomsTotal.value) return

  isLoading.value = true
  page.value += 1

  try {
    await fetchRooms(page.value)
  } finally {
    isLoading.value = false
  }
}

const onScroll = () => {
  const el = scrollContainer.value
  if (!el) return

  const threshold = 150

  const isNearBottom = el.scrollHeight - el.scrollTop - el.clientHeight < threshold

  if (isNearBottom) {
    loadMore()
  }
}

onMounted(() => {
  fetchRooms(page.value)
})
</script>
