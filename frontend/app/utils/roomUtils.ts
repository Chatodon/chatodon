import type { Room } from '~/types/rooms'

const getUsername = (room: Room): string => {
  if (room.isPrivate) {
    return ''
  }
  return room.username || ''
}

export default {
  getUsername
}
