'use client'

import { useStore } from '@/lib/store'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { MessageCircle, Radio, Zap } from 'lucide-react'

export function TwitchSection() {
  const { twitchConnected, twitchStats } = useStore()

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Radio className="h-5 w-5" />
          Twitch
        </CardTitle>
        <CardDescription>
          {twitchConnected ? 'Connected' : 'Disconnected'}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid gap-2">
          <div className="flex justify-between">
            <span className="text-sm text-muted-foreground">Viewers</span>
            <span className="font-semibold">{twitchStats.viewers}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-muted-foreground">Followers</span>
            <span className="font-semibold">{twitchStats.followers}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-sm text-muted-foreground">Uptime</span>
            <span className="font-semibold">{twitchStats.uptime}h</span>
          </div>
        </div>

        <div
          className={`h-2 rounded-full ${
            twitchConnected ? 'bg-green-500' : 'bg-red-500'
          }`}
        />
      </CardContent>
    </Card>
  )
}
