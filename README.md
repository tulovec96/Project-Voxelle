# Project J.A.I.son - Unified Edition

<p align="center">
  <strong>A fully customizable AI companion framework with integrated Discord, Twitch, and VTube Studio support</strong>
</p>

<p align="center">
  <img alt="Project JAIson badge" src="https://img.shields.io/badge/Project-JAIson-blue">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.12+-3776ab?logo=python">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-green">
  <img alt="Platform" src="https://img.shields.io/badge/Platform-Windows%20|%20Linux%20|%20macOS-lightgrey">
</p>

<p align="center">
  <a href="#about">About</a> •
  <a href="#features">Features</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#installation">Installation</a> •
  <a href="#applications">Applications</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#usage">Usage</a> •
  <a href="#development">Development</a> •
  <a href="#troubleshooting">Troubleshooting</a> •
  <a href="#community">Community</a>
</p>

---

## About

**Project J.A.I.son** is a unified framework for building AI companion applications. This distribution includes the core server and all official integrations in a single, production-ready package. Use it for streaming, content creation, or personal projects—run fully locally with no cloud dependencies required.

> **Note:** This software uses libraries from the FFmpeg project under the LGPLv2.1

## Features

### Core Capabilities
- 🤖 **Real-time AI Personality** - Promptable AI with text and speech input
- 🔊 **Voice Interaction** - Full audio processing with customizable TTS/STT
- 🌐 **REST API & WebSocket** - Build custom applications on top of the core server
- 🔌 **Model Context Protocol (MCP)** - Extend functionality with MCP support
- 💻 **Fully Local** - No cloud dependencies—run everything on your hardware

### Integrated Applications
- 💬 **Discord Integration** - Chat in text channels and participate in voice calls
- 📺 **Twitch Integration** - Monitor live chat and real-time events
- 🎭 **VTube Studio Integration** - Animate a VTuber model with emotion reactions
- 🎨 **Web UI** - Professional SvelteKit-based web interface

## Quick Start

### Minimum Requirements
- **Python 3.12+**
- **FFmpeg** (for audio processing)
- **Virtual environment** (venv or conda)
- **Disk space**: ~2-3 GB for models and dependencies

### 5-Minute Setup

```bash
# 1. Clone/navigate to the project
cd jaison-unified

# 2. Create virtual environment
python -m venv venv

# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run installation validation
python install.py

# 5. Copy and configure
cp config.yaml.template config.yaml
# Edit config.yaml with your settings

# 6. Start the core server
python src/main.py
```

The core server will be available at `http://localhost:7272`

## Installation

### Prerequisites

#### System Requirements
- **Python 3.12+** with pip
- **FFmpeg** (required for audio processing)
- **4GB+ RAM** (8GB recommended with models)
- **GPU** (optional but recommended for faster inference)

#### Platform-Specific Setup

<details open>
<summary><b>Windows</b></summary>

1. **Enable Developer Mode** (for symbolic links):
   - Settings → System → Developer settings → Enable Developer Mode

2. **Install FFmpeg:**
   - Download [`ffmpeg-git-essentials.7z`](https://www.gyan.dev/ffmpeg/builds/)
   - Extract and copy all files from `bin/` to the project root

3. **Install CUDA** (optional, for GPU acceleration):
   - [NVIDIA CUDA Toolkit 12.8](https://developer.nvidia.com/cuda-toolkit)
   - [NVIDIA cuDNN](https://developer.nvidia.com/cudnn)

</details>

<details>
<summary><b>macOS</b></summary>

```bash
# Install via Homebrew
brew install ffmpeg

# For GPU support (Apple Silicon):
# PyTorch will automatically use Metal Performance Shaders
```

</details>

<details>
<summary><b>Linux (Ubuntu/Debian)</b></summary>

```bash
sudo apt update
sudo apt install ffmpeg python3.12 python3.12-venv
```

</details>

### Installation Methods

**Method 1: Pip Install (Recommended)**
```bash
pip install -e .
```

**Method 2: From Requirements**
```bash
pip install -r requirements.txt
pip install --no-deps -r requirements.no_deps.txt
```

**Method 3: Python Setup**
```bash
python setup.py install
```

### Post-Installation Setup

```bash
# Download language models
python -m spacy download en_core_web_sm

# Download NLTK data
python install.py

# Optional: Download UniDic for better Japanese support
python -m unidic download
```

## Applications

All applications are located in the `apps/` directory and can run independently once the core server is active.

### Discord Bot

Enable your AI to chat in Discord servers and voice channels.

```bash
# Setup
cd apps/discord
cp .env-template .env
# Edit .env with your Discord bot token

# Run
python src/main.py
```

**Configuration:** `apps/discord/config.yaml`
- JAIson API endpoints
- Audio codec settings
- Voice activity detection

### Twitch Integration

Monitor live chat and events, with the AI responding based on configured filters.

```bash
# First-time setup
cd apps/twitch
python src/auth.py  # Authenticate with Twitch

# Run
python src/main.py
```

**Configuration:** `apps/twitch/config.yaml`
- Chat filtering (ALL, KEYWORD, HIGHLIGHT, BITS, DISABLE)
- Summary intervals
- Event types to monitor

### VTube Studio Integration

Animate a VTuber character with emotion reactions and hotkey responses.

```bash
cd apps/vts
# Ensure VTube Studio is running with Plugins API enabled
python src/main.py
```

**Configuration:** `apps/vts/config.yaml`
- VTube Studio WebSocket URL
- Hotkey mappings
- Emotion reactions

### Web UI

Professional dashboard for monitoring and controlling all services.

```bash
cd apps/frontend
npm install
npm run dev
```

Accessible at `http://localhost:5173` (default Vite port)

## Configuration

### Core Configuration

Edit `config.yaml` to customize:

```yaml
# AI Model Settings
model:
  type: "llama"
  name: "default"
  
# API Configuration
server:
  host: "localhost"
  port: 7272
  
# Voice Settings
audio:
  sample_rate: 16000
  channels: 1
  
# Prompts and Characters
prompts:
  character: "prompts/characters/default.txt"
  scene: "prompts/scenes/default.txt"
  instructions: "prompts/instructions/default.txt"
```

See `configs/example.yaml` for all available options.

### Environment Variables

Create `.env` in the project root for sensitive data:

```env
# OpenAI/Groq API
OPENAI_API_KEY=sk-...

# Discord
DISCORD_TOKEN=YOUR_TOKEN_HERE

# Twitch
TWITCH_CLIENT_ID=YOUR_CLIENT_ID
TWITCH_CLIENT_SECRET=YOUR_SECRET

# Other Services
CUSTOM_API_KEY=...
```

### API Configuration

For free T2T integration, use OpenAI API format with [Groq](https://console.groq.com/):

```yaml
text_to_text:
  type: "openai"
  model: "mixtral-8x7b-32768"
  api_key: "${GROQ_API_KEY}"
  base_url: "https://api.groq.com/openai/v1"
```

See [api.yaml](api.yaml) for complete REST API specifications.

## Usage

### Starting the Core Server

```bash
# Basic startup
python src/main.py

# With specific config
python src/main.py --config=example

# Help and options
python src/main.py --help
```

### Managing All Services

Use the included manager for coordinated startup:

```bash
# Start core server
python manager.py core

# In separate terminals:
python manager.py discord
python manager.py twitch
python manager.py vts
```

### API Endpoints

**REST API:** `http://localhost:7272/api/`
**WebSocket:** `ws://localhost:7272/ws`

### CLI Tools

After installing with `pip install -e .`:

```bash
# Start JAIson
jaison

# Start with manager
jaison-manager core

# Run installer
jaison-install
```

## Development

### Project Structure

```
jaison-unified/
├── src/                      # Core JAIson server
│   ├── main.py              # Entry point
│   ├── utils/               # Helper utilities
│   ├── operations/          # AI operations (STT, TTS, T2T, etc.)
│   └── server/              # API and WebSocket server
├── apps/
│   ├── discord/             # Discord bot application
│   ├── twitch/              # Twitch integration
│   ├── vts/                 # VTube Studio animation
│   └── frontend/            # SvelteKit web UI
├── configs/                 # Configuration templates
├── prompts/                 # Character definitions and instructions
├── models/                  # Model storage
├── docs/                    # Documentation
├── setup.py                 # Installation script
├── install.py               # Post-install validation
└── requirements.txt         # Python dependencies
```

### Building Custom Applications

See the [Developer Guide](DEVELOPER.md) for:
- REST API specifications [api.yaml](api.yaml)
- Creating custom integrations
- Configuration deep-dive
- Contributing guidelines [CONTRIBUTING.md](CONTRIBUTING.md)

### Development Setup

```bash
pip install -r requirements.txt
pip install -e .[dev]  # Includes dev dependencies

# Run tests
pytest

# Format code
black src/ apps/

# Lint
flake8 src/ apps/
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 7272
netstat -ano | findstr :7272  # Windows
lsof -i :7272                 # macOS/Linux

# Change port in config.yaml
```

### Discord Bot Won't Connect

- ✅ Verify token in `apps/discord/.env`
- ✅ Check bot has `Send Messages` and `Connect` permissions
- ✅ Ensure bot is invited to your server: `https://discord.com/oauth2/authorize?client_id=YOUR_ID&scope=bot&permissions=8`
- ✅ Check firewall/network settings

### Twitch Authentication Failed

```bash
# Re-authenticate
cd apps/twitch
python src/auth.py

# Verify credentials in .env and config.yaml
```

### VTube Studio Not Responding

- ✅ Ensure VTube Studio is running
- ✅ Enable Plugins API: Settings → General Settings & External Connections
- ✅ Verify WebSocket URL in `apps/vts/config.yaml` matches VTS settings
- ✅ Check firewall allows WebSocket connections

### FFmpeg Not Found

```bash
# Verify installation
ffmpeg -version

# Add to PATH (Windows)
# Copy ffmpeg.exe to project root or system PATH directory
```

### CUDA/GPU Issues

For PyTorch GPU support:

```bash
# Reinstall PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

For issues with duplicate `libiomp5md.dll` on Windows:
1. Locate your conda environment: `conda info`
2. Find `libiomp5md.dll` under `torch` package
3. Delete the duplicate in the torch directory

## Community

### Get Involved

- **Discord Community:** [Join the Discord server](https://discord.gg/Z8yyEzHsYM)
- **YouTube Channel:** [@LimitCantCode](https://www.youtube.com/@LimitCantCode)
- **Twitch Channel:** [atmylimit_](https://www.twitch.tv/atmylimit_)

### Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

<a href="https://github.com/limitcantcode/jaison-core/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=limitcantcode/jaison-core" alt="Contributors" />
</a>

## License

This project is licensed under the [MIT License](LICENSE).

**Third-party libraries:** This software uses libraries from the FFmpeg project under the LGPLv2.1.

---

<p align="center">
  Made with ❤️ by the Project J.A.I.son community
</p>
