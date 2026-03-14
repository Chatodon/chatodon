<template>
  <UUser
    :name="accountStore.user?.name"
    :avatar="{
      alt: accountStore.user?.name,
      size: 'md'
    }"
    class="cursor-pointer"
    @click="onClick"
  />
</template>

<script setup lang="ts">
import { useAccountStore } from '~/stores/account'
import { useOverlaysStore } from '~/stores/overlays'

const accountStore = useAccountStore()
const overlaysStore = useOverlaysStore()

const onClick = () => {
  overlaysStore.userSettings = !overlaysStore.userSettings
  overlaysStore.sidebar = false
}
</script>
