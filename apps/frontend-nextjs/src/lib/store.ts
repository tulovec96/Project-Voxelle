import { create } from 'zustand'
import { io, Socket } from 'socket.io-client'

export interface ServiceStatus {
  name: string
  status: 'running' | 'stopped' | 'error' | 'starting'
  uptime: number
  memory: number
  cpu: number
  version?: string
  lastPing?: number
}

export interface SystemMetrics {
  cpu: number
  memory: number
  memoryTotal: number
  latency: number
  requestsPerSecond: number
  errors: number
  uptime: number
  activeJobs: number
  completedJobs: number
}

export interface LogEntry {
  id: string
  timestamp: string
  level: 'info' | 'warn' | 'error' | 'debug'
  service: string
  message: string
}

export interface Notification {
  id: string
  type: 'info' | 'success' | 'warning' | 'error'
  title: string
  message: string
  timestamp: string
  read: boolean
}

export interface ChatMessage {
  id: string
  author: string
  message: string
  timestamp: string
  source: 'user' | 'ai' | 'system'
}

interface Store {
  socket: Socket | null
  isConnected: boolean
  currentMessage: string
  nextMessage: string
  aiThinking: boolean
  aiSpeaking: boolean
  humanSpeaking: boolean
  patiencePercent: number
  totalTime: number
  
  // Twitch
  twitchChat: ChatMessage[]
  twitchChatEnabled: boolean
  twitchConnected: boolean
  twitchStats: { viewers: number; followers: number; uptime: number }
  
  // Discord
  discordConnected: boolean
  discordStats: { servers: number; users: number; uptime: number }
  
  // VTS
  vtsStatus: 'connected' | 'disconnected' | 'connecting'
  
  // Features
  llmEnabled: boolean
  ttsEnabled: boolean
  sttEnabled: boolean
  multimodalEnabled: boolean
  movementEnabled: boolean
  selectedAudio: string
  songs: string[]
  
  // System
  metrics: SystemMetrics | null
  serviceStatus: ServiceStatus[]
  logs: LogEntry[]
  notifications: Notification[]
  
  // Actions
  initializeSocket: (url?: string) => void
  disconnectSocket: () => void
  abortMessage: () => void
  cancelMessage: () => void
  addMessage: (msg: ChatMessage) => void
  updateMetrics: (metrics: SystemMetrics) => void
  updateServiceStatus: (status: ServiceStatus[]) => void
  addLog: (log: LogEntry) => void
  addNotification: (notification: Notification) => void
}

export const useStore = create<Store>((set) => ({
  socket: null,
  isConnected: false,
  currentMessage: '',
  nextMessage: '',
  aiThinking: false,
  aiSpeaking: false,
  humanSpeaking: false,
  patiencePercent: 0,
  totalTime: 0,
  
  twitchChat: [],
  twitchChatEnabled: false,
  twitchConnected: false,
  twitchStats: { viewers: 0, followers: 0, uptime: 0 },
  
  discordConnected: false,
  discordStats: { servers: 0, users: 0, uptime: 0 },
  
  vtsStatus: 'disconnected',
  
  llmEnabled: true,
  ttsEnabled: true,
  sttEnabled: true,
  multimodalEnabled: false,
  movementEnabled: false,
  selectedAudio: 'default',
  songs: [],
  
  metrics: null,
  serviceStatus: [],
  logs: [],
  notifications: [],
  
  initializeSocket: (url = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000') => {
    set((state) => {
      if (state.socket?.connected) {
        return state
      }

      const newSocket = io(url, {
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
        reconnectionAttempts: 5,
      })

      newSocket.on('connect', () => {
        set({ isConnected: true })
      })

      newSocket.on('disconnect', () => {
        set({ isConnected: false })
      })

      newSocket.on('current_message', (data: string) => {
        set({ currentMessage: data })
      })

      newSocket.on('next_message', (data: string) => {
        set({ nextMessage: data })
      })

      newSocket.on('AI_thinking', (data: boolean) => {
        set({ aiThinking: data })
      })

      newSocket.on('AI_speaking', (data: boolean) => {
        set({ aiSpeaking: data })
      })

      newSocket.on('human_speaking', (data: boolean) => {
        set({ humanSpeaking: data })
      })

      newSocket.on('patience_percent', (data: number) => {
        set({ patiencePercent: data })
      })

      newSocket.on('total_time', (data: number) => {
        set({ totalTime: data })
      })

      newSocket.on('twitchChat', (msg: ChatMessage) => {
        set((state) => ({
          twitchChat: [...state.twitchChat, msg],
        }))
      })

      newSocket.on('metrics', (data: SystemMetrics) => {
        set({ metrics: data })
      })

      newSocket.on('service_status', (data: ServiceStatus[]) => {
        set({ serviceStatus: data })
      })

      newSocket.on('log', (data: LogEntry) => {
        set((state) => ({
          logs: [...state.logs, data].slice(-100),
        }))
      })

      return { socket: newSocket }
    })
  },

  disconnectSocket: () => {
    set((state) => {
      state.socket?.disconnect()
      return { socket: null, isConnected: false }
    })
  },

  abortMessage: () => {
    set((state) => {
      state.socket?.emit('abort_current_message')
      return state
    })
  },

  cancelMessage: () => {
    set((state) => {
      state.socket?.emit('cancel_next_message')
      return state
    })
  },

  addMessage: (msg: ChatMessage) => {
    set((state) => ({
      twitchChat: [...state.twitchChat, msg],
    }))
  },

  updateMetrics: (metrics: SystemMetrics) => {
    set({ metrics })
  },

  updateServiceStatus: (status: ServiceStatus[]) => {
    set({ serviceStatus: status })
  },

  addLog: (log: LogEntry) => {
    set((state) => ({
      logs: [...state.logs, log].slice(-100),
    }))
  },

  addNotification: (notification: Notification) => {
    set((state) => ({
      notifications: [...state.notifications, notification],
    }))
  },
}))
