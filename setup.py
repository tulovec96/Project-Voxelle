#!/usr/bin/env python3
"""
JAIson Unified - Setup & Installation Script
Professional setuptools configuration with full metadata

Installation methods:
    pip install -e .                    # Development mode (recommended)
    pip install .                       # Standard install
    python setup.py install             # Legacy method
    python setup.py develop             # For development
"""

from setuptools import setup, find_packages
from pathlib import Path
import sys
import re

# Get version from package
def get_version():
    """Extract version from version file or default"""
    version_file = Path(__file__).parent / "src" / "__init__.py"
    if version_file.exists():
        content = version_file.read_text()
        match = re.search(r'__version__\s*=\s*["\']([^"\']*)["\']', content)
        if match:
            return match.group(1)
    return "2.0.0"  # Default version

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = ""
long_description_content_type = "text/markdown"

if readme_path.exists():
    long_description = readme_path.read_text(encoding="utf-8")
else:
    long_description = """# Project J.A.I.son - Unified Edition
An extensible, open-source AI companion framework with Discord, Twitch, VTube Studio integration."""

# Core dependencies
core_requirements = [
    # AI/ML
    "torch>=2.5.0",
    "transformers>=4.50.0",
    "tokenizers>=0.21.0",
    "nltk>=3.9.0",
    "spacy>=3.8.0",
    
    # Audio
    "librosa>=0.9.0",
    "soundfile>=0.13.0",
    "pydub>=0.25.0",
    "azure-cognitiveservices-speech>=1.44.0",
    
    # Web
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.34.0",
    "websockets>=15.0.0",
    "pydantic>=2.11.0",
    "python-dotenv>=1.1.0",
    
    # Utilities
    "requests>=2.32.0",
    "pyyaml>=6.0.0",
    "typer[all]>=0.16.0",
    "rich>=13.9.0",
    
    # Discord
    "git+https://github.com/Rapptz/discord.py.git",
    "git+https://github.com/imayhaveborkedit/discord-ext-voice-recv.git",
    
    # Scheduling
    "apscheduler>=3.11.0",
]

# Optional extras
extras = {
    "dev": [
        "pytest>=7.0",
        "pytest-asyncio>=0.21.0",
        "black>=23.0",
        "flake8>=6.0",
        "mypy>=1.0",
    ],
    "docs": [
        "sphinx>=5.0",
        "sphinx-rtd-theme>=1.0",
    ],
    "audio": [
        "openai>=1.0",  # Whisper via OpenAI API
        "gradio>=5.0",  # Web UI
    ],
}

# All extras
extras["all"] = sum(extras.values(), [])

setup(
    name="jaison-unified",
    version=get_version(),
    description="JAIson Unified - AI Companion System with Discord, Twitch & VTube Studio Integration",
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    author="JAIson Community",
    author_email="community@jaison.dev",
    maintainer="tulovec96",
    maintainer_email="tulov@example.com",
    url="https://github.com/limitcantcode/jaison-core",
    project_urls={
        "Documentation": "https://github.com/limitcantcode/jaison-core/blob/main/DEVELOPER.md",
        "API Spec": "https://github.com/limitcantcode/jaison-core/blob/main/api.yaml",
        "Discord": "https://discord.gg/Z8yyEzHsYM",
        "Source": "https://github.com/limitcantcode/jaison-core",
        "Issue Tracker": "https://github.com/limitcantcode/jaison-core/issues",
        "Changelog": "https://github.com/limitcantcode/jaison-core/blob/main/CHANGELOG.md",
    },
    license="MIT",
    packages=find_packages(include=["src", "src.*"]),
    python_requires=">=3.12",
    install_requires=core_requirements,
    extras_require=extras,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "jaison=src.main:cli",
            "jaison-manager=manager:main",
            "jaison-install=install:main",
        ],
    },
    keywords=[
        "ai",
        "companion",
        "discord",
        "twitch",
        "vtuber",
        "streaming",
        "chatbot",
        "framework",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords=[
        "ai",
        "companion",
        "discord",
        "twitch",
        "vtuber",
        "vtubestudio",
        "asr",
        "tts",
        "nlp",
    ],
    include_package_data=True,
    zip_safe=False,
)
