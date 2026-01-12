'use client'

import { useEffect } from 'react'
import { useStore } from '@/lib/store'
import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { CurrentMessageSection } from '@/components/sections/current-message'
import { NextMessageSection } from '@/components/sections/next-message'
import { TwitchSection } from '@/components/sections/twitch'
import { DiscordSection } from '@/components/sections/discord'
import { VTSSection } from '@/components/sections/vts'
import { MetricsSection } from '@/components/sections/metrics'
import { ControlsSection } from '@/components/sections/controls'

export default function DashboardPage() {
  const { initializeSocket } = useStore()

  useEffect(() => {
    initializeSocket()
  }, [initializeSocket])

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Main Controls */}
        <ControlsSection />

        {/* Current and Next Message */}
        <div className="grid gap-8 md:grid-cols-2">
          <CurrentMessageSection />
          <NextMessageSection />
        </div>

        {/* Integration Status */}
        <div className="grid gap-8 md:grid-cols-3">
          <TwitchSection />
          <DiscordSection />
          <VTSSection />
        </div>

        {/* Metrics and Status */}
        <MetricsSection />
      </div>
    </DashboardLayout>
  )
}
