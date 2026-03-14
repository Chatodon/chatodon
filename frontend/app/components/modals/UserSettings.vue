<template>
  <UModal
    v-model:open="open"
    title="User settings"
    description="Configure your preferences and account settings"
  >
    <template #body>
      <AccountUserSettingsForm />
    </template>
  </UModal>
</template>

<script setup lang="ts">
const open = defineModel<boolean>()
</script>
