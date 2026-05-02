# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project-Specific Patterns

### Python Agent Architecture
- Agent modules (`watcher.py`, `verifier.py`, `reporter.py`) must be imported in `main.py` - they're designed as standalone modules but orchestrated centrally
- All Python modules use `TYPE_CHECKING` for colorama imports - type checkers see correct types, runtime has fallback
- `watcher.py` contains THREE separate classes (ChangeDetector, ReadmeParser, ReadmeGenerator) - not one monolithic class
- `main.py` uses `Path(__file__).parent.parent` to define project root - all paths in doc_rules.json are resolved relative to this root
- Path resolution happens in `resolve_paths()` method - converts relative paths (./target-app) to absolute paths based on project root

### README Management System
- README sections MUST use exact marker format: `<!-- MANAGED_SECTION:START:SectionName -->` and `<!-- MANAGED_SECTION:END:SectionName -->`
- Section names in markers must match `doc_rules.json` "managed_sections" array exactly (case-sensitive)
- Content between markers is replaced entirely - no merging or partial updates
- Sections outside markers are preserved - this is intentional for human-written content

### Configuration Schema
- `doc_rules.json` uses nested "monitoring.files" array where each file has different watch patterns
- Port detection uses regex patterns in "watch_patterns" - not simple string matching
- "change_types": ["major", "minor"] means patch versions (x.x.X) are intentionally ignored
- Verification commands run sequentially with dependency - if install fails, build is skipped

### Verification System
- Commands in `verifier.py` use `shell=True` for Windows compatibility - don't change to shell=False
- Port checking uses socket connection attempt, not process inspection
- Server verification expects timeout/failure - uses `continue-on-error` pattern
- Working directory for commands is relative to project root, not agent/ directory

### Report Generation
- Reports use timestamp in filename format: `YYYY-MM-DD-HH-MM-SS-living-readme-update.{format}`
- Both JSON and Markdown are generated from same data structure - don't create separate data
- INDEX.md is auto-generated and should list reports in reverse chronological order
- Report paths in `doc_rules.json` are relative to project root, not agent/

### Target App Structure
- TypeScript config uses "rootDir": "./src" and "outDir": "./dist" - source must be in src/
- Config loading in `config.ts` uses `path.join(__dirname, '..', '.env')` - .env is one level up from dist/
- Server class in `server.ts` is instantiated, not used as static - must call `new Server()` then `.start()`

## Critical Gotchas

- Python modules use relative imports in main.py but are designed to run standalone for testing
- README markers are parsed with regex - special characters in section names will break parsing
- Verification timeout in `doc_rules.json` is in seconds, not milliseconds
- GitHub Actions workflow expects reports in `bob_sessions/` at project root, not `agent/bob_sessions/`
- Target app's package.json "main" points to "dist/index.js" - must build before running with `npm start`

## Critical Gotchas (Continued)

- All file operations use `encoding='utf-8'` explicitly - required for Windows compatibility
- Without explicit encoding, Windows defaults to cp1252 causing UnicodeDecodeError on JSON files

## Testing

- Run agent standalone: `cd agent && python main.py` (must be in agent/ directory)
- Test individual modules: `python watcher.py`, `python verifier.py`, `python reporter.py`
- Target app requires: `cd target-app && npm install && npm run build` before `npm start`
- Demo scripts handle all setup - use `run_demo.sh` or `run_demo.bat` for full workflow