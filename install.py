#!/usr/bin/env python3
"""
JAIson Unified - Post-Installation Setup Script
Downloads required models and validates the installation

Usage:
    python install.py              # Full setup
    python install.py --check-only # Just verify
    python install.py --help       # Show options
"""

import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Tuple

def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_section(text: str):
    """Print a section header"""
    print(f"\n📌 {text}")
    print("-" * 60)

def run_command(cmd: List[str], description: str) -> Tuple[bool, str]:
    """Run a command and return success status and output"""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return False, f"Timeout running: {' '.join(cmd)}"
    except Exception as e:
        return False, str(e)

def install_nltk_data():
    """Download required NLTK data"""
    print_section("Downloading NLTK Language Data")
    
    nltk_items = [
        'averaged_perceptron_tagger_eng',
        'punkt',
        'wordnet',
        'averaged_perceptron_tagger',
        'brown',
        'universal_tagset',
    ]
    
    try:
        import nltk
        
        success_count = 0
        for item in nltk_items:
            try:
                print(f"  ⏳ Downloading {item}...", end=" ", flush=True)
                nltk.download(item, quiet=True)
                print("✅")
                success_count += 1
            except Exception as e:
                print(f"⚠️  Skipped ({type(e).__name__})")
        
        print(f"\n✅ NLTK: {success_count}/{len(nltk_items)} items installed")
        return True
    except ImportError:
        print("❌ NLTK not installed - run: pip install nltk")
        return False

def check_python_packages():
    """Check if critical Python packages are installed"""
    print_section("Checking Python Packages")
    
    packages = {
        "torch": "PyTorch",
        "transformers": "Hugging Face Transformers",
        "discord": "Discord.py",
        "fastapi": "FastAPI",
        "pydantic": "Pydantic",
        "websockets": "WebSockets",
    }
    
    installed = []
    missing = []
    
    for module, name in packages.items():
        try:
            mod = __import__(module)
            version = getattr(mod, "__version__", "unknown")
            print(f"  ✅ {name:<35} {version}")
            installed.append(module)
        except ImportError:
            print(f"  ❌ {name:<35} NOT INSTALLED")
            missing.append(module)
    
    print(f"\n✅ Installed: {len(installed)}/{len(packages)}")
    
    if missing:
        print(f"⚠️  Missing: {', '.join(missing)}")
        print(f"\nInstall missing packages with:")
        print(f"  pip install -r requirements.txt")
    
    return len(missing) == 0

def check_spacy_models():
    """Check and install Spacy language models"""
    print_section("Spacy Language Models")
    
    try:
        import spacy
        
        models = ["en_core_web_sm"]
        
        for model in models:
            try:
                spacy.load(model)
                print(f"  ✅ {model} already installed")
            except OSError:
                print(f"  ⏳ Downloading {model}...")
                try:
                    result = subprocess.run(
                        [sys.executable, "-m", "spacy", "download", model],
                        capture_output=True,
                        timeout=60
                    )
                    if result.returncode == 0:
                        print(f"  ✅ {model} installed")
                    else:
                        print(f"  ⚠️  {model} download failed")
                except Exception as e:
                    print(f"  ⚠️  {model} error: {e}")
        
        return True
    except ImportError:
        print("  ⚠️  Spacy not installed - install with: pip install spacy")
        return False

def check_directories():
    """Check if required directories exist"""
    print_section("Directory Structure")
    
    required_dirs = [
        "src",
        "apps/discord",
        "apps/twitch",
        "apps/vts",
        "apps/frontend",
        "prompts",
        "models",
        "configs",
        "logs",
        "output",
    ]
    
    base = Path(__file__).parent
    
    for dir_name in required_dirs:
        dir_path = base / dir_name
        if dir_path.exists():
            print(f"  ✅ {dir_name}")
        else:
            print(f"  ❌ {dir_name} MISSING")
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"      └─ Created")
            except Exception as e:
                print(f"      └─ Failed to create: {e}")

def check_config_files():
    """Check if configuration files are present"""
    print_section("Configuration Files")
    
    base = Path(__file__).parent
    
    configs = [
        ("config.yaml", "Main configuration"),
        ("config.yaml.template", "Configuration template"),
        ("requirements.txt", "Python dependencies"),
        ("manager.py", "System manager"),
        ("install.py", "This installer"),
        ("apps/discord/config.yaml", "Discord config"),
        ("apps/twitch/config.yaml", "Twitch config"),
        ("apps/vts/config.yaml", "VTS config"),
        ("apps/frontend/package.json", "Frontend config"),
    ]
    
    found = 0
    for file_path, description in configs:
        full_path = base / file_path
        if full_path.exists():
            print(f"  ✅ {description:<25} ({file_path})")
            found += 1
        else:
            print(f"  ⚠️  {description:<25} ({file_path}) - MISSING")
    
    print(f"\n✅ Found: {found}/{len(configs)} config files")

def check_frontend():
    """Check Node.js frontend"""
    print_section("Frontend (Node.js)")
    
    base = Path(__file__).parent / "apps" / "frontend"
    
    if not base.exists():
        print("  ❌ Frontend directory not found")
        return False
    
    if (base / "package.json").exists():
        print("  ✅ package.json found")
        
        # Check if node_modules exists
        if (base / "node_modules").exists():
            print("  ✅ node_modules already installed")
        else:
            print("  ⚠️  node_modules not installed")
            print("      Run: cd apps/frontend && npm install")
    else:
        print("  ❌ package.json not found")
        return False
    
    return True

def main():
    """Main installation routine"""
    parser = argparse.ArgumentParser(
        description="JAIson Unified - Setup & Validation Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python install.py              # Full setup
  python install.py --check-only # Verify installation only
  python install.py --skip-nltk  # Skip NLTK downloads
        """
    )
    
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check, don't install"
    )
    parser.add_argument(
        "--skip-nltk",
        action="store_true",
        help="Skip NLTK data download"
    )
    parser.add_argument(
        "--skip-spacy",
        action="store_true",
        help="Skip Spacy model download"
    )
    
    args = parser.parse_args()
    
    print_header("🚀 JAIson Unified - Setup & Validation")
    
    print("📋 This script will validate and configure your JAIson installation\n")
    
    # Check directories
    check_directories()
    
    # Check config files
    check_config_files()
    
    # Check Python packages
    all_good = check_python_packages()
    
    # Download NLTK data (unless skipped)
    if not args.skip_nltk:
        if not args.check_only:
            install_nltk_data()
        else:
            print_section("NLTK Data (skipped - check-only mode)")
    
    # Check Spacy models (unless skipped)
    if not args.skip_spacy:
        if not args.check_only:
            check_spacy_models()
        else:
            print_section("Spacy Models (skipped - check-only mode)")
    
    # Check frontend
    check_frontend()
    
    # Final summary
    print_header("✅ Setup Complete!")
    
    print("\n📋 Next steps:\n")
    print("1️⃣  Start the core server:")
    print("    python manager.py core\n")
    print("2️⃣  In another terminal, start an application:")
    print("    python manager.py discord    # Discord bot")
    print("    python manager.py twitch     # Twitch integration")
    print("    python manager.py vts        # VTube Studio\n")
    print("3️⃣  For the web frontend (optional):")
    print("    cd apps/frontend")
    print("    npm install")
    print("    npm run dev\n")
    print("📖 See QUICKSTART.md for detailed instructions")
    print("🔗 Documentation: https://github.com/limitcantcode/jaison-core\n")
    
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
