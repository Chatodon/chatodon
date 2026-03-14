<template>
  <UDashboardNavbar>
    <template #left>
      <div
        v-if="currentRoom?.id"
        class="flex items-center gap-3"
      >
        <UButton
          icon="i-lucide-arrow-left"
          color="neutral"
          variant="ghost"
          class="rounded-full cursor-pointer"
        />
        <UUser
          :name="currentRoom.name"
          :avatar="{
            src: currentRoom.avatar || '',
            alt: currentRoom.name
          }"
        />
      </div>
    </template>
    <template #right>
      <div class="flex gap-2 transition-all overflow-hidden">
        <UColorModeSwitch />
        <UIcon
          v-if="systemStore.wsConnecting"
          name="svg-spinners:ring-resize"
        />
      </div>
    </template>
  </UDashboardNavbar>
</template>

<script setup lang="ts">
import { useSystemStore } from '~/stores/system'

const { currentRoom } = useRooms()

const systemStore = useSystemStore()
</script>
