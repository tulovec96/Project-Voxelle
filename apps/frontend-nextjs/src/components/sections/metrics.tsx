'use client'

import { useStore } from '@/lib/store'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { BarChart3, Zap, Brain, Radio } from 'lucide-react'

export function MetricsSection() {
  const { metrics, serviceStatus } = useStore()

  if (!metrics) return null

  return (
    <div className="space-y-4">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <BarChart3 className="h-5 w-5" />
            System Metrics
          </CardTitle>
          <CardDescription>Real-time performance monitoring</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">CPU</p>
              <p className="text-2xl font-bold">{metrics.cpu.toFixed(1)}%</p>
            </div>
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">Memory</p>
              <p className="text-2xl font-bold">
                {(metrics.memory / 1024).toFixed(1)}MB
              </p>
            </div>
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">Latency</p>
              <p className="text-2xl font-bold">{metrics.latency}ms</p>
            </div>
            <div className="space-y-2">
              <p className="text-sm text-muted-foreground">Requests/s</p>
              <p className="text-2xl font-bold">{metrics.requestsPerSecond}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {serviceStatus.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Service Status</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {serviceStatus.map((service) => (
                <div
                  key={service.name}
                  className="flex items-center justify-between rounded-lg bg-secondary p-3"
                >
                  <span className="font-medium">{service.name}</span>
                  <div
                    className={`h-2 w-2 rounded-full ${
                      service.status === 'running'
                        ? 'bg-green-500'
                        : 'bg-red-500'
                    }`}
                  />
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
