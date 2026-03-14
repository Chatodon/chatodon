export interface User {
  id: string // UUID
  username: string
  name: string
  email: string | null // Optional field
  avatar: string | null // URL or path to the avatar image
  bio: string | null // Optional field
  verified: boolean
  official: boolean
  banned: boolean
  createdAt: Date
  updatedAt: Date
}

export interface UserBrief {
  id: string // UUID
  username: string
  name: string
  avatar: string | null // URL or path to the avatar image
}

export interface UserSettings {
  user: User // One-to-One relationship with User
  isProfilePublic: boolean
  allowDirectMessages: boolean
  whoCanInviteToRoom: PrivacyLevel
  lastSeenVisibility: PrivacyLevel
  showOnlineStatus: boolean
  notifyOnDirectMessage: boolean
  notifyOnRoomMessage: boolean
  notifyOnMentions: boolean
  notifyOnRoomInvite: boolean
  language: string // Default is 'en'
  updatedAt: Date // ISO datetime
}

export enum PrivacyLevel {
  EVERYONE = 'everyone',
  FRIENDS = 'friends',
  NOBODY = 'nobody'
}
