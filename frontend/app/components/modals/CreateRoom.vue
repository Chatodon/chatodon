<template>
  <UModal
    v-model:open="open"
    title="Create room"
    description="Set up a new room for your conversations"
    @update:open="onOpenChange"
  >
    <template #body>
      <RoomsCreateForm
        ref="formRef"
        @cancel="open = false"
        @created="open = false"
      />
    </template>
  </UModal>
</template>

<script setup lang="ts">
const open = defineModel<boolean>()

const formRef = ref()

const onOpenChange = (value: boolean) => {
  if (!value) {
    formRef.value?.reset()
  }
}
</script>
