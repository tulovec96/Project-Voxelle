'use client'

import { DashboardLayout } from '@/components/layout/dashboard-layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Radio, Users, Eye, Zap } from 'lucide-react'

export default function IntegrationsPage() {
  return (
    <DashboardLayout>
      <div className="space-y-8">
        <div>
          <h1 className="text-3xl font-bold">Integrations</h1>
          <p className="text-muted-foreground">Manage your platform connections</p>
        </div>

        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
          {/* Twitch */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Radio className="h-5 w-5 text-purple-500" />
                Twitch
              </CardTitle>
              <CardDescription>Connect your Twitch account</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Input placeholder="Channel Name" />
              <Input placeholder="OAuth Token" type="password" />
              <Button className="w-full">Connect</Button>
            </CardContent>
          </Card>

          {/* Discord */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5 text-indigo-500" />
                Discord
              </CardTitle>
              <CardDescription>Connect your Discord bot</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Input placeholder="Bot Token" type="password" />
              <Input placeholder="Guild ID" />
              <Button className="w-full">Connect</Button>
            </CardContent>
          </Card>

          {/* VTube Studio */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Eye className="h-5 w-5 text-pink-500" />
                VTube Studio
              </CardTitle>
              <CardDescription>Connect to VTube Studio</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Input placeholder="API Port" defaultValue="8001" />
              <Input placeholder="Authentication Token" type="password" />
              <Button className="w-full">Connect</Button>
            </CardContent>
          </Card>
        </div>

        {/* Advanced Settings */}
        <Card>
          <CardHeader>
            <CardTitle>Advanced Settings</CardTitle>
            <CardDescription>Configure integration behaviors</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-4 md:grid-cols-2">
              <div className="space-y-2">
                <label className="text-sm font-medium">Max Chat Messages</label>
                <Input type="number" defaultValue="100" />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">Message Timeout (s)</label>
                <Input type="number" defaultValue="30" />
              </div>
            </div>
            <Button>Save Settings</Button>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}
