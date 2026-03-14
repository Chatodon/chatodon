<template>
  <UDashboardGroup unit="rem">
    <UDashboardSidebar
      v-model:open="overlaysStore.sidebar"
      resizable
      class="bg-elevated/25"
      :ui="{
        footer: 'lg:border-t lg:border-default'
      }"
    >
      <template #header>
        <SidebarLogo />
      </template>
      <template #default>
        <RoomsList />
      </template>
      <template #footer>
        <SidebarUser />
      </template>
    </UDashboardSidebar>
    <UDashboardPanel>
      <template #header>
        <Header />
      </template>
      <template #body>
        <slot />
      </template>
    </UDashboardPanel>
  </UDashboardGroup>
</template>

<script setup lang="ts">
import { useOverlaysStore } from '~/stores/overlays'

const overlaysStore = useOverlaysStore()
</script>
