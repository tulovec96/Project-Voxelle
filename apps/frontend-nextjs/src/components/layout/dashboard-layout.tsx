'use client'

import { ReactNode } from 'react'
import { useTheme } from 'next-themes'
import { useStore } from '@/lib/store'
import { Button } from '@/components/ui/button'
import { Moon, Sun } from 'lucide-react'
import Link from 'next/link'

export function DashboardLayout({ children }: { children: ReactNode }) {
  const { theme, setTheme } = useTheme()
  const { isConnected } = useStore()

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="flex h-16 items-center justify-between px-4 md:px-8">
          <div className="flex items-center gap-4">
            <Link href="/" className="flex items-center gap-2">
              <div className="h-8 w-8 rounded-lg bg-primary" />
              <span className="font-bold">Voxelle</span>
            </Link>
            <div className="hidden gap-6 md:flex">
              <Link href="/" className="text-sm hover:text-primary">
                Dashboard
              </Link>
              <Link href="/integrations" className="text-sm hover:text-primary">
                Integrations
              </Link>
              <Link href="/settings" className="text-sm hover:text-primary">
                Settings
              </Link>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div
                className={`h-2 w-2 rounded-full ${
                  isConnected ? 'bg-green-500' : 'bg-red-500'
                }`}
              />
              <span className="text-xs text-muted-foreground">
                {isConnected ? 'Connected' : 'Disconnected'}
              </span>
            </div>

            <Button
              variant="ghost"
              size="icon"
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            >
              {theme === 'dark' ? (
                <Sun className="h-5 w-5" />
              ) : (
                <Moon className="h-5 w-5" />
              )}
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 px-4 py-8 md:px-8">
        <div className="mx-auto max-w-7xl">
          {children}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t bg-background/95 py-4 text-center text-xs text-muted-foreground">
        <p>Voxelle © 2024. Powered by AI.</p>
      </footer>
    </div>
  )
}
