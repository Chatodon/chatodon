<template>
  <div class="space-y-4">
    <UFormField
      label="Name"
      required
    >
      <UInput
        v-model="form.name"
        placeholder="Room name"
        class="w-full"
      />
    </UFormField>

    <UFormField label="Description">
      <UTextarea
        v-model="form.description"
        placeholder="Description (optional)"
        :rows="3"
        autoresize
        class="w-full"
      />
    </UFormField>

    <UFormField label="Type">
      <USelect
        v-model="form.roomType"
        :items="roomTypeOptions"
        class="w-full"
      />
    </UFormField>

    <UCheckbox
      v-model="form.isPublic"
      label="Public room"
    />

    <UFormField
      v-if="form.isPublic"
      label="Username"
    >
      <UInput
        v-model="form.username"
        placeholder="e.g. my-room"
        class="w-full"
      />
    </UFormField>

    <div class="flex justify-end gap-2 pt-2">
      <UButton
        variant="ghost"
        @click="emit('cancel')"
      >
        Cancel
      </UButton>
      <UButton
        :loading="isSubmitting"
        :disabled="!form.name.trim()"
        @click="submit"
      >
        Create
      </UButton>
    </div>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{
  cancel: []
  created: []
}>()

const { createRoom, setCurrentRoom } = useRooms()

const isSubmitting = ref(false)

const form = reactive({
  name: '',
  description: '',
  username: '',
  roomType: 'group' as 'group' | 'channel',
  isPublic: false
})

const roomTypeOptions = [
  { label: 'Group', value: 'group' },
  { label: 'Channel', value: 'channel' }
]

const reset = () => {
  form.name = ''
  form.description = ''
  form.username = ''
  form.roomType = 'group'
  form.isPublic = false
}

const submit = async () => {
  if (!form.name.trim()) return

  isSubmitting.value = true
  try {
    const room = await createRoom({
      name: form.name.trim(),
      description: form.description || null,
      username: form.isPublic ? (form.username.trim() || null) : null,
      roomType: form.roomType,
      isPublic: form.isPublic
    })
    if (room) {
      await setCurrentRoom(room)
      reset()
      emit('created')
    }
  } finally {
    isSubmitting.value = false
  }
}

defineExpose({ reset })
</script>
