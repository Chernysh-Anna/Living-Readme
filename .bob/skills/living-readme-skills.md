# Living README Bob Skills

This document defines three reusable skills that can be invoked in any Bob conversation to interact with the Living README Agent's Python modules.

---

## SKILL: run-agent

### Description
Triggers a full agent execution cycle, running change detection, verification, and reporting phases.

### Invocation
```
Use skill: run-agent
```

### Steps Bob Must Follow

#### Step 1: Confirm Working Directory
```
Verify current working directory is the project root (d:/Living-Readme).
If not in project root, navigate to it before proceeding.
```

#### Step 2: Execute Agent
```
Run command: cd agent && python main.py

Expected behavior:
- Agent will run three phases: Detection, Verification, Reporting
- Output will be colorized with status indicators
- Process may take 30-60 seconds depending on verification steps
```

#### Step 3: Parse Section Updates
```
Scan stdout for lines matching pattern: "✓ Updated section: {section_name}"

Extract and list all updated sections:
- Requirements
- Installation
- Configuration
- Running

If no sections updated, report: "No sections required updates"
```

#### Step 4: Parse Report Exports
```
Scan stdout for lines matching pattern: "- {format}: {filepath}"

Extract and list all exported report files:
- JSON report path
- Markdown report path

Example output format:
Exported Reports:
- JSON: bob_sessions/2026-05-03-10-30-00-living-readme-update.json
- Markdown: bob_sessions/2026-05-03-10-30-00-living-readme-update.md
```

#### Step 5: Summarize Pass/Fail
```
Parse verification summary section for:
- Tests Passed: X/Y

Generate one-sentence summary:
- If all passed: "Agent execution successful: all {Y} verification tests passed."
- If some failed: "Agent execution completed with {failed} of {total} verification tests failing."
- If verification disabled: "Agent execution successful: verification was disabled."
```

### Example Output

```
Running Living README Agent...

Working directory: d:/Living-Readme ✓
Executing: cd agent && python main.py

Agent Output:
🤖 LIVING README AGENT
Autonomous Documentation Maintenance System
═══════════════════════════════════════════

📍 PHASE 1: Change Detection
─────────────────────────────────────────
🔍 Scanning for changes...
✓ Found 13 configuration items
✓ Parsed 4 managed sections
✓ Updated section: Configuration
✓ Updated section: Running

📍 PHASE 2: Behavioral Verification
─────────────────────────────────────────
✓ npm install succeeded
✓ npm build succeeded
✓ Server listening on port 3000

📍 PHASE 3: Report Generation
─────────────────────────────────────────
✓ Exported JSON report
✓ Exported Markdown report

═══════════════════════════════════════════
✅ EXECUTION COMPLETE
═══════════════════════════════════════════

Sections Updated:
- Configuration
- Running

Exported Reports:
- JSON: bob_sessions/2026-05-03-10-30-00-living-readme-update.json
- Markdown: bob_sessions/2026-05-03-10-30-00-living-readme-update.md

Summary: Agent execution successful: all 3 verification tests passed.
```

### Error Handling

If execution fails:
1. Capture stderr output
2. Identify failure phase (Detection/Verification/Reporting)
3. Report specific error with line number if available
4. Suggest remediation based on error type:
   - Import errors → Check Python dependencies
   - File not found → Verify paths in doc_rules.json
   - Permission errors → Check file permissions
   - JSON decode errors → Validate doc_rules.json syntax

---

## SKILL: check-drift

### Description
Non-destructive drift check that detects what WOULD change without writing anything. Compares current codebase state against the last agent_runs snapshot.

### Invocation
```
Use skill: check-drift
```

### Steps Bob Must Follow

#### Step 1: Load Latest Snapshot
```
1. Read bob_sessions/INDEX.md to find the most recent JSON report
2. Load the JSON report file
3. Extract baseline values:
   - changes_detected.dependencies[]
   - changes_detected.env_variables[]
   - changes_detected.port_configs[]
4. Store as baseline_state
```

#### Step 2: Detect Current State
```
1. Read agent/doc_rules.json for configuration
2. Scan target-app/package.json for current dependencies
3. Scan target-app/.env for current environment variables
4. Scan target-app/src/**/*.ts for current port configurations
5. Store as current_state

Use the same detection logic as ChangeDetector in watcher.py:
- Dependencies: Read from package.json dependencies and devDependencies
- Env vars: Parse .env file for KEY=VALUE pairs
- Ports: Regex search for port:\s*(\d+), listen\((\d+)\), PORT\s*=\s*(\d+)
```

#### Step 3: Compare States
```
For each monitored item, compare baseline vs current:

Dependencies:
- Match by package name
- Compare versions
- Flag: ADDED, REMOVED, CHANGED, UNCHANGED

Environment Variables:
- Match by variable name
- Compare values
- Flag critical variables (PORT, HOST, NODE_ENV)
- Status: ADDED, REMOVED, CHANGED, UNCHANGED

Port Configurations:
- Match by file path
- Compare port numbers
- Status: CHANGED, UNCHANGED
```

#### Step 4: Map to README Sections
```
Determine which managed sections would be affected:

Dependencies change → Requirements section
Env variables change → Configuration section
Port change → Configuration + Running sections

For each affected section:
- Read current content from target-app/README.md
- Identify specific lines that would change
- Calculate diff size (lines added/removed)
```

#### Step 5: Generate Drift Report
```
Output a color-coded table with the following format:

| Section       | Item              | Current Value | Documented Value | Status    |
|---------------|-------------------|---------------|------------------|-----------|
| Requirements  | express           | ^4.19.0       | ^4.18.2          | 🔴 DRIFT  |
| Requirements  | typescript        | 5.1.6         | 5.1.6            | 🟢 SYNCED |
| Configuration | PORT              | 8080          | 3000             | 🔴 DRIFT  |
| Configuration | NODE_ENV          | development   | development      | 🟢 SYNCED |
| Running       | Server Port       | 8080          | 3000             | 🔴 DRIFT  |

Color codes:
🔴 DRIFT - Values don't match, update needed
🟢 SYNCED - Values match, no action needed
🟡 ADDED - New item not in documentation
⚫ REMOVED - Item in docs but not in code

Summary:
- Total items checked: 15
- In sync: 12
- Drifted: 3
- Sections requiring updates: 2 (Configuration, Running)
```

### Example Output

```
Checking for documentation drift...

Loading baseline from latest report:
File: bob_sessions/2026-05-02-17-59-11-living-readme-update.json
Timestamp: 2026-05-02T17:59:11Z

Scanning current codebase state:
- target-app/package.json: 7 dependencies
- target-app/.env: 6 environment variables
- target-app/src/**/*.ts: 1 port configuration

Comparing states...

DRIFT ANALYSIS:

| Section       | Item              | Current Value | Documented Value | Status    |
|---------------|-------------------|---------------|------------------|-----------|
| Requirements  | express           | ^4.18.2       | ^4.18.2          | 🟢 SYNCED |
| Requirements  | dotenv            | ^16.0.3       | ^16.0.3          | 🟢 SYNCED |
| Requirements  | cors              | ^2.8.5        | ^2.8.5           | 🟢 SYNCED |
| Requirements  | typescript        | 5.1.6         | 5.1.6            | 🟢 SYNCED |
| Configuration | NODE_ENV          | development   | development      | 🟢 SYNCED |
| Configuration | PORT              | 3000          | 3000             | 🟢 SYNCED |
| Configuration | HOST              | localhost     | localhost        | 🟢 SYNCED |
| Configuration | DB_HOST           | localhost     | localhost        | 🟢 SYNCED |
| Configuration | DB_PORT           | 5432          | 5432             | 🟢 SYNCED |
| Configuration | DB_NAME           | testdb        | testdb           | 🟢 SYNCED |
| Running       | Server Port       | 3000          | 3000             | 🟢 SYNCED |

SUMMARY:
✓ All 11 items are in sync
✓ No documentation updates required
✓ Last sync: 2026-05-02T17:59:11Z (1 day ago)

Recommendation: No action needed. Documentation is current.
```

### Example Output (With Drift)

```
Checking for documentation drift...

Loading baseline from latest report:
File: bob_sessions/2026-05-02-17-59-11-living-readme-update.json
Timestamp: 2026-05-02T17:59:11Z

Scanning current codebase state:
- target-app/package.json: 7 dependencies
- target-app/.env: 6 environment variables
- target-app/src/**/*.ts: 1 port configuration

Comparing states...

DRIFT ANALYSIS:

| Section       | Item              | Current Value | Documented Value | Status    |
|---------------|-------------------|---------------|------------------|-----------|
| Requirements  | express           | ^4.19.0       | ^4.18.2          | 🔴 DRIFT  |
| Requirements  | dotenv            | ^16.0.3       | ^16.0.3          | 🟢 SYNCED |
| Requirements  | cors              | ^2.8.5        | ^2.8.5           | 🟢 SYNCED |
| Requirements  | typescript        | 5.1.6         | 5.1.6            | 🟢 SYNCED |
| Configuration | NODE_ENV          | development   | development      | 🟢 SYNCED |
| Configuration | PORT              | 8080          | 3000             | 🔴 DRIFT  |
| Configuration | HOST              | localhost     | localhost        | 🟢 SYNCED |
| Configuration | DB_HOST           | localhost     | localhost        | 🟢 SYNCED |
| Configuration | DB_PORT           | 5432          | 5432             | 🟢 SYNCED |
| Configuration | DB_NAME           | testdb        | testdb           | 🟢 SYNCED |
| Running       | Server Port       | 8080          | 3000             | 🔴 DRIFT  |

SUMMARY:
⚠️ 3 of 11 items have drifted
⚠️ 2 sections require updates: Requirements, Configuration, Running
⚠️ Last sync: 2026-05-02T17:59:11Z (1 day ago)

CRITICAL DRIFT DETECTED:
- PORT changed from 3000 → 8080 (affects Configuration + Running sections)

Recommendation: Run 'run-agent' skill to update documentation.
```

---

## SKILL: export-session

### Description
Package the current Bob conversation plus all bob_sessions/ reports into a single ZIP file for hackathon submission.

### Invocation
```
Use skill: export-session
```

### Steps Bob Must Follow

#### Step 1: Create Session Markdown
```
1. Generate timestamp in format: YYYY-MM-DD-HH-MM-SS
2. Create filename: bob_sessions/bob_ide_sessions/<timestamp>-session.md
3. Write conversation history to file with structure:

# Bob IDE Session - <timestamp>

## Session Metadata
- **Date:** <ISO 8601 timestamp>
- **Mode:** <current mode>
- **Task:** <original user request>
- **Duration:** <calculated from start to now>

## Conversation History

### User Message 1
<user message content>

### Bob Response 1
<bob response content>

### User Message 2
<user message content>

### Bob Response 2
<bob response content>

[... continue for all messages ...]

## Session Summary
- **Total Messages:** <count>
- **Tools Used:** <list of tools used>
- **Files Modified:** <list of files created/modified>
- **Outcome:** <success/partial/failed>

---
*Generated by Living README Agent*
```

#### Step 2: Regenerate INDEX.md
```
1. Scan bob_sessions/ directory for all report files
2. Group by timestamp (JSON + Markdown pairs)
3. Sort by timestamp descending (newest first)
4. Generate INDEX.md with structure:

# Living README Agent - Report Index

**Last Updated:** <current timestamp>

---

## Recent Reports

| Date | Format | File |
|------|--------|------|
| <date> | Markdown | [<filename>](./<filename>) |
| <date> | JSON | [<filename>](./<filename>) |
[... continue for all reports ...]

---

*This index is automatically updated by the Living README Agent*

5. Write to bob_sessions/INDEX.md
```

#### Step 3: Create ZIP Archive
```
1. Generate timestamp: YYYY-MM-DD-HH-MM-SS
2. Create ZIP filename: submission-<timestamp>.zip
3. Add to ZIP:
   - bob_sessions/*.json (all JSON reports)
   - bob_sessions/*.md (all Markdown reports)
   - bob_sessions/INDEX.md
   - bob_sessions/bob_ide_sessions/*.md (all IDE session logs)
4. Save ZIP to project root: d:/Living-Readme/submission-<timestamp>.zip

Use Python zipfile module or system zip command:
python -c "import zipfile, pathlib; z = zipfile.ZipFile('submission-<timestamp>.zip', 'w'); [z.write(f, f.relative_to('.')) for f in pathlib.Path('bob_sessions').rglob('*') if f.is_file()]; z.close()"
```

#### Step 4: Generate Summary Report
```
Print summary with:
1. ZIP file path (absolute)
2. ZIP file size (in MB)
3. File count breakdown:
   - JSON reports: <count>
   - Markdown reports: <count>
   - IDE sessions: <count>
   - Total files: <count>
4. Date range of reports (oldest to newest)
5. Verification: ZIP integrity check
```

### Example Output

```
Exporting session for hackathon submission...

Step 1: Creating session markdown
Writing conversation history...
Created: bob_sessions/bob_ide_sessions/2026-05-03-10-45-30-session.md
- Messages captured: 12
- Tools used: read_file, write_to_file, execute_command
- Files modified: 3

Step 2: Regenerating INDEX.md
Scanning bob_sessions/ directory...
Found 18 report files (9 JSON + 9 Markdown)
Updated: bob_sessions/INDEX.md

Step 3: Creating ZIP archive
Packaging files...
- Adding JSON reports: 9 files
- Adding Markdown reports: 9 files
- Adding IDE sessions: 6 files
- Adding INDEX.md: 1 file
Created: d:/Living-Readme/submission-2026-05-03-10-45-30.zip

Step 4: Summary Report

📦 EXPORT COMPLETE

ZIP File: d:/Living-Readme/submission-2026-05-03-10-45-30.zip
Size: 2.4 MB
Integrity: ✓ Verified

File Breakdown:
- JSON reports: 9
- Markdown reports: 9
- IDE sessions: 6
- INDEX.md: 1
─────────────────
Total files: 25

Report Date Range:
- Oldest: 2026-05-02 09:00:00
- Newest: 2026-05-03 10:45:30
- Span: 1 day, 1 hour, 45 minutes

✓ Ready for hackathon submission
```

### Error Handling

If export fails:
1. Check write permissions on project root
2. Verify bob_sessions/ directory exists and is readable
3. Ensure sufficient disk space for ZIP creation
4. If ZIP creation fails, provide manual instructions:
   ```
   Manual export steps:
   1. Navigate to project root
   2. Run: zip -r submission.zip bob_sessions/
   3. Verify: unzip -l submission.zip
   ```

---

## Usage Guidelines

### Invoking Skills

Skills can be invoked in any Bob conversation using natural language:

```
"Use the run-agent skill"
"Check for drift using check-drift"
"Export this session"
"Run skill: run-agent"
```

### Skill Chaining

Skills can be chained for comprehensive workflows:

```
1. "Check drift" → Identify what needs updating
2. "Run agent" → Apply updates
3. "Export session" → Package for submission
```

### When to Use Each Skill

**run-agent:**
- After making changes to target-app/
- Before creating a pull request
- To verify documentation is current
- As part of CI/CD pipeline

**check-drift:**
- Before running the agent (preview changes)
- During code review (assess documentation impact)
- For periodic audits (weekly/monthly checks)
- When investigating documentation bugs

**export-session:**
- At end of development session
- Before hackathon submission deadline
- For archival/audit purposes
- When sharing work with team

---

## Implementation Notes

### Python Integration

Skills interact with Python modules using:
- `execute_command` tool for running Python scripts
- `read_file` tool for loading JSON reports
- `write_to_file` tool for creating session logs
- Standard output parsing for extracting results

### Error Recovery

All skills include error handling:
- Graceful degradation if files missing
- Clear error messages with remediation steps
- Fallback to manual instructions when automation fails
- Validation of outputs before reporting success

### Performance Considerations

- **run-agent:** 30-60 seconds (includes verification)
- **check-drift:** 2-5 seconds (read-only operations)
- **export-session:** 5-10 seconds (depends on file count)

---

*Last Updated: 2026-05-03*
*Version: 1.0.0*