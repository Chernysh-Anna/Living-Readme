# 🎬 Living README Agent - Demo Guide

This guide demonstrates the Living README Agent in action, showing how it automatically maintains synchronized documentation.

## 📋 Table of Contents

1. [Setup](#setup)
2. [Demo Scenario 1: Dependency Update](#demo-scenario-1-dependency-update)
3. [Demo Scenario 2: Environment Variable Change](#demo-scenario-2-environment-variable-change)
4. [Demo Scenario 3: Port Configuration Change](#demo-scenario-3-port-configuration-change)
5. [Verification Process](#verification-process)
6. [Report Review](#report-review)

---

## Setup

### Prerequisites

```bash
# Install Python dependencies
pip install -r agent/requirements.txt

# Install Node.js dependencies
cd target-app
npm install
cd ..
```

### Initial State

Before running the demo, verify the initial state:

```bash
# Check current dependencies
cat target-app/package.json | grep express
# Output: "express": "^4.18.2"

# Check current README
cat target-app/README.md | grep "express:"
# Output: - express: ^4.18.2
```

---

## Demo Scenario 1: Dependency Update

### 🎯 Objective
Show how the agent detects and documents dependency version changes.

### Step 1: Update Dependency

Edit `target-app/package.json`:

```diff
  "dependencies": {
-   "express": "^4.18.2",
+   "express": "^4.19.0",
    "dotenv": "^16.0.3",
    "cors": "^2.8.5"
  }
```

### Step 2: Run the Agent

```bash
cd agent
python main.py
```

### Expected Output

```
🤖 Living README Agent Starting...
==================================================================

📍 PHASE 1: Change Detection
──────────────────────────────────────────────────────────────────

🔍 Scanning for changes...
✓ Found 8 configuration items
✓ Parsed 4 managed sections
✓ Updated section: Requirements

📍 PHASE 2: Behavioral Verification
──────────────────────────────────────────────────────────────────

📦 Verifying Installation...
  ▶ Running: npm install
  ✓ Command succeeded

🔨 Verifying Build...
  ▶ Running: npm run build
  ✓ Command succeeded

🚀 Verifying Server Start...
  Expected port: 3000
  ✓ Server is listening on port 3000

📍 PHASE 3: Report Generation
──────────────────────────────────────────────────────────────────

📄 Exporting Reports...
✓ JSON report exported: bob_sessions/2026-05-02-10-30-00-living-readme-update.json
✓ Markdown report exported: bob_sessions/2026-05-02-10-30-00-living-readme-update.md
✓ All reports exported successfully

==================================================================
                    ✅ EXECUTION COMPLETE
==================================================================

📊 Summary:
  - Sections Updated: 1
  - Reports Generated: 2
  - Tests Passed: 3/3
```

### Step 3: Verify README Update

```bash
cat target-app/README.md | grep "express:"
# Output: - express: ^4.19.0
```

### Step 4: Review the Diff

```bash
git diff target-app/README.md
```

```diff
 ### Dependencies
 
-- express: ^4.18.2
+- express: ^4.19.0
 - dotenv: ^16.0.3
 - cors: ^2.8.5
```

---

## Demo Scenario 2: Environment Variable Change

### 🎯 Objective
Demonstrate how the agent tracks environment variable changes.

### Step 1: Update .env File

Edit `target-app/.env`:

```diff
  # Application Configuration
  NODE_ENV=development
- PORT=3000
+ PORT=8080
  HOST=localhost
```

### Step 2: Update Source Code

Edit `target-app/src/config.ts`:

```diff
  export const config: AppConfig = {
    nodeEnv: process.env.NODE_ENV || 'development',
-   port: parseInt(process.env.PORT || '3000', 10),
+   port: parseInt(process.env.PORT || '8080', 10),
    host: process.env.HOST || 'localhost',
```

### Step 3: Run the Agent

```bash
cd agent
python main.py
```

### Expected Changes

The agent will update:
1. **Configuration section** - New PORT value documented
2. **Running section** - Server URL updated to port 8080
3. **Verification** - Tests server starts on port 8080

### Step 4: Verify Updates

```bash
# Check Configuration section
cat target-app/README.md | grep -A 2 "PORT"
# Output: - `PORT`: Server port (default: 8080)

# Check Running section
cat target-app/README.md | grep "localhost:"
# Output: The server will start on `http://localhost:8080`
```

---

## Demo Scenario 3: Port Configuration Change

### 🎯 Objective
Show detection of hardcoded port numbers in source code.

### Step 1: Add Hardcoded Port

Edit `target-app/src/server.ts`:

```typescript
// Add a comment with port reference
// Server will listen on port 8080
```

### Step 2: Run the Agent

```bash
cd agent
python main.py
```

### Expected Behavior

The agent will:
1. Scan all `.ts` files for port patterns
2. Detect the port number 8080
3. Verify it matches the .env configuration
4. Update documentation if needed

---

## Verification Process

### What Gets Verified

The agent runs these commands to ensure documentation is accurate:

#### 1. Installation Verification

```bash
cd target-app
npm install
```

**Checks:**
- All dependencies resolve correctly
- No version conflicts
- Installation completes successfully

#### 2. Build Verification

```bash
npm run build
```

**Checks:**
- TypeScript compiles without errors
- Build output is generated
- No type errors

#### 3. Server Start Verification

```bash
npm start
```

**Checks:**
- Server starts without errors
- Binds to documented port
- Responds to health checks

### Verification Output

```
📊 Verification Summary
==================================================================
  ✓ Passed: 3
  ✗ Failed: 0
  ⊘ Skipped: 0
```

---

## Report Review

### JSON Report Structure

```json
{
  "timestamp": "2026-05-02T10:30:00.000Z",
  "success": true,
  "sections_updated": ["Requirements", "Configuration"],
  "changes_detected": {
    "dependencies": [...],
    "env_variables": [...],
    "port_configs": [...]
  },
  "verification_results": {
    "summary": {
      "total": 3,
      "passed": 3,
      "failed": 0
    }
  }
}
```

### Markdown Report Preview

```markdown
# Living README Agent - Execution Report

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
```

### Accessing Reports

```bash
# View latest markdown report
cat bob_sessions/*.md | tail -n 100

# Parse JSON report
jq '.verification_results.summary' bob_sessions/*.json | tail -n 1

# List all reports
ls -lh bob_sessions/
```

---

## GitHub Actions Integration

### Triggering the Workflow

The agent runs automatically when you:

1. **Push changes** to monitored files:
   ```bash
   git add target-app/package.json
   git commit -m "Update express to 4.19.0"
   git push
   ```

2. **Create a Pull Request** with changes to:
   - `target-app/package.json`
   - `target-app/.env`
   - `target-app/src/**/*.ts`

### Workflow Output

The GitHub Action will:
1. ✅ Run the Living README Agent
2. ✅ Verify all setup commands
3. ✅ Generate reports
4. ✅ Create a PR with updates (if changes detected)
5. ✅ Upload reports as artifacts

### PR Description Example

```markdown
## 🤖 Automated README Update

### 📋 Changes Detected
- Updated express from ^4.18.2 to ^4.19.0

### ✅ Verification Status
- ✅ npm install: Success
- ✅ npm build: Success
- ✅ npm start: Success (port 3000)

### 📊 Reports
Detailed reports available in workflow artifacts.
```

---

## Testing the Complete Flow

### End-to-End Test

```bash
# 1. Make a change
echo 'PORT=9000' >> target-app/.env

# 2. Run the agent
cd agent && python main.py && cd ..

# 3. Check the diff
git diff target-app/README.md

# 4. Review reports
cat bob_sessions/INDEX.md

# 5. Verify the change
grep "9000" target-app/README.md
```

### Expected Results

- ✅ README updated with new port
- ✅ Verification tests pass
- ✅ Reports generated in bob_sessions/
- ✅ All changes documented

---

## Troubleshooting

### Agent Not Detecting Changes

**Check:**
1. File paths in `doc_rules.json` are correct
2. Changes match monitored patterns
3. README has proper section markers

### Verification Failing

**Check:**
1. Dependencies are installed: `cd target-app && npm install`
2. .env file exists and is readable
3. Port is not already in use

### Reports Not Generated

**Check:**
1. `bob_sessions/` directory exists
2. Python has write permissions
3. Reporter module is imported correctly

---

## Next Steps

1. **Customize Configuration**: Edit `agent/doc_rules.json` for your needs
2. **Add More Sections**: Define new managed sections in README
3. **Extend Monitoring**: Add more file patterns to watch
4. **Integrate CI/CD**: Enable GitHub Actions workflow

---

## 🎓 Learning Points

After completing this demo, you should understand:

- ✅ How the agent detects changes in your codebase
- ✅ How README sections are automatically updated
- ✅ How verification ensures documentation accuracy
- ✅ How reports provide audit trails
- ✅ How GitHub Actions automates the process

---

**Ready to see it in action? Start with Demo Scenario 1!** 🚀