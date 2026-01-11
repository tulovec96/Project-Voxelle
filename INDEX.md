📖 **JAIson Unified - Documentation Index**

Welcome to the unified JAIson system! Here's where to find what you need.

---

## 🚀 Getting Started

**New to JAIson?** Start here:
1. **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
2. **[README-UNIFIED.md](README-UNIFIED.md)** - Full system overview
3. **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - How everything works together

---

## 📚 Documentation Files

### Essential Reading
- **[QUICKSTART.md](QUICKSTART.md)** (8KB)
  - Setup instructions for Windows, macOS, Linux
  - How to configure each application
  - Common troubleshooting

- **[README-UNIFIED.md](README-UNIFIED.md)** (6KB)
  - System features and capabilities
  - Installation instructions
  - Configuration options
  - Customization guide

- **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** (11KB)
  - System architecture diagrams
  - How applications communicate
  - Data flow examples
  - Advanced configuration

- **[MERGE_SUMMARY.md](MERGE_SUMMARY.md)** (9KB)
  - What was changed in the merge
  - Files preserved and added
  - Migration guide from old projects
  - File inventory

### Original Documentation
- **[README.md](README.md)** - Original JAIson core README
- **[api.yaml](api.yaml)** - REST API specification
- **[DEVELOPER.md](DEVELOPER.md)** - Developer guide
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute

---

## ⚙️ Configuration Files

### Templates & Examples
- **[config.yaml.template](config.yaml.template)** (5KB)
  - Complete configuration template
  - All available options documented
  - Includes app-specific settings

### Per-Application Configs
- **[apps/discord/config.yaml](apps/discord/config.yaml)** - Discord bot settings
- **[apps/twitch/config.yaml](apps/twitch/config.yaml)** - Twitch integration settings
- **[apps/vts/config.yaml](apps/vts/config.yaml)** - VTube Studio settings

### Environment Files
- **[apps/discord/.env-template](apps/discord/.env-template)** - Discord credentials template
- **[apps/twitch/.env-template](apps/twitch/.env-template)** - Twitch credentials template

---

## 🛠️ Tools & Scripts

### System Manager
- **[manager.py](manager.py)** (5KB)
  - Start/stop applications
  - Check system status
  - View logs
  - Usage: `python manager.py --help`

### Installation & Setup
- **[requirements-all.txt](requirements-all.txt)** (4KB)
  - All Python dependencies
  - Usage: `pip install -r requirements-all.txt`

- **[install.py](install.py)** - Automated installer (if available)

---

## 📁 Directory Guide

### Core System
```
src/                     Core JAIson server
├── main.py             Entry point
├── utils/              Utilities
│   ├── jaison.py      Main class
│   ├── config.py      Config management
│   └── operations/    AI operations (TTS, STT, etc.)
└── ...
```

### Applications
```
apps/                   All integrations
├── discord/           Discord bot
│   ├── src/
│   ├── config.yaml
│   └── README.md
├── twitch/            Twitch integration
│   ├── src/
│   ├── config.yaml
│   └── README.md
└── vts/               VTube Studio
    ├── src/
    ├── config.yaml
    └── vts_hotkeys/
```

### Data & Models
```
configs/               Configuration templates
prompts/              AI personalities
├── characters/       Character definitions
├── instructions/     System instructions
└── scenes/          Scene contexts
models/              Stored AI models
├── rvc/            Voice conversion
├── melotts/        Text-to-speech
├── kobold/         Language models
└── mcp/            MCP models
```

---

## 🎯 Quick Command Reference

### Start Applications
```bash
# Check status
python manager.py status

# Start core server
python manager.py core

# Start Discord bot
python manager.py discord

# Start Twitch integration
python manager.py twitch

# Start VTube Studio integration
python manager.py vts
```

### Setup
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install all dependencies
pip install -r requirements-all.txt

# Check what's installed
pip list

# Update outdated packages
pip install --upgrade -r requirements-all.txt
```

### Configuration
```bash
# Copy template to active config
cp config.yaml.template config.yaml

# Edit with your favorite editor
nano config.yaml        # Linux/macOS
code config.yaml        # VS Code
```

---

## 🔍 Finding What You Need

### "I want to..."

**Setup the system**
→ [QUICKSTART.md](QUICKSTART.md)

**Understand how it works**
→ [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)

**Configure Discord bot**
→ [QUICKSTART.md](QUICKSTART.md) → Discord section

**Configure Twitch integration**
→ [QUICKSTART.md](QUICKSTART.md) → Twitch section

**Setup VTube Studio animation**
→ [QUICKSTART.md](QUICKSTART.md) → VTube Studio section

**Write custom commands**
→ [DEVELOPER.md](DEVELOPER.md) + [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)

**Use the REST API**
→ [api.yaml](api.yaml) + [README-UNIFIED.md](README-UNIFIED.md)

**Report a bug**
→ Original repo on GitHub

**Get community help**
→ Discord: https://discord.gg/Z8yyEzHsYM

**See what changed in the merge**
→ [MERGE_SUMMARY.md](MERGE_SUMMARY.md)

---

## 📊 File Statistics

| Category | File | Size | Purpose |
|----------|------|------|---------|
| Setup | QUICKSTART.md | 8 KB | Quick setup guide |
| Documentation | README-UNIFIED.md | 6 KB | System overview |
| Architecture | INTEGRATION_GUIDE.md | 11 KB | Technical details |
| Merge Info | MERGE_SUMMARY.md | 9 KB | What changed |
| Config | config.yaml.template | 5 KB | Configuration template |
| Config | requirements-all.txt | 4 KB | Dependencies |
| Tools | manager.py | 5 KB | System manager |
| Docs | README.md | 163 KB | Original JAIson README |
| API | api.yaml | - | API specification |

---

## 🆘 Need Help?

### Documentation Issues
1. Check [QUICKSTART.md](QUICKSTART.md) troubleshooting section
2. Read [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) for architecture
3. See [README-UNIFIED.md](README-UNIFIED.md) for detailed explanations

### Installation Issues
```bash
# Verify installation
python -c "import torch; print(torch.__version__)"

# Reinstall dependencies
pip install --force-reinstall -r requirements-all.txt
```

### Application Issues
- **Discord**: See [apps/discord/README.md](apps/discord/README.md)
- **Twitch**: See [apps/twitch/README.md](apps/twitch/README.md)
- **VTube Studio**: See [apps/vts/README.md](apps/vts/README.md)

### Community Help
- **Discord Server**: https://discord.gg/Z8yyEzHsYM
- **GitHub Issues**: 
  - Core: https://github.com/limitcantcode/jaison-core/issues
  - Discord: https://github.com/limitcantcode/app-jaison-discord-lcc/issues
  - Twitch: https://github.com/limitcantcode/app-jaison-twitch-lcc/issues
  - VTS: https://github.com/limitcantcode/app-jaison-vts-hotkeys-lcc/issues

---

## 📋 Checklist: First Time Setup

- [ ] Read QUICKSTART.md
- [ ] Create Python virtual environment
- [ ] Install dependencies
- [ ] Copy config.yaml.template to config.yaml
- [ ] Edit config.yaml with your settings
- [ ] Test core server with `python manager.py core`
- [ ] Setup Discord (.env and config)
- [ ] Setup Twitch (.env and config)
- [ ] Setup VTube Studio (config and hotkeys)
- [ ] Test each application individually
- [ ] Join community Discord for updates

---

## 🎓 Learning Path

1. **Beginner** → QUICKSTART.md → Get basic system running
2. **Intermediate** → README-UNIFIED.md → Understand features
3. **Advanced** → INTEGRATION_GUIDE.md → Understand architecture
4. **Developer** → DEVELOPER.md + api.yaml → Build extensions

---

**Last Updated**: January 2026
**Version**: JAIson Unified v1.0
**Status**: ✅ Ready to use

For the latest updates, visit: https://github.com/limitcantcode/jaison-core
