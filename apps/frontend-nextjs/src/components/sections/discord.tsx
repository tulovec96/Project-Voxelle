'use client'

import { useStore } from '@/lib/store'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Users } from 'lucide-react'

export function DiscordSection() {
  const { discordConnected, discordStats } = useStore()

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Users className="h-5 w-5" />
          Discord
        </CardTitle>
        <CardDescription>
          {discordConnected ? 'Connected' : 'Disconnected'}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid gap-2">
          <div className="flex justify-between">
            <span className="text-sm text-muted-foreground">Servers</span>
            <span className="font-semibold">{discordStats.servers}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-muted-foreground">Users</span>
            <span className="font-semibold">{discordStats.users}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-muted-foreground">Uptime</span>
            <span className="font-semibold">{discordStats.uptime}h</span>
          </div>
        </div>

        <div
          className={`h-2 rounded-full ${
            discordConnected ? 'bg-green-500' : 'bg-red-500'
          }`}
        />
      </CardContent>
    </Card>
  )
}
