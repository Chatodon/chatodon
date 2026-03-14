import { useRoomsStore } from '~/stores/rooms'
import type { PaginatedResponse } from '~/types/api'
import type { Room, Rooms } from '~/types/rooms'

export const useRooms = () => {
  const toast = useToast()
  const api = useApi()
  const roomsStore = useRoomsStore()

  const rooms = computed<Rooms>(() => {
    // TODO: Rooms filtering
    return roomsStore.rooms
  })
  const currentRoom = computed<Room>(() => roomsStore.room)
  const roomsTotal = ref<number>(0)

  const fetchRooms = async (page: number = 1) => {
    const res = await api.get(`/rooms/my/?page=${page}`)
    if (res?.ok) {
      const data = res.data as PaginatedResponse
      const rms = data.results as Rooms
      roomsStore.rooms = [...roomsStore.rooms, ...rms]
      roomsStore.removeDuplicates()
      roomsTotal.value = data.count
      sortRooms()
    }
  }

  const updateRoom = async (room: Room, updateOrder: boolean = false) => {
    roomsStore.rooms = roomsStore.rooms.map((r: Room) => r.id === room.id ? { ...room } : r)
    if (updateOrder) {
      sortRooms()
    }
  }

  const setCurrentRoom = async (room: Room) => {
    const res = await api.get(`/rooms/${room.id}/`)
    if (res?.ok) {
      const data = res.data as Room
      roomsStore.room = data
    } else {
      toast.add({
        title: 'Failed to open the room',
        color: 'error'
      })
    }
  }

  const sortRooms = () => {
    roomsStore.rooms.sort((a, b) => Number(new Date(b.updatedAt)) - Number(new Date(a.updatedAt)))
  }

  return {
    rooms,
    currentRoom,
    roomsTotal,

    fetchRooms,
    updateRoom,
    setCurrentRoom
  }
}
