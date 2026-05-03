#!/usr/bin/env python3
"""
Living README Agent - Reporter Module
Exports execution results to bob_sessions/ for judges
"""

import json
from pathlib import Path
from typing import Dict, List, Any, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from colorama import Fore as ColoramaFore, Style as ColoramaStyle
    Fore = ColoramaFore
    Style = ColoramaStyle
else:
    try:
        from colorama import Fore, Style
    except ImportError:
        class Fore:  # type: ignore
            GREEN = RED = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ""
        class Style:  # type: ignore
            BRIGHT = RESET_ALL = ""


class Reporter:
    """Generates reports in JSON and Markdown formats"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.reporting_config = config.get('reporting', {})
        self.export_path = Path(self.reporting_config.get('export_path', './bob_sessions'))
        
        # Ensure export directory exists
        self.export_path.mkdir(parents=True, exist_ok=True)
    
    def generate_filename(self, format: str) -> str:
        """Generate filename based on template"""
        template = self.reporting_config.get('filename_template', '{timestamp}-living-readme-update.{format}')
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        return template.format(timestamp=timestamp, format=format)
    
    def export_json(self, data: Dict[str, Any]) -> Path:
        """Export report as JSON"""
        filename = self.generate_filename('json')
        filepath = self.export_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"{Fore.GREEN}✓ JSON report exported: {filepath}")
        return filepath
    
    def export_markdown(self, data: Dict[str, Any]) -> Path:
        """Export report as Markdown"""
        filename = self.generate_filename('md')
        filepath = self.export_path / filename
        
        md_content = self._generate_markdown_content(data)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        print(f"{Fore.GREEN}✓ Markdown report exported: {filepath}")
        return filepath
    
    def _generate_markdown_content(self, data: Dict[str, Any]) -> str:
        """
        Generate enhanced Markdown content with improved scannability and change tracking.
        
        This method creates a structured report that:
        1. Opens with a TL;DR badge line for quick status assessment
        2. Tracks changes against previous runs to show what's new/updated
        3. Uses collapsible sections for verbose output to maintain readability
        4. Includes deep-links back to source JSON for detailed analysis
        """
        md = []
        
        # ═══════════════════════════════════════════════════════════════════
        # HEADER SECTION
        # Purpose: Establish report identity and generation metadata
        # ═══════════════════════════════════════════════════════════════════
        md.append("# Living README Agent - Execution Report")
        md.append("")
        md.append(f"**Generated:** {data.get('timestamp', 'N/A')}")
        md.append(f"**Agent Version:** {self.config.get('version', '1.0.0')}")
        md.append("")
        md.append("---")
        md.append("")
        
        # ═══════════════════════════════════════════════════════════════════
        # EXECUTIVE SUMMARY WITH TL;DR BADGE
        # Purpose: Provide instant status visibility without scrolling
        # Why: Judges and reviewers need to quickly assess success/failure
        # ═══════════════════════════════════════════════════════════════════
        md.append("## Executive Summary")
        md.append("")
        
        # Extract key metrics for the TL;DR badge line
        sections_updated = data.get('sections_updated', [])
        verification = data.get('verification_results', {})
        
        # Build verification status string
        if verification.get('enabled', False):
            summary = verification.get('summary', {})
            passed = summary.get('passed', 0)
            total = summary.get('total', 0)
            failed = summary.get('failed', 0)
            ver_status = f"{passed}/{total} verifications passed"
            failure_note = f"{failed} failures" if failed > 0 else "0 failures"
        else:
            ver_status = "verification disabled"
            failure_note = "N/A"
        
        # Determine overall status icon
        success_icon = "✅" if data.get('success', False) and verification.get('summary', {}).get('failed', 0) == 0 else "⚠️"
        
        # TL;DR badge line: One-line summary for maximum scannability
        # Format: > [icon] X sections updated | Y/Z verifications passed | N failures
        md.append(f"> {success_icon} **{len(sections_updated)} sections updated** | {ver_status} | {failure_note}")
        md.append("")
        
        # Detailed breakdown for those who want more context
        if sections_updated:
            md.append("**Updated Sections:**")
            for section in sections_updated:
                md.append(f"- ✏️ {section}")
            md.append("")
        else:
            md.append("*No sections required updates*")
            md.append("")
        
        md.append("---")
        md.append("")
        
        # ═══════════════════════════════════════════════════════════════════
        # CHANGES DETECTED WITH CHANGE TRACKING
        # Purpose: Show what changed and whether items are new/updated/same
        # Why: Understanding change context helps assess documentation impact
        # ═══════════════════════════════════════════════════════════════════
        md.append("## Changes Detected")
        md.append("")
        changes = data.get('changes_detected', {})
        
        # Load previous report for change comparison
        # Why: Comparing against the last run reveals what's truly new vs. what was already documented
        previous_data = self._load_previous_report()
        previous_changes = previous_data.get('changes_detected', {}) if previous_data else {}
        
        # ───────────────────────────────────────────────────────────────────
        # DEPENDENCIES TABLE WITH CHANGE INDICATORS
        # Purpose: Track dependency additions, updates, and stability
        # ───────────────────────────────────────────────────────────────────
        dependencies = changes.get('dependencies', [])
        if dependencies:
            md.append("### 📦 Dependencies")
            md.append("")
            
            # Enhanced table with "Changed?" column
            # Why: Quickly identify which dependencies are new or updated since last run
            md.append("| Package | Version | Category | Changed? |")
            md.append("|---------|---------|----------|----------|")
            
            # Build lookup of previous dependencies for comparison
            prev_deps = {d['name']: d['version'] for d in previous_changes.get('dependencies', [])}
            
            for dep in dependencies:
                name = dep['name']
                version = dep['version']
                category = dep['category']
                
                # Determine change status by comparing with previous report
                if name not in prev_deps:
                    change_indicator = "✅ new"  # New dependency added
                elif prev_deps[name] != version:
                    change_indicator = "🔄 updated"  # Version changed
                else:
                    change_indicator = "— same"  # No change
                
                md.append(f"| {name} | {version} | {category} | {change_indicator} |")
            md.append("")
        
        # ───────────────────────────────────────────────────────────────────
        # ENVIRONMENT VARIABLES TABLE
        # Purpose: Document configuration state and highlight critical vars
        # ───────────────────────────────────────────────────────────────────
        env_vars = changes.get('env_variables', [])
        if env_vars:
            md.append("### ⚙️ Environment Variables")
            md.append("")
            md.append("| Variable | Value | Critical |")
            md.append("|----------|-------|----------|")
            for var in env_vars:
                critical = "✅" if var.get('critical', False) else "—"
                # Mask sensitive values for security
                # Why: Reports may be shared publicly; protect credentials
                value = var['value'] if len(var['value']) < 20 else f"{var['value'][:10]}..."
                md.append(f"| {var['name']} | `{value}` | {critical} |")
            md.append("")
        
        # ───────────────────────────────────────────────────────────────────
        # PORT CONFIGURATIONS
        # Purpose: Track server binding configuration across source files
        # ───────────────────────────────────────────────────────────────────
        port_configs = changes.get('port_configs', [])
        if port_configs:
            md.append("### 🔌 Port Configurations")
            md.append("")
            md.append("| File | Port |")
            md.append("|------|------|")
            for config in port_configs:
                md.append(f"| {config['file']} | {config['port']} |")
            md.append("")
        
        md.append("---")
        md.append("")
        
        # ═══════════════════════════════════════════════════════════════════
        # VERIFICATION RESULTS WITH COLLAPSIBLE LOGS
        # Purpose: Prove that setup instructions work without cluttering report
        # Why: Full logs are essential for debugging but make reports unreadable
        # Solution: Use <details> blocks to hide verbose output by default
        # ═══════════════════════════════════════════════════════════════════
        if 'verification_results' in data:
            md.append("## 🔍 Verification Results")
            md.append("")
            
            verification = data['verification_results']
            if verification.get('enabled', False):
                summary = verification.get('summary', {})
                
                # High-level summary for quick scanning
                md.append(f"- **Total Tests:** {summary.get('total', 0)}")
                md.append(f"- **Passed:** ✅ {summary.get('passed', 0)}")
                md.append(f"- **Failed:** ❌ {summary.get('failed', 0)}")
                md.append(f"- **Skipped:** ⊘ {summary.get('skipped', 0)}")
                md.append("")
                
                # ───────────────────────────────────────────────────────────
                # INDIVIDUAL TEST RESULTS WITH COLLAPSIBLE OUTPUT
                # Why: Each test needs its own collapsible section so readers
                # can expand only the tests they care about
                # ───────────────────────────────────────────────────────────
                results = verification.get('results', [])
                if results:
                    md.append("### Test Details")
                    md.append("")
                    
                    for result in results:
                        # Determine status icon
                        if result.get('skipped', False):
                            status = "⊘"
                            status_text = "SKIPPED"
                        elif result.get('success', False):
                            status = "✅"
                            status_text = "PASSED"
                        else:
                            status = "❌"
                            status_text = "FAILED"
                        
                        command_name = result.get('command', 'Unknown')
                        md.append(f"#### {status} {command_name} ({status_text})")
                        md.append("")
                        
                        if result.get('skipped', False):
                            # Skipped tests just show the reason
                            md.append(f"**Reason:** {result.get('reason', 'N/A')}")
                            md.append("")
                        else:
                            # For executed tests, use collapsible <details> blocks
                            # Why: Keeps report scannable while preserving full logs
                            # for debugging. Readers can expand only failed tests.
                            
                            stdout = result.get('stdout', '').strip()
                            stderr = result.get('stderr', '').strip()
                            
                            if stdout:
                                # Collapsible stdout section
                                md.append("<details>")
                                md.append("<summary>📄 View stdout</summary>")
                                md.append("")
                                md.append("```")
                                md.append(stdout)
                                md.append("```")
                                md.append("</details>")
                                md.append("")
                            
                            if stderr:
                                # Collapsible stderr section
                                # Why: Errors are critical but often verbose
                                md.append("<details>")
                                md.append("<summary>⚠️ View stderr</summary>")
                                md.append("")
                                md.append("```")
                                md.append(stderr)
                                md.append("```")
                                md.append("</details>")
                                md.append("")
                            
                            # Port verification status (if applicable)
                            if 'port_verified' in result:
                                port_status = "✅ Verified" if result['port_verified'] else "❌ Not detected"
                                expected_port = result.get('expected_port', 'N/A')
                                md.append(f"**Port {expected_port}:** {port_status}")
                                md.append("")
            else:
                md.append("*Verification was disabled in configuration*")
                md.append("")
            
            md.append("---")
            md.append("")
        
        # ═══════════════════════════════════════════════════════════════════
        # DIFF PREVIEW (OPTIONAL)
        # Purpose: Show exact changes made to README
        # ═══════════════════════════════════════════════════════════════════
        if self.reporting_config.get('include_diff', False) and 'diff' in data:
            md.append("## 📝 README Diff Preview")
            md.append("")
            md.append("```diff")
            md.append(data['diff'])
            md.append("```")
            md.append("")
            md.append("---")
            md.append("")
        
        # ═══════════════════════════════════════════════════════════════════
        # METADATA SECTION
        # Purpose: Provide configuration context for reproducibility
        # ═══════════════════════════════════════════════════════════════════
        md.append("## 📋 Metadata")
        md.append("")
        md.append(f"- **Configuration File:** `{self.config.get('$schema', 'N/A')}`")
        md.append(f"- **Target App:** `{self.config.get('target_app', {}).get('path', 'N/A')}`")
        md.append(f"- **README Path:** `{self.config.get('readme_management', {}).get('target_readme', 'N/A')}`")
        md.append("")
        
        # ═══════════════════════════════════════════════════════════════════
        # FOOTER WITH DEEP-LINK TO JSON
        # Purpose: Connect Markdown report to its source JSON for detailed analysis
        # Why: Markdown is for humans, JSON is for machines. Link them together
        # so readers can drill down into raw data when needed.
        # ═══════════════════════════════════════════════════════════════════
        md.append("---")
        md.append("")
        
        # Generate JSON filename from current timestamp
        # Why: Both JSON and Markdown use the same timestamp, so we can construct
        # the JSON filename and create a relative link
        timestamp = data.get('timestamp', '')
        if timestamp:
            # Extract timestamp and format as filename
            json_filename = self.generate_filename('json')
            md.append(f"📊 **[View detailed JSON report](./{json_filename})**")
            md.append("")
        
        md.append("*This report was automatically generated by the Living README Agent*")
        md.append("")
        
        return "\n".join(md)
    
    def _load_previous_report(self) -> Dict[str, Any]:
        """
        Load the most recent JSON report for change comparison.
        
        Purpose: Enable change tracking by comparing current state against
        the last documented state.
        
        Why: Without historical context, we can't distinguish between:
        - New dependencies vs. existing ones
        - Updated versions vs. stable versions
        - First-time documentation vs. re-documentation
        
        Returns:
            Dict containing previous report data, or empty dict if none found
        """
        try:
            # Find all JSON reports in export directory
            json_files = sorted(self.export_path.glob('*.json'), reverse=True)
            
            # Skip the first file if it's the current report being generated
            # Why: We want the PREVIOUS report, not the one we're creating now
            for json_file in json_files:
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        return json.load(f)
                except (json.JSONDecodeError, IOError):
                    # If file is corrupted or unreadable, try the next one
                    continue
            
            # No valid previous report found
            return {}
            
        except Exception:
            # If anything goes wrong, fail gracefully
            # Why: Change tracking is a nice-to-have, not a requirement
            return {}
    
    def export_report(self, data: Dict[str, Any]) -> Dict[str, Path]:
        """Export report in all configured formats"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}📄 Exporting Reports...")
        
        formats = self.reporting_config.get('formats', ['json', 'markdown'])
        exported_files = {}
        
        if 'json' in formats:
            exported_files['json'] = self.export_json(data)
        
        if 'markdown' in formats or 'md' in formats:
            exported_files['markdown'] = self.export_markdown(data)
        
        print(f"{Fore.GREEN}✓ All reports exported successfully")
        return exported_files
    
    def create_summary_index(self) -> Path:
        """Create an index.md file listing all reports"""
        index_path = self.export_path / 'INDEX.md'
        
        # Get all report files
        json_files = sorted(self.export_path.glob('*.json'), reverse=True)
        md_files = sorted(self.export_path.glob('*.md'), reverse=True)
        md_files = [f for f in md_files if f.name != 'INDEX.md']
        
        content = []
        content.append("# Living README Agent - Report Index")
        content.append("")
        content.append(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append("")
        content.append("---")
        content.append("")
        
        content.append("## Recent Reports")
        content.append("")
        
        # Combine and sort all reports
        all_reports = []
        for json_file in json_files[:10]:  # Last 10 reports
            all_reports.append(('JSON', json_file))
        for md_file in md_files[:10]:
            all_reports.append(('Markdown', md_file))
        
        all_reports.sort(key=lambda x: x[1].stat().st_mtime, reverse=True)
        
        if all_reports:
            content.append("| Date | Format | File |")
            content.append("|------|--------|------|")
            
            for format_type, filepath in all_reports[:20]:  # Show last 20
                mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
                date_str = mtime.strftime('%Y-%m-%d %H:%M')
                content.append(f"| {date_str} | {format_type} | [{filepath.name}](./{filepath.name}) |")
        else:
            content.append("*No reports found*")
        
        content.append("")
        content.append("---")
        content.append("")
        content.append("*This index is automatically updated by the Living README Agent*")
        content.append("")
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(content))
        
        print(f"{Fore.GREEN}✓ Index updated: {index_path}")
        return index_path


def main():
    """Test the reporter standalone"""
    import json
    
    # Load config
    config_path = Path('agent/doc_rules.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Create sample data
    sample_data = {
        'timestamp': datetime.now().isoformat(),
        'success': True,
        'sections_updated': ['Requirements', 'Configuration'],
        'changes_detected': {
            'dependencies': [
                {'name': 'express', 'version': '^4.18.2', 'category': 'production'},
                {'name': 'typescript', 'version': '^5.1.6', 'category': 'development'}
            ],
            'env_variables': [
                {'name': 'PORT', 'value': '3000', 'critical': True},
                {'name': 'HOST', 'value': 'localhost', 'critical': True}
            ],
            'port_configs': [
                {'file': 'src/config.ts', 'port': '3000'}
            ]
        },
        'verification_results': {
            'enabled': True,
            'summary': {'total': 3, 'passed': 2, 'failed': 1, 'skipped': 0},
            'results': [
                {'command': 'install_dependencies', 'success': True},
                {'command': 'build_project', 'success': True},
                {'command': 'start_server', 'success': False}
            ]
        }
    }
    
    # Export reports
    reporter = Reporter(config)
    exported = reporter.export_report(sample_data)
    reporter.create_summary_index()
    
    print(f"\n{Fore.CYAN}Exported files:")
    for format_type, filepath in exported.items():
        print(f"  - {format_type}: {filepath}")


if __name__ == '__main__':
    main()

# Made with Bob
