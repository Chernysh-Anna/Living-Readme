# 🤖 Living README Agent

> **An autonomous development partner that ensures README documentation never goes out of sync with your actual codebase.**

[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-blue)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.1+-blue)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Demo Scenario](#demo-scenario)
- [Project Structure](#project-structure)
- [Bob Sessions](#bob-sessions)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The Living README Agent is an intelligent automation system that monitors your codebase for changes and automatically updates your documentation to stay in sync. No more outdated README files with wrong dependency versions, incorrect port numbers, or missing environment variables!

### The Problem

Documentation drift is a common issue in software development:
- ✗ Developer updates `package.json` but forgets to update README
- ✗ Port number changes in code but documentation still shows old port
- ✗ New environment variables added but not documented
- ✗ Setup instructions become outdated and fail for new developers

### The Solution

The Living README Agent automatically:
- ✓ Detects changes in dependencies, environment variables, and configurations
- ✓ Updates relevant README sections with accurate information
- ✓ Verifies setup commands actually work by running them
- ✓ Creates pull requests with detailed change reports
- ✓ Exports audit trails for review and compliance

## ✨ Key Features

### 🔍 **Context Awareness**
- Monitors `package.json` for dependency version changes (major/minor)
- Tracks `.env` file for environment variable updates
- Scans source code for port number configurations
- Detects setup-critical changes automatically

### 🔄 **Auto-Update**
- Parses README.md and identifies managed sections
- Generates updated content based on detected changes
- Preserves custom notes and human-written content
- Creates clean, readable documentation

### ✅ **Behavioral Verification**
- Runs `npm install` to verify dependencies resolve
- Executes `npm build` to ensure project compiles
- Tests `npm start` to confirm server starts correctly
- Validates port binding and configuration

### 📊 **Comprehensive Reporting**
- Exports JSON reports with full change details
- Generates Markdown summaries for easy review
- Maintains audit trail in `bob_sessions/` directory
- Creates PR descriptions with verification results

### 🤝 **GitHub Integration**
- Triggers on commits and pull requests
- Creates automated PRs with proposed changes
- Comments on PRs with change summaries
- Uploads reports as workflow artifacts

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Actions Trigger                    │
│              (Commit/PR on monitored files)                  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Living README Agent                        │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Watcher    │  │   Verifier   │  │   Reporter   │     │
│  │              │  │              │  │              │     │
│  │ • Detect     │  │ • Run npm    │  │ • Generate   │     │
│  │   changes    │  │   install    │  │   JSON       │     │
│  │ • Parse      │  │ • Run npm    │  │ • Generate   │     │
│  │   README     │  │   build      │  │   Markdown   │     │
│  │ • Generate   │  │ • Test npm   │  │ • Create     │     │
│  │   updates    │  │   start      │  │   index      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Output & Actions                          │
│                                                              │
│  • Updated README.md with synchronized content               │
│  • Pull Request with change summary                          │
│  • Reports in bob_sessions/ (JSON + Markdown)               │
│  • GitHub Actions artifacts for review                       │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1. **Watcher** (`agent/watcher.py`)
- **ChangeDetector**: Scans target-app for changes
- **ReadmeParser**: Extracts managed sections from README
- **ReadmeGenerator**: Creates updated content from templates

#### 2. **Verifier** (`agent/verifier.py`)
- **CommandVerifier**: Executes setup commands
- Validates installation, build, and runtime
- Checks port binding and configuration

#### 3. **Reporter** (`agent/reporter.py`)
- Exports JSON reports with full details
- Generates Markdown summaries
- Maintains index of all reports

#### 4. **Orchestrator** (`agent/main.py`)
- Coordinates all components
- Manages execution flow
- Generates PR summaries

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Living-Readme
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r agent/requirements.txt
   ```

3. **Install Node.js dependencies (for target-app)**
   ```bash
   cd target-app
   npm install
   cd ..
   ```

### Running the Agent

**Manual execution:**
```bash
cd agent
python main.py
```

**Automated via GitHub Actions:**
- Push changes to monitored files
- Agent runs automatically
- Creates PR with updates

## 🔧 How It Works

### 1. Change Detection

The agent monitors these files in `target-app/`:

```yaml
Monitored Files:
  - package.json          # Dependency versions
  - .env                  # Environment variables
  - src/**/*.ts          # Port configurations
```

### 2. README Management

README sections are marked with special comments:

```markdown
<!-- MANAGED_SECTION:START:Requirements -->
## Requirements
- Node.js >= 18.0.0
- express: ^4.18.2
<!-- MANAGED_SECTION:END:Requirements -->
```

Sections outside these markers are preserved (human-written content).

### 3. Verification Process

```bash
Step 1: npm install    # Verify dependencies resolve
Step 2: npm run build  # Ensure TypeScript compiles
Step 3: npm start      # Test server starts on correct port
```

### 4. Report Generation

Reports are exported to `bob_sessions/`:

```
bob_sessions/
├── 2026-05-02-10-30-00-living-readme-update.json
├── 2026-05-02-10-30-00-living-readme-update.md
└── INDEX.md
```

## ⚙️ Configuration

The agent is configured via `agent/doc_rules.json`:

```json
{
  "target_app": {
    "path": "./target-app",
    "package_manager": "npm",
    "language": "typescript"
  },
  "monitoring": {
    "files": [
      {
        "path": "target-app/package.json",
        "watch_fields": ["dependencies", "devDependencies"],
        "change_types": ["major", "minor"]
      }
    ]
  },
  "verification": {
    "enabled": true,
    "commands": [
      {
        "name": "install_dependencies",
        "command": "npm install",
        "timeout": 300
      }
    ]
  }
}
```

### Key Configuration Options

- **monitoring.files**: Which files to watch and what to track
- **readme_management.managed_sections**: Which README sections to auto-update
- **verification.commands**: Setup commands to verify
- **reporting.formats**: Export formats (json, markdown)
- **pr_creation**: PR title/body templates

## 🎬 Demo Scenario

### Before: Developer Updates Dependencies

```json
// target-app/package.json
{
  "dependencies": {
    "express": "^4.18.2"  // Updated from 4.17.0
  }
}
```

### Agent Detects Change

```
🔍 Scanning for changes...
✓ Found 1 configuration items
  - express: ^4.18.2 (production dependency)
```

### Agent Updates README

```diff
<!-- MANAGED_SECTION:START:Requirements -->
## Requirements

### Dependencies

- express: ^4.18.2
+ express: ^4.19.0
<!-- MANAGED_SECTION:END:Requirements -->
```

### Agent Verifies Setup

```
📦 Verifying Installation...
  ▶ Running: npm install
  ✓ Command succeeded

🔨 Verifying Build...
  ▶ Running: npm run build
  ✓ Command succeeded

🚀 Verifying Server Start...
  Expected port: 3000
  ✓ Server is listening on port 3000
```

### Agent Creates PR

```markdown
## 📝 Living README Agent Update

**Total Changes Detected:** 1

**Sections Updated:**
- ✅ Requirements

**Verification Results:**
- ✅ Passed: 3
- ❌ Failed: 0

### 📦 Dependencies
- `express`: ^4.19.0
```

## 📁 Project Structure

```
living-readme/
├── .github/
│   └── workflows/
│       └── living-readme.yml      # GitHub Actions workflow
├── agent/
│   ├── doc_rules.json             # Configuration
│   ├── requirements.txt           # Python dependencies
│   ├── watcher.py                 # Change detection
│   ├── verifier.py                # Command verification
│   ├── reporter.py                # Report generation
│   └── main.py                    # Main orchestrator
├── target-app/                    # Sample application
│   ├── src/
│   │   ├── index.ts              # Main entry point
│   │   ├── server.ts             # Express server
│   │   └── config.ts             # Configuration loader
│   ├── package.json              # Dependencies (monitored)
│   ├── tsconfig.json             # TypeScript config
│   ├── .env                      # Environment vars (monitored)
│   └── README.md                 # App documentation (managed)
├── bob_sessions/                  # Execution reports (MANDATORY)
│   ├── *.json                    # JSON reports
│   ├── *.md                      # Markdown reports
│   └── INDEX.md                  # Report index
└── README.md                      # This file
```

## 📊 Bob Sessions

The `bob_sessions/` directory contains execution reports for judges and auditors:

### Report Contents

**JSON Format:**
- Complete change detection data
- Verification results with stdout/stderr
- Timestamps and metadata
- Configuration snapshot

**Markdown Format:**
- Executive summary
- Change tables (dependencies, env vars, ports)
- Verification test results
- Diff previews

### Example Report Structure

```markdown
# Living README Agent - Execution Report

**Generated:** 2026-05-02T10:30:00Z
**Agent Version:** 1.0.0

## Executive Summary
- **Sections Updated:** 2
- **Status:** ✅ Success

## Changes Detected
### Dependencies
| Package | Version | Category |
|---------|---------|----------|
| express | ^4.19.0 | production |

## Verification Results
- **Total Tests:** 3
- **Passed:** ✅ 3
- **Failed:** ❌ 0
```

## 🛠️ Development

### Running Tests

```bash
# Test watcher standalone
cd agent
python watcher.py

# Test verifier standalone
python verifier.py

# Test reporter standalone
python reporter.py

# Full integration test
python main.py
```

### Adding New Monitored Files

1. Update `doc_rules.json`:
   ```json
   {
     "monitoring": {
       "files": [
         {
           "path": "target-app/new-file.json",
           "watch_fields": ["field1", "field2"]
         }
       ]
     }
   }
   ```

2. Add detection logic in `watcher.py`
3. Update README template in `doc_rules.json`

### Customizing Templates

Edit `doc_rules.json` templates section:

```json
{
  "templates": {
    "requirements": {
      "format": "markdown",
      "sections": [
        {
          "title": "Custom Section",
          "content": "{custom_placeholder}"
        }
      ]
    }
  }
}
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Built with Python, TypeScript, and GitHub Actions
- Inspired by the need for always-accurate documentation
- Designed for the Bob AI Agent competition

---

**Made with ❤️ by the Living README Agent Team**

*Keeping documentation alive, one commit at a time.*
