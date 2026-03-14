<template>
  <div class="h-full max-h-full">
    <Chat v-if="currentRoom?.id" />
    <UEmpty
      v-else
      title="No  chat selected"
    />
  </div>
</template>

<script setup lang="ts">
definePageMeta({})

const { currentRoom } = useRooms()
</script>
