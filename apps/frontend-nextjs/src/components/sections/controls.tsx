'use client'

import { useStore } from '@/lib/store'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Switch } from '@/components/ui/switch'
import { Zap, Brain, Radio, Mic } from 'lucide-react'

export function ControlsSection() {
  const {
    llmEnabled,
    ttsEnabled,
    sttEnabled,
    multimodalEnabled,
    movementEnabled,
    socket,
  } = useStore()

  const toggleFeature = (feature: string, enabled: boolean) => {
    if (socket) {
      socket.emit(`toggle_${feature}`, !enabled)
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Zap className="h-5 w-5" />
          Feature Controls
        </CardTitle>
        <CardDescription>Enable/disable features in real-time</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">LLM</span>
            <Switch
              checked={llmEnabled}
              onCheckedChange={() => toggleFeature('llm', llmEnabled)}
            />
          </div>

          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">TTS</span>
            <Switch
              checked={ttsEnabled}
              onCheckedChange={() => toggleFeature('tts', ttsEnabled)}
            />
          </div>

          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">STT</span>
            <Switch
              checked={sttEnabled}
              onCheckedChange={() => toggleFeature('stt', sttEnabled)}
            />
          </div>

          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">Multimodal</span>
            <Switch
              checked={multimodalEnabled}
              onCheckedChange={() =>
                toggleFeature('multimodal', multimodalEnabled)
              }
            />
          </div>

          <div className="flex items-center justify-between">
            <span className="text-sm font-medium">Movement</span>
            <Switch
              checked={movementEnabled}
              onCheckedChange={() =>
                toggleFeature('movement', movementEnabled)
              }
            />
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
