#!/usr/bin/env python3
"""
JAIson Unified System Manager
Manage running the core server and applications
"""

import argparse
import subprocess
import os
import sys
from pathlib import Path

def get_base_dir():
    """Get the base directory of this project"""
    return Path(__file__).parent.absolute()

def start_core(args):
    """Start the core JAIson server"""
    base_dir = get_base_dir()
    os.chdir(base_dir)
    
    cmd = [sys.executable, "src/main.py"]
    if args.debug:
        cmd.append("--debug")
    
    print("🚀 Starting JAIson Core Server...")
    print(f"   Command: {' '.join(cmd)}")
    print(f"   API: http://localhost:7272")
    print(f"   WebSocket: ws://localhost:7272")
    
    subprocess.run(cmd)

def start_discord(args):
    """Start the Discord bot integration"""
    base_dir = get_base_dir()
    os.chdir(base_dir / "apps" / "discord")
    
    # Check for .env file
    if not Path(".env").exists():
        print("❌ Discord bot requires .env file")
        print("   Copy .env-template to .env and add your Discord bot token")
        return
    
    cmd = [sys.executable, "src/main.py"]
    if args.debug:
        cmd.append("--debug")
    
    print("🤖 Starting Discord Bot Integration...")
    print(f"   Make sure the core server is running on ws://127.0.0.1:7272")
    
    subprocess.run(cmd)

def start_twitch(args):
    """Start the Twitch integration"""
    base_dir = get_base_dir()
    app_dir = base_dir / "apps" / "twitch"
    os.chdir(app_dir)
    
    # Check for .env file
    if not Path(".env").exists():
        print("❌ Twitch integration requires .env file")
        print("   Copy .env-template to .env with your Twitch credentials")
        return
    
    # Check if tokens exist, if not authenticate
    if not Path("tokens").exists():
        print("🔑 Running Twitch authentication...")
        subprocess.run([sys.executable, "src/auth.py"])
    
    cmd = [sys.executable, "src/main.py"]
    if args.debug:
        cmd.append("--debug")
    
    print("🎮 Starting Twitch Integration...")
    print(f"   Make sure the core server is running on ws://127.0.0.1:7272")
    
    subprocess.run(cmd)

def start_vts(args):
    """Start the VTube Studio integration"""
    base_dir = get_base_dir()
    os.chdir(base_dir / "apps" / "vts")
    
    cmd = [sys.executable, "src/main.py"]
    if args.debug:
        cmd.append("--debug")
    
    print("🎭 Starting VTube Studio Integration...")
    print(f"   Make sure VTube Studio API is enabled on ws://localhost:8001")
    print(f"   Make sure the core server is running on ws://localhost:7272")
    
    subprocess.run(cmd)

def show_status(args):
    """Show status of the system"""
    base_dir = get_base_dir()
    
    print("📊 JAIson Unified System Status")
    print("=" * 50)
    
    # Check core config
    config_path = base_dir / "config.yaml"
    print(f"\n✓ Core server configured: {config_path.exists()}")
    
    # Check apps
    apps = ["discord", "twitch", "vts"]
    for app in apps:
        app_dir = base_dir / "apps" / app
        env_file = app_dir / ".env"
        config_file = app_dir / "config.yaml"
        
        print(f"\n✓ {app.upper()} Integration:")
        print(f"  - Directory: {app_dir.exists()}")
        print(f"  - Config: {config_file.exists()}")
        print(f"  - .env file: {env_file.exists()}")
    
    print("\n" + "=" * 50)

def main():
    parser = argparse.ArgumentParser(
        description="JAIson Unified System Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python manager.py core              # Start core server
  python manager.py discord           # Start Discord bot
  python manager.py twitch            # Start Twitch integration
  python manager.py vts               # Start VTube Studio integration
  python manager.py status            # Show system status
        """
    )
    
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Commands
    subparsers.add_parser("core", help="Start the core JAIson server")
    subparsers.add_parser("discord", help="Start Discord bot integration")
    subparsers.add_parser("twitch", help="Start Twitch integration")
    subparsers.add_parser("vts", help="Start VTube Studio integration")
    subparsers.add_parser("status", help="Show system status")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "core":
        start_core(args)
    elif args.command == "discord":
        start_discord(args)
    elif args.command == "twitch":
        start_twitch(args)
    elif args.command == "vts":
        start_vts(args)
    elif args.command == "status":
        show_status(args)

if __name__ == "__main__":
    main()
