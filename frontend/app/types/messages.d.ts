import type { UserBrief } from './account'

export type MessageType = 'user' | 'system'
export type SystemMessageAction = 'room_created' | 'user_joined'

export interface SystemMessagePayload {
  action: SystemMessageAction
  user?: UserBrief
  createdAt: string // ISO datetime
}

export interface MessageAttachment {
  id: string // UUID
  message: Message
  file: string // URL
  fileType: string
  fileSize: number
  createdAt: string // ISO datetime
}

export interface Message {
  id: number

  room: string
  sender: UserBrief | null

  content?: string

  messageType: MessageType
  payload?: SystemMessagePayload

  isEdited: boolean
  isDeleted: boolean

  replyTo: Message

  createdAt: string // ISO datetime
  updatedAt: string // ISO datetime

  attachments: MessageAttachment[]
}

export interface UserMessageBrief {
  id: number
  content: string | null
}

export interface MessageToSend {
  room: string
  content: string
  replyTo?: number

  attachments?: MessageAttachment[]
}

export interface SystemMessage extends Message {
  payload: SystemMessagePayload
}
