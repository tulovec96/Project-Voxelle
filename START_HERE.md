# 🎉 Welcome to JAIson Unified!

This is a **merged and unified distribution** of Project J.A.I.son - a fully customizable AI companion system with integrated support for Discord, Twitch, and VTube Studio.

## 📍 You are here

This directory contains everything you need to run the complete JAIson system. It includes:
- **Core AI Server** - The brains of the operation
- **Discord Bot** - Chat and voice in Discord servers
- **Twitch Integration** - Monitor chat and react to events
- **VTube Studio Plugin** - Animate a VTuber with emotions

## 🚀 Quick Start (3 Steps)

### 1. Read the Documentation Index
```bash
# Open this file first - it explains everything
cat INDEX.md
```

### 2. Follow the Setup Guide
```bash
# Step-by-step instructions for your OS
cat QUICKSTART.md
```

### 3. Run It!
```bash
# Create environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install everything
pip install -r requirements-all.txt

# Start the core server
python manager.py core
```

## 📚 Documentation Map

| File | Purpose | Read Time |
|------|---------|-----------|
| **[INDEX.md](INDEX.md)** | 📖 Documentation index - START HERE | 5 min |
| **[QUICKSTART.md](QUICKSTART.md)** | 🚀 Setup guide for all platforms | 10 min |
| **[README-UNIFIED.md](README-UNIFIED.md)** | 📋 Complete system overview | 15 min |
| **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** | 🏗️ Architecture & how it works | 15 min |
| **[MERGE_SUMMARY.md](MERGE_SUMMARY.md)** | 🔄 What changed in the merge | 10 min |
| **[config.yaml.template](config.yaml.template)** | ⚙️ Configuration template | Reference |

## 🎯 What's Inside

### Core Components
- **`src/`** - JAIson core server (AI engine, APIs, models)
- **`apps/discord/`** - Discord bot integration
- **`apps/twitch/`** - Twitch chat & alerts monitoring  
- **`apps/vts/`** - VTube Studio animation plugin

### Resources
- **`prompts/`** - AI personality definitions
- **`models/`** - Storage for AI models (RVC, TTS, LLMs)
- **`configs/`** - Configuration templates
- **`assets/`** - Images and resources

### Tools
- **`manager.py`** - Start/stop the system components
- **`requirements-all.txt`** - All Python dependencies
- **`config.yaml.template`** - Configuration template

## ⚡ Key Features

✨ **AI Companion**
- Customizable personality with text & speech input
- Multiple AI model support (GPT, local models, etc.)
- Real-time conversation with context awareness

🎤 **Discord Integration**
- Text chat in channels
- Voice chat in call channels
- Slash commands for control

📺 **Twitch Integration**  
- Monitor live chat in real-time
- React to follows, subs, raids, donations
- Customizable chat filtering

🎭 **VTube Studio**
- Animate a VTuber model
- Emotion-based expressions
- Real-time lipsync

🔌 **Extensible**
- REST API for custom integrations
- WebSocket for real-time apps
- MCP (Model Context Protocol) support

## 🛠️ System Requirements

- **Python**: 3.12+
- **RAM**: 4+ GB (8+ recommended for faster AI)
- **Storage**: 5+ GB (for models)
- **Network**: Internet connection
- **Optional**: GPU for faster AI processing

## 🎓 Learning Path

**New to JAIson?**
1. Open [INDEX.md](INDEX.md) - understand the structure
2. Follow [QUICKSTART.md](QUICKSTART.md) - set it up
3. Read [README-UNIFIED.md](README-UNIFIED.md) - learn features
4. Check [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - understand architecture

**Developer?**
1. Read [DEVELOPER.md](DEVELOPER.md) - development guide
2. Check [api.yaml](api.yaml) - API specification
3. Study [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) - how components work

## 📞 Community & Support

**Questions?**
- 📖 Read the documentation first
- 💬 [Join our Discord](https://discord.gg/Z8yyEzHsYM)
- 🐛 [Report issues on GitHub](https://github.com/limitcantcode/jaison-core)

**Having Problems?**
- Check [QUICKSTART.md](QUICKSTART.md#-troubleshooting) troubleshooting section
- See [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md#troubleshooting-inter-app-communication)

## 📦 What's Included

This unified distribution merges:
- ✅ jaison-core-2.2.1 (core server)
- ✅ app-jaison-discord-lcc-main (Discord bot)
- ✅ app-jaison-twitch-lcc-main (Twitch integration)
- ✅ app-jaison-vts-hotkeys-lcc-main (VTube Studio)

All original code and functionality is preserved!

## 🔐 License

Each component maintains its original MIT License. 
FFmpeg usage is under LGPLv2.1.

See individual `LICENSE` files in component directories for details.

## 🎯 Next Steps

### Immediate
```bash
# 1. Read the index
cat INDEX.md

# 2. Follow quick start
cat QUICKSTART.md

# 3. Set up your environment
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements-all.txt
```

### Configuration
```bash
# 1. Copy config template
cp config.yaml.template config.yaml

# 2. Edit with your API keys
code config.yaml  # or your favorite editor

# 3. Configure each app (Discord, Twitch, VTS)
# See QUICKSTART.md for detailed instructions
```

### Testing
```bash
# 1. Start core server
python manager.py core

# 2. In another terminal, test an app
python manager.py discord

# 3. Check system status anytime
python manager.py status
```

## 🚀 You're Ready!

Everything you need is here. Start with [INDEX.md](INDEX.md) and follow the guides.

**Need help?** See the community links above.

---

**This is JAIson Unified Edition - Created by merging official JAIson projects for your convenience.**

*Last updated: January 2026*
*Project JAIson: https://github.com/limitcantcode/jaison-core*
