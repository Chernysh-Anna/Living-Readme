# 🎬 Living README Agent - Demo Guide

Quick demonstration of the Living README Agent's automatic documentation synchronization.

## Prerequisites

See main [README.md](README.md) for installation instructions.

## Demo Scenarios

### Scenario 1: Dependency Update

**Update package.json:**
```diff
  "dependencies": {
-   "express": "^4.18.2",
+   "express": "^4.19.0",
```

**Run agent:**
```bash
cd agent && python main.py
```

**Expected output:**
```
🤖 Living README Agent Starting...
📍 PHASE 1: Change Detection
  ✓ Found 8 configuration items
  ✓ Updated section: Requirements

📍 PHASE 2: Behavioral Verification
  ✓ npm install succeeded
  ✓ npm build succeeded
  ✓ Server listening on port 3000

📍 PHASE 3: Report Generation
  ✓ Reports exported to bob_sessions/
```

**Verify README update:**
```bash
git diff target-app/README.md
# Shows: - express: ^4.18.2 → + express: ^4.19.0
```

### Scenario 2: Port Configuration Change

**Update .env and config.ts:**
```diff
# .env
- PORT=3000
+ PORT=8080

# src/config.ts
- port: parseInt(process.env.PORT || '3000', 10),
+ port: parseInt(process.env.PORT || '8080', 10),
```

**Run agent:**
```bash
cd agent && python main.py
```

**Agent updates:**
- Configuration section with new PORT value
- Running instructions with updated URL
- Verifies server starts on port 8080

**Verify:**
```bash
cat target-app/README.md | grep "PORT"
# Output: - `PORT`: Server port (default: 8080)
```

## Verification Process

The agent validates documentation accuracy by running:

```bash
npm install    # Dependencies resolve correctly
npm run build  # TypeScript compiles without errors
npm start      # Server starts on documented port
```

**Verification output:**
```
📊 Verification Summary
  ✓ Passed: 3
  ✗ Failed: 0
```

## Report Structure

Reports are exported to `bob_sessions/`:

**JSON Report:**
```json
{
  "timestamp": "2026-05-02T10:30:00.000Z",
  "success": true,
  "sections_updated": ["Requirements"],
  "verification_results": {
    "total": 3,
    "passed": 3,
    "failed": 0
  }
}
```

**Markdown Report:**
```markdown
# Living README Agent - Execution Report

## Executive Summary
- **Sections Updated:** 1
- **Status:** ✅ Success

## Changes Detected
| Package | Version | Category |
|---------|---------|----------|
| express | ^4.19.0 | production |

## Verification Results
- **Passed:** ✅ 3
```

**Access reports:**
```bash
# View latest report
cat bob_sessions/*.md | tail -n 50

# List all reports
ls -lh bob_sessions/
```

## GitHub Actions Integration

**Automatic triggers:**
- Push changes to `target-app/package.json`, `.env`, or `src/**/*.ts`
- Create PR with changes to monitored files

**Workflow actions:**
1. Runs Living README Agent
2. Verifies all setup commands
3. Generates reports
4. Creates PR with updates
5. Uploads reports as artifacts

**Example PR:**
```markdown
## 🤖 Automated README Update

### Changes Detected
- Updated express from ^4.18.2 to ^4.19.0

### Verification Status
- ✅ npm install: Success
- ✅ npm build: Success
- ✅ npm start: Success (port 3000)
```

## End-to-End Test

```bash
# 1. Make a change
echo 'PORT=9000' >> target-app/.env

# 2. Run agent
cd agent && python main.py && cd ..

# 3. Check diff
git diff target-app/README.md

# 4. Review reports
cat bob_sessions/INDEX.md

# 5. Verify change
grep "9000" target-app/README.md
```

**Expected results:**
- ✅ README updated with new port
- ✅ Verification tests pass
- ✅ Reports generated
- ✅ Changes documented

## Customization

**Add monitored files** in `agent/doc_rules.json`:
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

**Customize templates** in `doc_rules.json`:
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

---

**Ready to see it in action? Start with Scenario 1!** 🚀