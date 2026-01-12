'use client'

import { useStore } from '@/lib/store'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Clock, X } from 'lucide-react'

export function NextMessageSection() {
  const { nextMessage, cancelMessage } = useStore()

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Clock className="h-5 w-5" />
          Next Message
        </CardTitle>
        <CardDescription>Queued for processing</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="min-h-20 rounded-lg bg-secondary p-4 font-mono text-sm">
          {nextMessage || 'No message queued'}
        </div>
        
        <Button
          variant="outline"
          className="w-full"
          onClick={cancelMessage}
          disabled={!nextMessage}
        >
          <X className="mr-2 h-4 w-4" />
          Cancel
        </Button>
      </CardContent>
    </Card>
  )
}
