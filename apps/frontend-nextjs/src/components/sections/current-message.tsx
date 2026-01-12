'use client'

import { useStore } from '@/lib/store'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { MessageCircle, Pause, Play, StopCircle } from 'lucide-react'

export function CurrentMessageSection() {
  const { currentMessage, aiSpeaking, abortMessage } = useStore()

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <MessageCircle className="h-5 w-5" />
          Current Message
        </CardTitle>
        <CardDescription>What the AI is currently saying</CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="min-h-20 rounded-lg bg-secondary p-4 font-mono text-sm">
          {currentMessage || 'Waiting for message...'}
        </div>
        
        <div className="flex gap-2">
          <Button
            variant={aiSpeaking ? 'default' : 'outline'}
            size="sm"
            className="flex-1"
            disabled={!aiSpeaking}
          >
            {aiSpeaking ? (
              <>
                <Pause className="mr-2 h-4 w-4" />
                Speaking
              </>
            ) : (
              <>
                <Play className="mr-2 h-4 w-4" />
                Ready
              </>
            )}
          </Button>
          
          <Button
            variant="destructive"
            size="sm"
            onClick={abortMessage}
            disabled={!aiSpeaking}
          >
            <StopCircle className="mr-2 h-4 w-4" />
            Stop
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}
