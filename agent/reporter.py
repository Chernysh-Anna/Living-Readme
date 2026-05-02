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
        """Generate Markdown content from data"""
        md = []
        
        # Header
        md.append("# Living README Agent - Execution Report")
        md.append("")
        md.append(f"**Generated:** {data.get('timestamp', 'N/A')}")
        md.append(f"**Agent Version:** {self.config.get('version', '1.0.0')}")
        md.append("")
        md.append("---")
        md.append("")
        
        # Executive Summary
        md.append("## Executive Summary")
        md.append("")
        sections_updated = data.get('sections_updated', [])
        md.append(f"- **Sections Updated:** {len(sections_updated)}")
        md.append(f"- **Status:** {'✅ Success' if data.get('success', False) else '❌ Failed'}")
        md.append("")
        
        if sections_updated:
            md.append("**Updated Sections:**")
            for section in sections_updated:
                md.append(f"- {section}")
            md.append("")
        
        md.append("---")
        md.append("")
        
        # Changes Detected
        md.append("## Changes Detected")
        md.append("")
        changes = data.get('changes_detected', {})
        
        # Dependencies
        dependencies = changes.get('dependencies', [])
        if dependencies:
            md.append("### Dependencies")
            md.append("")
            md.append("| Package | Version | Category |")
            md.append("|---------|---------|----------|")
            for dep in dependencies:
                md.append(f"| {dep['name']} | {dep['version']} | {dep['category']} |")
            md.append("")
        
        # Environment Variables
        env_vars = changes.get('env_variables', [])
        if env_vars:
            md.append("### Environment Variables")
            md.append("")
            md.append("| Variable | Value | Critical |")
            md.append("|----------|-------|----------|")
            for var in env_vars:
                critical = "✅" if var.get('critical', False) else "❌"
                # Mask sensitive values
                value = var['value'] if len(var['value']) < 20 else f"{var['value'][:10]}..."
                md.append(f"| {var['name']} | `{value}` | {critical} |")
            md.append("")
        
        # Port Configurations
        port_configs = changes.get('port_configs', [])
        if port_configs:
            md.append("### Port Configurations")
            md.append("")
            md.append("| File | Port |")
            md.append("|------|------|")
            for config in port_configs:
                md.append(f"| {config['file']} | {config['port']} |")
            md.append("")
        
        md.append("---")
        md.append("")
        
        # Verification Results
        if 'verification_results' in data:
            md.append("## Verification Results")
            md.append("")
            
            verification = data['verification_results']
            if verification.get('enabled', False):
                summary = verification.get('summary', {})
                md.append(f"- **Total Tests:** {summary.get('total', 0)}")
                md.append(f"- **Passed:** ✅ {summary.get('passed', 0)}")
                md.append(f"- **Failed:** ❌ {summary.get('failed', 0)}")
                md.append(f"- **Skipped:** ⊘ {summary.get('skipped', 0)}")
                md.append("")
                
                # Individual test results
                results = verification.get('results', [])
                if results:
                    md.append("### Test Details")
                    md.append("")
                    for result in results:
                        status = "✅" if result.get('success', False) else "❌"
                        if result.get('skipped', False):
                            status = "⊘"
                        
                        md.append(f"#### {status} {result.get('command', 'Unknown')}")
                        md.append("")
                        
                        if result.get('skipped', False):
                            md.append(f"**Reason:** {result.get('reason', 'N/A')}")
                        else:
                            if result.get('stdout'):
                                md.append("**Output:**")
                                md.append("```")
                                md.append(result['stdout'][:300])  # Truncate
                                md.append("```")
                            
                            if result.get('stderr'):
                                md.append("**Errors:**")
                                md.append("```")
                                md.append(result['stderr'][:300])  # Truncate
                                md.append("```")
                        
                        md.append("")
            else:
                md.append("*Verification was disabled*")
                md.append("")
            
            md.append("---")
            md.append("")
        
        # Diff Preview
        if self.reporting_config.get('include_diff', False) and 'diff' in data:
            md.append("## README Diff Preview")
            md.append("")
            md.append("```diff")
            md.append(data['diff'])
            md.append("```")
            md.append("")
            md.append("---")
            md.append("")
        
        # Metadata
        md.append("## Metadata")
        md.append("")
        md.append(f"- **Configuration File:** `{self.config.get('$schema', 'N/A')}`")
        md.append(f"- **Target App:** `{self.config.get('target_app', {}).get('path', 'N/A')}`")
        md.append(f"- **README Path:** `{self.config.get('readme_management', {}).get('target_readme', 'N/A')}`")
        md.append("")
        
        # Footer
        md.append("---")
        md.append("")
        md.append("*This report was automatically generated by the Living README Agent*")
        md.append("")
        
        return "\n".join(md)
    
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
