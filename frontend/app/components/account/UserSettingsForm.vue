<template>
  <div class="max-w-3xl mx-auto space-y-6">
    <div class="flex items-center justify-end text-sm h-5">
      <div
        v-if="isSaving"
        class="flex items-center gap-2 text-primary"
      >
        <UIcon
          name="i-lucide-loader-2"
          class="animate-spin"
        />
        Saving...
      </div>

      <div
        v-else-if="saveSuccess"
        class="text-green-500"
      >
        Saved
      </div>

      <div
        v-else-if="saveError"
        class="text-red-500"
      >
        Error while saving
      </div>
    </div>

    <UCard>
      <template #header>
        <h2 class="font-semibold">
          Profile
        </h2>
      </template>

      <div class="space-y-6">
        <!-- TODO: -->
        <!-- <div class="flex items-center gap-6">
          <UAvatar
            :src="avatarPreview"
            :alt="profileForm.name"
            size="xl"
          />

          <div class="flex-1 space-y-2">
            <UFileUpload
              type="file"
              accept="image/*"
              @change="onAvatarChange"
            />
            <div class="text-xs text-muted">
              JPG, PNG. Replaces previous avatar.
            </div>
          </div>
        </div> -->

        <div class="flex gap-4">
          <UAvatar
            :src="avatarPreview"
            :alt="profileForm.name"
            size="xl"
          />
          <UInput
            v-model="profileForm.username"
            placeholder="Username"
            class="flex-1"
          />
          <UInput
            v-model="profileForm.name"
            placeholder="Display Name"
            class="flex-1"
          />
        </div>

        <!-- TODO: -->
        <!-- <UInput v-model="profileForm.email" type="email" label="Email" /> -->

        <UTextarea
          v-model="profileForm.bio"
          label="Bio"
          :rows="4"
          autoresize
          class="w-full"
          placeholder="Bio"
        />
      </div>
    </UCard>

    <!-- SETTINGS -->
    <UCard>
      <template #header>
        <h2 class="font-semibold">
          Privacy & Preferences
        </h2>
      </template>

      <div class="space-y-6">
        <UCheckbox
          v-model="settingsForm.allowDirectMessages"
          label="Allow direct messages"
        />
        <UCheckbox
          v-model="settingsForm.showOnlineStatus"
          label="Show my last seen"
        />

        <UFormField label="Who can invite me to rooms">
          <USelect
            v-model="settingsForm.whoCanInviteToRoom"
            :items="privacyOptions"
          />
        </UFormField>

        <UFormField label="Last seen visibility">
          <USelect
            v-model="settingsForm.lastSeenVisibility"
            :items="privacyOptions"
          />
        </UFormField>

        <UFormField label="Theme">
          <UColorModeSelect />
        </UFormField>

        <!-- TODO: -->
        <!-- <UFormField label="Language">
          <UInput v-model="settingsForm.language" />
        </UFormField> -->

        <USeparator label="Notifications" />

        <div class="grid md:grid-cols-2 gap-3">
          <UCheckbox
            v-model="settingsForm.notifyOnDirectMessage"
            label="Direct messages"
          />
          <UCheckbox
            v-model="settingsForm.notifyOnRoomMessage"
            label="Room messages"
          />
          <UCheckbox
            v-model="settingsForm.notifyOnMentions"
            label="Mentions"
          />
          <UCheckbox
            v-model="settingsForm.notifyOnRoomInvite"
            label="Room invites"
          />
        </div>
      </div>
    </UCard>
  </div>
</template>

<script setup lang="ts">
import { PrivacyLevel } from '~/types/account'

const { user, userSettings, updateUser, updateUserSettings } = useAccount()
const toast = useToast()

/* STATE */

const isSaving = ref(false)
const saveSuccess = ref(false)
const saveError = ref(false)

let saveTimer: NodeJS.Timeout | null = null
let initialized = false

/* PROFILE */

const profileForm = reactive({
  username: '',
  name: '',
  email: null as string | null,
  bio: null as string | null
})

const avatarFile = ref<File | null>(null)
const avatarPreview = ref<string | undefined>()

watchEffect(() => {
  if (!user.value) return

  profileForm.username = user.value.username
  profileForm.name = user.value.name
  profileForm.email = user.value.email
  profileForm.bio = user.value.bio

  avatarPreview.value = user.value.avatar ?? undefined

  initialized = true
})

// const onAvatarChange = (e: Event) => {
//   const file = (e.target as HTMLInputElement).files?.[0]
//   if (!file) return

//   avatarFile.value = file
//   avatarPreview.value = URL.createObjectURL(file)

//   triggerAutoSave()
// }

/* SETTINGS */

const settingsForm = reactive({
  allowDirectMessages: true,
  whoCanInviteToRoom: PrivacyLevel.EVERYONE,
  lastSeenVisibility: PrivacyLevel.EVERYONE,
  showOnlineStatus: true,
  notifyOnDirectMessage: true,
  notifyOnRoomMessage: true,
  notifyOnMentions: true,
  notifyOnRoomInvite: true,
  language: 'en'
})

watchEffect(() => {
  if (!userSettings.value) return
  Object.assign(settingsForm, userSettings.value)
})

/* OPTIONS */

const privacyOptions = [
  { label: 'Everyone', value: PrivacyLevel.EVERYONE },
  { label: 'Friends', value: PrivacyLevel.FRIENDS },
  { label: 'Nobody', value: PrivacyLevel.NOBODY }
]

/* AUTOSAVE */

watch(
  [profileForm, settingsForm],
  () => {
    if (!initialized) return
    triggerAutoSave()
  },
  { deep: true }
)

function triggerAutoSave() {
  if (saveTimer) clearTimeout(saveTimer)

  saveTimer = setTimeout(() => {
    saveAll()
  }, 2000)
}

async function saveAll() {
  isSaving.value = true
  saveSuccess.value = false
  saveError.value = false

  try {
    // PROFILE (multipart)
    const formData = new FormData()

    formData.append('username', profileForm.username)
    formData.append('name', profileForm.name)
    if (profileForm.email) formData.append('email', profileForm.email)
    if (profileForm.bio) formData.append('bio', profileForm.bio)
    if (avatarFile.value) formData.append('avatar', avatarFile.value)

    let saved: boolean = await updateUser(formData)

    // SETTINGS (json)
    if (saved) {
      saved = await updateUserSettings(settingsForm)
      if (!saved) {
        toast.add({ title: 'Failed to save settings', color: 'error' })
        saveError.value = true
        return
      }
    } else {
      toast.add({ title: 'Failed to save profile', color: 'error' })
      saveError.value = true
      return
    }

    avatarFile.value = null
    saveSuccess.value = true

    setTimeout(() => {
      saveSuccess.value = false
    }, 2000)
  } catch (e) {
    console.log(e)
    saveError.value = true
  } finally {
    isSaving.value = false
  }
}
</script>
