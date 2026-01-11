#!/usr/bin/env python3
"""
JAIson Unified - Setup & Installation Script
CLI installer with setuptools configuration

Usage:
    python setup.py --help
    python setup.py develop
    pip install -e .
"""

from setuptools import setup, find_packages
from pathlib import Path
import sys

# Read README
readme_path = Path(__file__).parent / "README-UNIFIED.md"
long_description = ""
if readme_path.exists():
    long_description = readme_path.read_text(encoding="utf-8")

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
    version="2.0.0",
    description="JAIson Unified - AI Companion System with Discord, Twitch & VTube Studio Integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="JAIson Community",
    author_email="contact@jaison.dev",
    url="https://github.com/limitcantcode/jaison-core",
    project_urls={
        "Documentation": "https://github.com/limitcantcode/jaison-core/blob/main/README.md",
        "Discord": "https://discord.gg/Z8yyEzHsYM",
        "Source": "https://github.com/limitcantcode/jaison-core",
        "Tracker": "https://github.com/limitcantcode/jaison-core/issues",
    },
    license="MIT",
    packages=find_packages(include=["src", "src.*"]),
    python_requires=">=3.12",
    install_requires=core_requirements,
    extras_require=extras,
    entry_points={
        "console_scripts": [
            "jaison=src.main:cli",
            "jaison-manager=manager:main",
            "jaison-install=install:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
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
