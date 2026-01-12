'use client'

import { useStore } from '@/lib/store'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Eye } from 'lucide-react'

export function VTSSection() {
  const { vtsStatus } = useStore()

  const statusColor = {
    connected: 'bg-green-500',
    disconnected: 'bg-red-500',
    connecting: 'bg-yellow-500',
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Eye className="h-5 w-5" />
          VTube Studio
        </CardTitle>
        <CardDescription className="capitalize">
          {vtsStatus}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-sm text-muted-foreground">
          Control VTube Studio avatar
        </p>

        <div className={`h-3 rounded-full ${statusColor[vtsStatus]}`} />
      </CardContent>
    </Card>
  )
}
