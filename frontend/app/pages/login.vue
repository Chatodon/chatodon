<template>
  <div class="h-screen flex justify-center items-center">
    <UPageCard class="w-full max-w-md">
      <UAuthForm
        title="Login"
        description="Enter your credentials to access your account."
        :fields="fields"
        @submit="submitForm"
      />
    </UPageCard>
  </div>
</template>

<script setup lang="ts">
import type { AuthFormField, FormSubmitEvent } from '@nuxt/ui'

const account = useAccount()
const router = useRouter()

definePageMeta({
  layout: 'void'
})

const fields = ref<AuthFormField[]>([
  {
    name: 'username',
    type: 'text',
    label: 'Username'
  },
  {
    name: 'password',
    type: 'password',
    label: 'Password'
  }
])

type Schema = { username: string, password: string }

const submitForm = async (payload: FormSubmitEvent<Schema>) => {
  const logged = await account.login(payload.data.username, payload.data.password)
  if (logged) router.replace('/')
}
</script>
