# 🤝 Contributing to Project J.A.I.son

Thank you for your interest in contributing to Project J.A.I.son! This project thrives on community contributions, whether it's code, documentation, bug reports, or feature ideas.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Feature Requests](#feature-requests)
- [Questions & Support](#questions--support)

---

## 📜 Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please:

- ✅ Be respectful and considerate
- ✅ Welcome different opinions and experiences
- ✅ Provide constructive feedback
- ❌ No harassment, discrimination, or hate speech
- ❌ No spam or self-promotion

---

## 💡 How to Contribute

### 🐛 Found a Bug?

1. **Check if it's already reported** - Search [Issues](https://github.com/limitcantcode/jaison-core/issues)
2. **Create a detailed bug report** including:
   - What you were trying to do
   - What you expected to happen
   - What actually happened
   - Your environment (OS, Python version, etc.)
   - Error messages or logs
   - Minimal code to reproduce

### 🎯 Have a Feature Idea?

1. **Discuss first** - Open an [Issue](https://github.com/limitcantcode/jaison-core/issues) to discuss your idea
2. **Explain the use case** - Why is this feature needed?
3. **Get feedback** - We want to align on the approach before you code
4. **Propose an implementation** - How would you implement it?

### 📚 Improve Documentation?

Documentation is crucial! You can:
- Fix typos in README or docs
- Add examples or tutorials
- Clarify confusing sections
- Translate to other languages

No approval needed—just submit a PR!

### 🔧 Submit Code

Follow the guidelines below for the best chance of acceptance.

---

## 🛠️ Development Setup

### 1. Fork & Clone

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/jaison-core.git
cd jaison-core
git remote add upstream https://github.com/limitcantcode/jaison-core.git
```

### 2. Create Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `.\venv\Scripts\activate` on Windows

# Install in development mode with dev dependencies
pip install -e .[dev]
pip install -r requirements.txt
```

### 3. Set Up Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

---

## 📝 Commit Guidelines

### Commit Message Format

Use clear, descriptive commit messages following this format:

```
[TYPE] Brief description (50 chars or less)

Optional longer explanation (72 chars per line):
- What changed
- Why it changed  
- Any relevant details
```

### Commit Types

- `[feature]` - New feature
- `[fix]` - Bug fix
- `[refactor]` - Code restructuring
- `[perf]` - Performance improvement
- `[docs]` - Documentation changes
- `[test]` - Test additions/changes
- `[chore]` - Build, dependency updates, etc.

### Examples

```
[feature] Add voice filtering support to Discord bot

[fix] Resolve FFmpeg path detection on Windows

[docs] Update macOS installation guide

[perf] Optimize WebSocket parsing (+30% speed)
```

---

## 🔄 Pull Request Process

### 1. Create a Feature Branch

```bash
git checkout -b feature/amazing-feature
```

### 2. Make Your Changes

- ✅ Write clear, well-commented code
- ✅ Follow existing code style (PEP 8)
- ✅ Add tests for new features
- ✅ Update documentation

### 3. Run Tests & Checks

```bash
pytest tests/           # Run tests
black src/              # Format code
flake8 src/             # Lint
mypy src/               # Type checking
```

### 4. Keep Branch Updated

```bash
git fetch upstream
git rebase upstream/main
```

### 5. Push & Create PR

```bash
git push origin feature/amazing-feature
```

**Include in PR Description:**
- What changed and why
- Related issues (fixes #123)
- How to test
- Checklist of completion

---

## 🐛 Reporting Issues

**Title Format:**
```
[BUG] Short description
```

**Include:**
- OS, Python version, JAIson version
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs
- Screenshots if applicable

---

## 🎯 Feature Requests

**Title Format:**
```
[FEATURE] Short description
```

**Include:**
- Use case (why is this needed?)
- Proposed solution
- Alternative approaches
- Additional context/examples

---

## ❓ Questions?

- **Discord**: [Join Server](https://discord.gg/Z8yyEzHsYM)
- **Discussions**: [GitHub Discussions](https://github.com/limitcantcode/jaison-core/discussions)
- **Email**: community@jaison.dev

---

## 📜 Code Style

We follow PEP 8 with automated formatting:

```bash
black src/ --line-length 100
isort src/
flake8 src/
```

Use type hints:
```python
def greet(name: str) -> str:
    """Greet a person."""
    return f"Hello, {name}!"
```

---

## 🚀 Review Process

PRs are reviewed within 7 days. We check:
- Code quality and style
- Logic and implementation
- Tests and documentation
- Compatibility

Common feedback:
- "Add tests" - Unit tests needed
- "Update docs" - Document changes
- "Fix style" - See code style guide
- "Break into smaller PR" - Large PRs are harder to review

---

## 🎉 All Contributions Welcome!

We appreciate:
- 🐛 Bug fixes
- ✨ Features  
- 📚 Documentation
- 🧪 Tests
- 🌐 Translations
- 💬 Community support

---

<p align="center">
  <strong>Thank you for making J.A.I.son better! ❤️</strong>
</p>