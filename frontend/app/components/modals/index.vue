<template>
  <div>
    <ModalsUserSettings v-model="overlaysStore.userSettings" />
    <ModalsRawMessage v-model="overlaysStore.rawMessage" />
    <ModalsCreateRoom v-model="overlaysStore.createRoom" />
  </div>
</template>

<script setup lang="ts">
import { useOverlaysStore } from '~/stores/overlays'

const overlaysStore = useOverlaysStore()
</script>
