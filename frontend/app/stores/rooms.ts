import type { Room, Rooms } from '~/types/rooms'

export const useRoomsStore = defineStore('Rooms', () => {
  const room = ref<Room>({} as Room) // Current opened room
  const rooms = ref<Rooms>([]) // List of all Loaded rooms

  const removeDuplicates = () => {
    const seenIds = new Set<string>()
    rooms.value = rooms.value.filter((room: Room) => {
      if (seenIds.has(room.id)) {
        return false
      }
      seenIds.add(room.id)
      return true
    })
  }

  return {
    room,
    rooms,

    removeDuplicates
  }
})
