import type { User } from './account'

type RoomTypes = 'private' | 'group' | 'channel'

export interface Room {
  id: string // UUID
  name: string
  username: string | null
  description: string | null
  avatar: string | null // URL
  roomType: RoomTypes
  isPrivate: boolean
  isActive: boolean
  owner: User
  participants: User[] // The first five participants
  participantsCount: number
  createdAt: Date // ISO datetime
  updatedAt: Date // ISO datetime
}

export type Rooms = Room[]
