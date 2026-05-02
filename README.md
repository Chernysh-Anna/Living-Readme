# 🤖 Living README Agent

> **An autonomous development partner that ensures README documentation never goes out of sync with your actual codebase.**

[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-blue)](https://github.com/features/actions)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://www.python.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.1+-blue)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

## 🎯 Overview

The Living README Agent monitors your codebase for changes and automatically updates documentation to stay in sync. No more outdated README files with wrong dependency versions, incorrect port numbers, or missing environment variables.

**The Problem:** Documentation drift is common - developers update code but forget to update README files.

**The Solution:** This agent automatically detects changes in dependencies, environment variables, and configurations, updates relevant README sections, verifies setup commands actually work, and creates pull requests with detailed change reports.

## ✨ Key Features

### 🔍 Context Awareness
- Monitors `package.json` for dependency version changes (major/minor)
- Tracks `.env` file for environment variable updates
- Scans source code for port number configurations

### 🔄 Auto-Update
- Parses README.md and identifies managed sections
- Generates updated content based on detected changes
- Preserves custom notes and human-written content

### ✅ Behavioral Verification
- Runs `npm install` to verify dependencies resolve
- Executes `npm build` to ensure project compiles
- Tests `npm start` to confirm server starts correctly

### 📊 Comprehensive Reporting
- Exports JSON reports with full change details
- Generates Markdown summaries for easy review
- Maintains audit trail in `bob_sessions/` directory

### 🤝 GitHub Integration
- Triggers on commits and pull requests
- Creates automated PRs with proposed changes
- Uploads reports as workflow artifacts

## 🏗️ Architecture

**Components:**

1. **Watcher** (`agent/watcher.py`)
   - ChangeDetector: Scans target-app for changes
   - ReadmeParser: Extracts managed sections from README
   - ReadmeGenerator: Creates updated content from templates

2. **Verifier** (`agent/verifier.py`)
   - CommandVerifier: Executes setup commands
   - Validates installation, build, and runtime
   - Checks port binding and configuration

3. **Reporter** (`agent/reporter.py`)
   - Exports JSON reports with full details
   - Generates Markdown summaries
   - Maintains index of all reports

4. **Orchestrator** (`agent/main.py`)
   - Coordinates all components
   - Manages execution flow
   - Generates PR summaries

**Flow:**
```
GitHub Trigger → Watcher (detect changes) → Verifier (test commands) 
→ Reporter (generate reports) → Updated README + PR
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### Installation

```bash
# Clone repository
git clone <repository-url>
cd Living-Readme

# Install Python dependencies
pip install -r agent/requirements.txt

# Install Node.js dependencies
cd target-app && npm install && cd ..
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

### Change Detection

Monitored files in `target-app/`:
- `package.json` - Dependency versions
- `.env` - Environment variables
- `src/**/*.ts` - Port configurations

### README Management

Sections are marked with special comments:

```markdown
<!-- MANAGED_SECTION:START:Requirements -->
## Requirements
- Node.js >= 18.0.0
- express: ^4.18.2
<!-- MANAGED_SECTION:END:Requirements -->
```

Content between markers is replaced entirely. Sections outside markers are preserved.

### Verification Process

```bash
npm install    # Verify dependencies resolve
npm run build  # Ensure TypeScript compiles
npm start      # Test server starts on correct port
```

### Report Generation

Reports exported to `bob_sessions/`:
```
bob_sessions/
├── 2026-05-02-10-30-00-living-readme-update.json
├── 2026-05-02-10-30-00-living-readme-update.md
└── INDEX.md
```

## ⚙️ Configuration

Configure via `agent/doc_rules.json`:

```json
{
  "target_app": {
    "path": "./target-app",
    "package_manager": "npm"
  },
  "monitoring": {
    "files": [
      {
        "path": "target-app/package.json",
        "watch_fields": ["dependencies"],
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

**Key options:**
- `monitoring.files` - Which files to watch and what to track
- `readme_management.managed_sections` - Which README sections to auto-update
- `verification.commands` - Setup commands to verify
- `reporting.formats` - Export formats (json, markdown)

## 🎬 Demo Example

See [DEMO.md](DEMO.md) for detailed walkthrough.

**Quick example:**

1. Developer updates `package.json`:
   ```json
   "express": "^4.19.0"  // Changed from 4.18.2
   ```

2. Agent detects change:
   ```
   🔍 Scanning for changes...
   ✓ Found 1 configuration items
   ```

3. Agent updates README:
   ```diff
   - express: ^4.18.2
   + express: ^4.19.0
   ```

4. Agent verifies setup:
   ```
   ✓ npm install succeeded
   ✓ npm build succeeded
   ✓ Server listening on port 3000
   ```

5. Agent creates PR with change summary and verification results.

## 📁 Project Structure

```
living-readme/
├── .github/workflows/
│   └── living-readme.yml      # GitHub Actions workflow
├── agent/
│   ├── doc_rules.json         # Configuration
│   ├── requirements.txt       # Python dependencies
│   ├── watcher.py            # Change detection
│   ├── verifier.py           # Command verification
│   ├── reporter.py           # Report generation
│   └── main.py               # Main orchestrator
├── target-app/               # Sample application
│   ├── src/
│   │   ├── index.ts         # Main entry point
│   │   ├── server.ts        # Express server
│   │   └── config.ts        # Configuration loader
│   ├── package.json         # Dependencies (monitored)
│   ├── .env                 # Environment vars (monitored)
│   └── README.md            # App documentation (managed)
├── bob_sessions/            # Execution reports
│   ├── *.json              # JSON reports
│   ├── *.md                # Markdown reports
│   └── INDEX.md            # Report index
└── README.md               # This file
```

## 📊 Bob Sessions

The `bob_sessions/` directory contains execution reports for judges and auditors.

**JSON Format:**
- Complete change detection data
- Verification results with stdout/stderr
- Timestamps and metadata

**Markdown Format:**
- Executive summary
- Change tables (dependencies, env vars, ports)
- Verification test results

**Example report:**
```markdown
# Living README Agent - Execution Report

**Generated:** 2026-05-02T10:30:00Z

## Executive Summary
- **Sections Updated:** 2
- **Status:** ✅ Success

## Changes Detected
| Package | Version | Category |
|---------|---------|----------|
| express | ^4.19.0 | production |

## Verification Results
- **Passed:** ✅ 3
- **Failed:** ❌ 0
```

## 🛠️ Development

### Running Tests

```bash
# Test individual modules
cd agent
python watcher.py
python verifier.py
python reporter.py

# Full integration test
python main.py
```

### Adding Monitored Files

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

Edit templates in `doc_rules.json`:
```json
{
  "templates": {
    "requirements": {
      "format": "markdown",
      "sections": [
        {
          "title": "Custom Section",
          "content": "{placeholder}"
        }
      ]
    }
  }
}
```

## 🤝 Contributing

Contributions welcome! Please:

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
