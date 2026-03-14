<template>
  <div>
    <ModalsUserSettings v-model="overlaysStore.userSettings" />
    <ModalsRawMessage v-model="overlaysStore.rawMessage" />
  </div>
</template>

<script setup lang="ts">
import { useOverlaysStore } from '~/stores/overlays'

const overlaysStore = useOverlaysStore()
</script>
