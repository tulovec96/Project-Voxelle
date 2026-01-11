# J.A.I.son Frontend - Modern Control Panel

![screenshot.png](images/main.png)

Enhanced web dashboard for monitoring and controlling your J.A.I.son AI companion framework.

This frontend is built with **SvelteKit**, **Tailwind CSS**, and **Svelte**, using **Socket.IO** for real-time communication with the Python backend.

## 🎯 Features

### 📊 Dashboard
- **Real-time Service Status** - Monitor all services (Core, Discord, Twitch, VTS) with uptime tracking
- **System Metrics** - Live CPU, memory, and latency monitoring
- **Performance Graphs** - Visual resource usage with history charts
- **Service Controls** - Start/stop services directly from the dashboard

### 📈 Metrics Panel
- **CPU & Memory Usage** - Real-time tracking with 14-second rolling charts
- **API Latency** - 95th percentile latency monitoring
- **Request Throughput** - Requests/sec and error tracking
- **Performance History** - Visual bar charts for trend analysis

### 🔍 Logs Viewer
- **Real-time Logging** - Stream from all services (Core, Discord, Twitch, VTS)
- **Advanced Filtering** - Filter by log level and service
- **Full-text Search** - Find messages across logs
- **Export** - Download logs as CSV for external analysis
- **Clear** - Reset log history with one click

### ⚙️ Configuration Manager
- **View Configuration** - Read current YAML config
- **Edit Configuration** - Inline editor with JSON/YAML support
- **Copy to Clipboard** - Share configs easily
- **Documentation** - Integrated help for each section

### 🧪 API Playground
- **Interactive HTTP Client** - Test API endpoints in browser
- **Request Builder** - Visual method and body builder
- **Quick Presets** - Pre-configured example requests
- **Response Viewer** - Formatted JSON response display
- **Copy Response** - Export API responses

### 🎨 UI/UX Enhancements
- **Dark Mode** - Default dark theme with toggle
- **Responsive Design** - Desktop, tablet, mobile support
- **Persistent Sidebar** - Desktop navigation panel
- **Connection Status** - Real-time server connection indicator
- **Smooth Transitions** - Animated UI interactions

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- npm or pnpm

### Installation

```bash
cd apps/frontend
npm install
```

### Development

```bash
npm run dev
```

Visit http://localhost:5173 in your browser.

### Build for Production

```bash
npm run build
npm run preview
```

## 📁 Project Structure

```
src/
├── routes/
│   ├── +layout.svelte           # Main layout with sidebar nav
│   ├── +page.svelte             # Dashboard (home)
│   ├── metrics/
│   │   └── +page.svelte         # Performance metrics
│   ├── logs/
│   │   └── +page.svelte         # Log viewer with filtering
│   ├── config/
│   │   └── +page.svelte         # Configuration editor
│   ├── api/
│   │   └── +page.svelte         # API playground
│   ├── lobotomy/
│   ├── moderation/
│   ├── memory/
│   ├── vtube/
│   └── socketio.ts              # WebSocket client
├── lib/
│   ├── stores.ts                # Svelte stores
│   ├── components/              # UI components
│   └── utils.ts                 # Helper functions
└── app.pcss                     # Global styles
```

## 🔌 Backend Integration

The frontend connects to the core J.A.I.son server via:

- **REST API**: `http://localhost:7272/api/*`
- **WebSocket**: `ws://localhost:7272/ws`

### Environment Configuration

Create a `.env.local` file in `apps/frontend`:

```env
VITE_API_URL=http://localhost:7272
VITE_WS_URL=ws://localhost:7272
VITE_DEBUG=false
```

## 🎨 Tech Stack

| Tool | Purpose |
|------|---------|
| Svelte | Reactive UI framework |
| SvelteKit | Full-stack web framework |
| TypeScript | Type-safe development |
| Tailwind CSS | Utility-first styling |
| Lucide | Icon library |
| Socket.IO | Real-time WebSocket |
| Bits UI | Headless components |

## 📦 Key Dependencies

```json
{
  "svelte": "^4.2.7",
  "@sveltejs/kit": "^2.0.0",
  "tailwindcss": "^3.3.6",
  "socket.io-client": "^4.7.4",
  "lucide-svelte": "^0.343.0",
  "bits-ui": "^0.21.9",
  "mode-watcher": "^0.2.2"
}
```

## 📖 Development Guide

### Creating New Pages

1. Create a folder under `src/routes/your-page/`
2. Add `+page.svelte` with your component
3. Add link to `src/routes/+layout.svelte` sidebar

Example page:

```svelte
<script>
  import { Button } from "$lib/components/ui/button";
</script>

<div class="space-y-6">
  <h1 class="text-4xl font-bold">My Page</h1>
  <p>Hello world</p>
</div>
```

### Using Components

```svelte
<script>
  import { Button } from "$lib/components/ui/button";
  import { Input } from "$lib/components/ui/input";
  import { Select } from "$lib/components/ui/select";
</script>

<Button on:click={() => console.log('clicked')}>Click Me</Button>
<Input placeholder="Enter text..." />
```

### WebSocket Events

Listen to server events:

```svelte
<script>
  import { socket } from "./socketio";

  socket.on("service_status", (data) => {
    console.log("Service updated:", data);
  });

  socket.emit("get_metrics", {}, (response) => {
    console.log("Metrics:", response);
  });
</script>
```

## 🔐 Security Considerations

- Configurations and secrets are NOT persisted in browser storage
- All connections should use HTTPS in production
- Socket.IO is protected against CSRF attacks
- Validate all user inputs before sending to backend

## 📱 Responsive Design

| Breakpoint | Size | Layout |
|------------|------|--------|
| Mobile | < 768px | Hidden sidebar, full-width content |
| Tablet | 768px - 1024px | Flexible layout |
| Desktop | > 1024px | Sidebar + content |

## 🎨 Customization

### Theme Colors

Edit `tailwind.config.js`:

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        success: '#10b981',
      },
    },
  },
};
```

### Component Styling

Modify component files in `src/lib/components/` using Tailwind classes.

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| WebSocket won't connect | Verify core server is running on port 7272 |
| Metrics not updating | Check browser console for errors, verify WebSocket |
| Styles not loading | Run `npm run build`, check Tailwind config |
| CORS errors | Ensure API URL matches server domain |

## 📚 Resources

- [SvelteKit Documentation](https://kit.svelte.dev/)
- [Svelte Documentation](https://svelte.dev/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Socket.IO Client](https://socket.io/docs/v4/client-api/)
- [Lucide Icons](https://lucide.dev/)

## 📸 Gallery

See images in `images/` directory for screenshots of:
- Main dashboard
- Metrics panel
- Lobotomy editor
- Moderation tools
- Memory viewer
- VTube Studio controls

## 📝 License

MIT License - Same as J.A.I.son core project

---

Built with ❤️ by the J.A.I.son community

