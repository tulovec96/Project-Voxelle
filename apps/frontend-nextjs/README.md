# Voxelle Frontend - Next.js Migration

This is the new **Next.js 15** frontend for Voxelle, migrated from SvelteKit with enhanced design and functionality.

## 🚀 Features

### ✅ All Functionality Preserved from SvelteKit
- **Real-time Socket.IO** communication with Python backend
- **Dashboard** with live system metrics and service status
- **Discord Integration** - Bot status and controls
- **Twitch Integration** - Chat and stream stats
- **VTube Studio Integration** - Avatar control
- **Memory Management** - Manage AI memory and context
- **Moderation Controls** - Manage user interactions
- **Analytics** - Real-time metrics and performance monitoring

### ✨ New Improvements with Next.js
- **Modern UI Components** - Tailwind CSS + shadcn/ui
- **Better Performance** - Server-side rendering, optimized builds
- **Type Safety** - Full TypeScript support
- **Dark Mode** - Built-in theme switching
- **Responsive Design** - Mobile-first approach
- **State Management** - Zustand for global state
- **Data Fetching** - React Query integration ready
- **Production Ready** - Optimized for deployment

## 📋 Requirements

- Node.js 18+
- npm or yarn
- Python backend running (for Socket.IO communication)

## 🔧 Installation

### 1. Install Dependencies

```bash
cd apps/frontend-nextjs
npm install
# or
yarn install
```

### 2. Environment Setup

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

### 3. Run Development Server

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## 📁 Project Structure

```
src/
├── app/                      # Next.js App Router
│   ├── page.tsx             # Dashboard home page
│   ├── integrations/        # Integration management
│   ├── settings/            # Settings page
│   ├── layout.tsx           # Root layout
│   ├── providers.tsx        # Providers (Zustand, Query, Themes)
│   └── globals.css          # Global styles
├── components/
│   ├── ui/                  # Reusable UI components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   ├── textarea.tsx
│   │   ├── progress.tsx
│   │   └── switch.tsx
│   ├── sections/            # Page sections
│   │   ├── current-message.tsx
│   │   ├── next-message.tsx
│   │   ├── twitch.tsx
│   │   ├── discord.tsx
│   │   ├── vts.tsx
│   │   ├── metrics.tsx
│   │   └── controls.tsx
│   └── layout/              # Layout components
│       └── dashboard-layout.tsx
└── lib/
    ├── store.ts             # Zustand state management
    └── utils.ts             # Utility functions
```

## 🔌 Socket.IO Integration

The frontend maintains full Socket.IO connectivity with the Python backend:

```typescript
// Automatic Socket.IO initialization
useEffect(() => {
  const { initializeSocket } = useStore()
  initializeSocket()
}, [])

// Real-time event listeners
socket.on('current_message', (data) => { ... })
socket.on('AI_thinking', (data) => { ... })
socket.on('metrics', (data) => { ... })
```

## 🎨 Styling

Uses **Tailwind CSS** with custom design system:

- **Dark mode**: Built-in with `next-themes`
- **Colors**: Customizable CSS variables
- **Components**: Pre-styled with shadcn/ui patterns
- **Responsive**: Mobile-first design

## 🧪 Building for Production

```bash
npm run build
npm run start
```

Or with Docker:

```bash
docker build -t voxelle-frontend .
docker run -p 3000:3000 voxelle-frontend
```

## 📦 Key Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Next.js | ^15.1.0 | React framework |
| React | ^19.0.0 | UI library |
| socket.io-client | ^4.7.2 | WebSocket communication |
| zustand | ^4.4.1 | State management |
| tailwindcss | ^3.4.1 | Styling |
| lucide-react | ^0.374.0 | Icons |
| next-themes | ^0.2.1 | Theme management |

## 🔄 Migration from SvelteKit

### What Changed
- **Framework**: SvelteKit → Next.js
- **Styling**: Tailwind (same) + shadcn/ui components
- **State**: Svelte stores → Zustand
- **Components**: Svelte components → React components

### What Stayed the Same
- **Backend Connection**: Socket.IO unchanged
- **Data Structure**: Same API contracts
- **Features**: All functionality preserved
- **Deployment**: Still containerizable

## 🚨 Troubleshooting

### Socket.IO Connection Issues

```typescript
// Check connection status
const { isConnected } = useStore()

// Manual reconnection
const { initializeSocket } = useStore()
initializeSocket('ws://custom-url:port')
```

### Dark Mode Not Working

Ensure `next-themes` provider is loaded:

```typescript
<ThemeProvider attribute="class" defaultTheme="dark" enableSystem>
  {children}
</ThemeProvider>
```

### TypeScript Errors

Run type checking:

```bash
npm run type-check
```

## 🤝 Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for contribution guidelines.

## 📝 Development Commands

```bash
# Development
npm run dev              # Start dev server
npm run build           # Build for production
npm run start           # Start production server
npm run type-check      # Check TypeScript types
npm run lint            # Run ESLint

# Building
npm run build           # Next.js build
npm run export          # Static export (if needed)
```

## 🔐 Environment Variables

Required `.env.local`:

```env
# Backend API connection
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
```

Optional:

```env
# Analytics (if using)
NEXT_PUBLIC_ANALYTICS_ID=your-id

# Environment
NEXT_PUBLIC_ENV=development
```

## 📚 Additional Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [shadcn/ui](https://ui.shadcn.com)
- [Socket.IO Client](https://socket.io/docs/v4/client-api/)
- [Zustand](https://github.com/pmndrs/zustand)

## ✅ Testing Status

### Functionality Verified
- ✅ Socket.IO connections working
- ✅ Real-time message updates
- ✅ Integration status display
- ✅ Metrics/analytics display
- ✅ Control features (toggles, buttons)
- ✅ Responsive design
- ✅ Dark mode switching

### Backend Compatibility
- ✅ Python backend communication
- ✅ Event emission/reception
- ✅ JSON data handling
- ✅ WebSocket protocols

## 🎯 Next Steps

1. **Run the development server** - `npm run dev`
2. **Connect your Python backend** - Ensure Socket.IO server is running
3. **Test integrations** - Verify Twitch, Discord, VTS connections
4. **Deploy** - Use Docker or your preferred hosting

## 📞 Support

For issues or questions:
1. Check [CONTRIBUTING.md](../../CONTRIBUTING.md)
2. Review [ADVANCED_DEVELOPMENT.md](../../ADVANCED_DEVELOPMENT.md)
3. Open a GitHub issue

---

**Status**: ✅ **Production Ready**

**Maintained by**: @tulovec96

**Last Updated**: January 2026
