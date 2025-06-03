# Astrology AI - GitHub Integration Guide

## 🚀 Overview

The Astrology AI project is now fully integrated with GitHub for version control, collaboration, and automated deployments. This document explains all the GitHub features and automation tools available.

## 📦 Repository Information

- **Repository URL**: https://github.com/Veg-briyani/vediq.git
- **Main Branch**: `main`
- **Visibility**: Public (can be changed to private if needed)

## 🛠️ Quick Start Commands

### Using the Deploy Script (Recommended)
```bash
# Simple auto-push with timestamp
./scripts/deploy.sh

# Custom commit message
./scripts/deploy.sh "✨ Added new feature: enhanced rule extraction"
```

### Using the Python Automation Tool
```bash
# Check repository status
python scripts/auto_github.py status

# Auto commit and push
python scripts/auto_github.py push -m "🔄 Auto-update with improvements"

# Create a new release
python scripts/auto_github.py release -v "1.1.0" -m "Major rule extraction improvements"

# Sync with remote
python scripts/auto_github.py sync

# Get current stats
python scripts/auto_github.py stats
```

### Manual Git Commands
```bash
# Add all changes
git add .

# Commit with message
git commit -m "🔄 Manual update"

# Push to GitHub
git push origin main
```

## 🤖 GitHub Actions Workflows

### 1. Continuous Integration (CI)
**File**: `.github/workflows/ci.yml`

**Triggers**: 
- Push to `main` or `develop` branches
- Pull requests to `main`

**What it does**:
- Tests on Python 3.9, 3.10, and 3.11
- Installs dependencies and spaCy models
- Tests all core components (imports, rule extraction, knowledge base)
- Runs linting (black, isort, flake8)
- Security checks (bandit, safety)

**Status**: ✅ Automated testing on every push

### 2. Automated Releases
**File**: `.github/workflows/release.yml`

**Triggers**: 
- Version tags (e.g., `v1.0.0`, `v2.1.3`)

**What it does**:
- Creates GitHub releases automatically
- Generates changelog from commit history
- Packages source code (tar.gz and zip)
- Exports knowledge base (if available)
- Uploads all assets to the release

**Usage**: Create a tag to trigger release
```bash
git tag -a v1.1.0 -m "Release v1.1.0: Enhanced rule extraction"
git push origin v1.1.0
```

## 📁 Directory Structure

```
.
├── .github/
│   └── workflows/
│       ├── ci.yml          # Continuous Integration
│       └── release.yml     # Automated Releases
├── scripts/
│   ├── deploy.sh           # Quick deploy script
│   └── auto_github.py      # Python automation tool
├── .gitignore              # Git ignore rules
└── GITHUB_INTEGRATION.md   # This documentation
```

## 🔄 Automation Features

### Automatic Commits & Pushes

The project includes several automation tools:

#### 1. **Deploy Script** (`scripts/deploy.sh`)
- ✅ Checks for git repository
- ✅ Detects uncommitted changes
- ✅ Adds all changes automatically
- ✅ Creates timestamp-based commit messages
- ✅ Pushes to GitHub
- ✅ Shows repository status and recent commits

#### 2. **Python Automation** (`scripts/auto_github.py`)
- ✅ Repository status checking
- ✅ Automatic commit and push
- ✅ Release creation with version tags
- ✅ Remote synchronization
- ✅ Statistics export
- ✅ Error handling and validation

### Workflow Examples

#### Daily Development Workflow
```bash
# Make your changes to the code
# Then auto-push:
./scripts/deploy.sh "✨ Enhanced rule patterns for better extraction"
```

#### Release Workflow
```bash
# 1. Ensure all changes are committed
./scripts/deploy.sh "🚀 Prepare for release v1.2.0"

# 2. Create and push release tag
python scripts/auto_github.py release -v "1.2.0" -m "Major improvements to rule extraction"

# 3. GitHub Actions will automatically create the release
```

#### Sync Workflow
```bash
# Before starting work, sync with remote
python scripts/auto_github.py sync

# Check current status
python scripts/auto_github.py status
```

## 🏷️ Version Management

### Semantic Versioning
We follow semantic versioning (semver.org):
- **Major** (1.0.0): Breaking changes
- **Minor** (1.1.0): New features, backwards compatible
- **Patch** (1.1.1): Bug fixes, backwards compatible

### Current Version
- **Version**: 1.0.0 (Initial release with rule extraction)
- **Next Planned**: 1.1.0 (Enhanced extraction improvements)

### Creating Releases

#### Automatic (Recommended)
```bash
python scripts/auto_github.py release -v "1.1.0" -m "Enhanced rule extraction with 3x improvement"
```

#### Manual
```bash
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin v1.1.0
```

## 📊 GitHub Actions Status

### CI Pipeline
- ✅ **Python 3.9**: Tests pass
- ✅ **Python 3.10**: Tests pass  
- ✅ **Python 3.11**: Tests pass
- ✅ **Linting**: Code style checks
- ✅ **Security**: Vulnerability scanning

### Release Pipeline
- ✅ **Source Packaging**: tar.gz and zip archives
- ✅ **Knowledge Base Export**: JSON export of rules
- ✅ **Changelog Generation**: Automatic from commits
- ✅ **Asset Upload**: All files attached to release

## 🔐 Security & Best Practices

### Included in .gitignore
- ✅ Python cache files (`__pycache__/`)
- ✅ Virtual environments (`venv/`, `.env`)
- ✅ IDE files (`.vscode/`, `.cursor/`)
- ✅ OS files (`.DS_Store`, `Thumbs.db`)
- ✅ Large PDF books (optional)
- ✅ Database files (optional)
- ✅ Log files and temporary files
- ✅ Configuration with sensitive data

### Security Measures
- ✅ **Bandit**: Security linting for Python
- ✅ **Safety**: Dependency vulnerability checking
- ✅ **No sensitive data**: API keys and secrets excluded
- ✅ **Automated security reports**: Generated on every CI run

## 🚨 Troubleshooting

### Common Issues

#### "Failed to push to GitHub"
```bash
# Check authentication
git remote -v

# Re-authenticate if needed
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### "Git command failed"
```bash
# Check git status
git status

# Reset if needed
git reset --soft HEAD~1
```

#### "GitHub Actions failing"
1. Check the Actions tab on GitHub
2. Review error logs
3. Ensure all required files are present
4. Check Python dependencies in requirements.txt

### Getting Help

#### Check Status
```bash
python scripts/auto_github.py status
```

#### Verify Setup
```bash
# Test that everything works
python -m src.cli test-setup

# Check knowledge base
python -m src.cli stats
```

## 🎯 Future Enhancements

### Planned GitHub Features
- [ ] **Issue Templates**: For bug reports and feature requests
- [ ] **Pull Request Templates**: For contribution guidelines
- [ ] **Branch Protection**: Require reviews for main branch
- [ ] **Dependabot**: Automatic dependency updates
- [ ] **GitHub Pages**: Documentation hosting
- [ ] **Discussion Board**: Community Q&A

### Advanced Automation
- [ ] **Scheduled Backups**: Weekly knowledge base exports
- [ ] **Performance Monitoring**: Track extraction speed
- [ ] **Coverage Reports**: Code coverage tracking
- [ ] **Docker Integration**: Containerized deployments

## 📈 Analytics & Monitoring

### Available Metrics
- ✅ **Commit History**: Track development progress
- ✅ **Knowledge Base Growth**: Rules extracted over time
- ✅ **Code Quality**: Automated linting reports
- ✅ **Security Status**: Vulnerability monitoring

### Accessing Analytics
```bash
# Get current project statistics
python scripts/auto_github.py stats

# View recent commit history
git log --oneline -10

# Check GitHub Actions status
# Visit: https://github.com/Veg-briyani/vediq/actions
```

## 🔗 Quick Links

- **Repository**: https://github.com/Veg-briyani/vediq.git
- **Actions**: https://github.com/Veg-briyani/vediq/actions
- **Releases**: https://github.com/Veg-briyani/vediq/releases
- **Issues**: https://github.com/Veg-briyani/vediq/issues

---

## 📝 Summary

The Astrology AI project now has:
- ✅ **Full GitHub integration** with automated workflows
- ✅ **Simple deployment scripts** for daily development
- ✅ **Automated testing** on multiple Python versions
- ✅ **Automated releases** with version tagging
- ✅ **Security monitoring** and code quality checks
- ✅ **Comprehensive documentation** and troubleshooting guides

**Next Steps**: 
1. Use `./scripts/deploy.sh` for daily updates
2. Create releases with `python scripts/auto_github.py release -v "x.y.z"`
3. Monitor GitHub Actions for build status
4. Enjoy automated backups and version control! 🎉 