<template>
  <UModal
    v-model:open="open"
    title="Raw message"
    description="Full content of the message"
  >
    <template #body>
      <pre class="max-w-full text-wrap text-xs overflow-y-auto">{{ overlaysStore.rawMessageContent }}</pre>
    </template>
  </UModal>
</template>

<script setup lang="ts">
import { useOverlaysStore } from '~/stores/overlays'

const open = defineModel<boolean>()

const overlaysStore = useOverlaysStore()
</script>
