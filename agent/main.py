#!/usr/bin/env python3
"""
Living README Agent - Main Orchestrator
Coordinates all components to maintain synchronized documentation
"""

import sys
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, TYPE_CHECKING
from datetime import datetime

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from watcher import LivingReadmeAgent
from verifier import CommandVerifier
from reporter import Reporter

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


class LivingReadmeOrchestrator:
    """Main orchestrator that coordinates all agent components"""
    
    def __init__(self, config_path: Optional[str] = None):
        # Define project root as parent of agent/ directory
        self.project_root = Path(__file__).parent.parent
        
        if config_path is None:
            # Config is in agent/ directory
            self.config_path = Path(__file__).parent / 'doc_rules.json'
        else:
            self.config_path = Path(config_path)
        
        self.config = self.load_config()
        self.resolve_paths()
        
        # Initialize components with resolved config
        self.agent = LivingReadmeAgent(config=self.config)
        self.verifier = CommandVerifier(self.config)
        self.reporter = Reporter(self.config)
        
        self.execution_data: Dict[str, Any] = {}
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from doc_rules.json"""
        try:
            if not self.config_path.exists():
                print(f"{Fore.RED}❌ Configuration file not found: {self.config_path}")
                sys.exit(1)
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"{Fore.RED}❌ Invalid JSON in configuration file: {e}")
            sys.exit(1)
        except PermissionError as e:
            print(f"{Fore.RED}❌ Permission denied reading configuration: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"{Fore.RED}❌ Error loading configuration: {e}")
            sys.exit(1)
    
    def resolve_paths(self) -> None:
        """Resolve all relative paths in config to absolute paths based on project root"""
        # Resolve target_app path
        if 'target_app' in self.config and 'path' in self.config['target_app']:
            target_path = self.config['target_app']['path']
            if target_path.startswith('./') or target_path.startswith('.\\'):
                target_path = target_path[2:]
            self.config['target_app']['path'] = str(self.project_root / target_path)
        
        # Resolve README paths
        if 'readme_management' in self.config:
            for key in ['target_readme', 'root_readme']:
                if key in self.config['readme_management']:
                    readme_path = self.config['readme_management'][key]
                    if readme_path.startswith('./') or readme_path.startswith('.\\'):
                        readme_path = readme_path[2:]
                    self.config['readme_management'][key] = str(self.project_root / readme_path)
        
        # Resolve reporting export path
        if 'reporting' in self.config and 'export_path' in self.config['reporting']:
            export_path = self.config['reporting']['export_path']
            if export_path.startswith('./') or export_path.startswith('.\\'):
                export_path = export_path[2:]
            self.config['reporting']['export_path'] = str(self.project_root / export_path)
        
        # Resolve verification working directories
        if 'verification' in self.config and 'commands' in self.config['verification']:
            for cmd in self.config['verification']['commands']:
                if 'working_dir' in cmd:
                    work_dir = cmd['working_dir']
                    if work_dir.startswith('./') or work_dir.startswith('.\\'):
                        work_dir = work_dir[2:]
                    cmd['working_dir'] = str(self.project_root / work_dir)
    
    def print_banner(self):
        """Print startup banner"""
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{'=' * 70}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'  🤖 LIVING README AGENT':^70}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'  Autonomous Documentation Maintenance System':^70}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'=' * 70}\n")
        print(f"{Fore.CYAN}Version: {self.config.get('version', '1.0.0')}")
        print(f"{Fore.CYAN}Target: {self.config['target_app']['path']}")
        print(f"{Fore.CYAN}README: {self.config['readme_management']['target_readme']}")
        print(f"{Fore.CYAN}Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{'=' * 70}\n")
    
    def run_detection_phase(self) -> Dict[str, Any]:
        """Phase 1: Detect changes in target application"""
        print(f"{Fore.CYAN}{Style.BRIGHT}📍 PHASE 1: Change Detection")
        print(f"{Fore.CYAN}{'─' * 70}\n")
        
        result = self.agent.run()
        
        print(f"\n{Fore.GREEN}✓ Detection phase complete")
        return result
    
    def run_verification_phase(self) -> Dict[str, Any]:
        """Phase 2: Verify setup commands work"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}📍 PHASE 2: Behavioral Verification")
        print(f"{Fore.CYAN}{'─' * 70}\n")
        
        if not self.config['verification'].get('enabled', False):
            print(f"{Fore.YELLOW}⚠️  Verification disabled in configuration")
            return {'enabled': False, 'results': []}
        
        verification_results = self.verifier.run_all_verifications()
        
        print(f"\n{Fore.GREEN}✓ Verification phase complete")
        return verification_results
    
    def run_reporting_phase(self, detection_data: Dict[str, Any], 
                           verification_data: Dict[str, Any]) -> Dict[str, Path]:
        """Phase 3: Generate and export reports"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}📍 PHASE 3: Report Generation")
        print(f"{Fore.CYAN}{'─' * 70}\n")
        
        # Combine all data
        report_data = {
            **detection_data,
            'verification_results': verification_data,
            'config_version': self.config.get('version', '1.0.0'),
            'agent_info': {
                'name': 'Living README Agent',
                'description': 'Autonomous Documentation Maintenance System',
                'target_app': self.config['target_app']['path']
            }
        }
        
        # Export reports
        exported_files = self.reporter.export_report(report_data)
        
        # Update index
        self.reporter.create_summary_index()
        
        print(f"\n{Fore.GREEN}✓ Reporting phase complete")
        return exported_files
    
    def generate_pr_summary(self, detection_data: Dict[str, Any], 
                           verification_data: Dict[str, Any]) -> str:
        """Generate PR description summary"""
        summary = []
        
        summary.append("## 📝 Living README Agent Update\n")
        
        # Changes summary
        changes = detection_data.get('changes_detected', {})
        total_changes = sum(len(v) for v in changes.values())
        
        summary.append(f"**Total Changes Detected:** {total_changes}\n")
        
        # Sections updated
        sections = detection_data.get('sections_updated', [])
        if sections:
            summary.append("**Sections Updated:**")
            for section in sections:
                summary.append(f"- ✅ {section}")
            summary.append("")
        
        # Verification summary
        if verification_data.get('enabled', False):
            ver_summary = verification_data.get('summary', {})
            summary.append("**Verification Results:**")
            summary.append(f"- ✅ Passed: {ver_summary.get('passed', 0)}")
            summary.append(f"- ❌ Failed: {ver_summary.get('failed', 0)}")
            summary.append(f"- ⊘ Skipped: {ver_summary.get('skipped', 0)}")
            summary.append("")
        
        # Change details
        if changes.get('dependencies'):
            summary.append("### 📦 Dependencies")
            for dep in changes['dependencies'][:5]:  # Show first 5
                summary.append(f"- `{dep['name']}`: {dep['version']}")
            if len(changes['dependencies']) > 5:
                summary.append(f"- *...and {len(changes['dependencies']) - 5} more*")
            summary.append("")
        
        if changes.get('env_variables'):
            summary.append("### ⚙️ Environment Variables")
            critical = [v for v in changes['env_variables'] if v.get('critical')]
            if critical:
                summary.append("**Critical:**")
                for var in critical:
                    summary.append(f"- `{var['name']}`: {var['value']}")
            summary.append("")
        
        summary.append("---")
        summary.append("*This update was automatically generated by the Living README Agent*")
        
        return "\n".join(summary)
    
    def execute(self) -> int:
        """Main execution flow"""
        try:
            self.print_banner()
            
            # Phase 1: Detection
            detection_result = self.run_detection_phase()
            
            if not detection_result.get('success', False):
                print(f"\n{Fore.YELLOW}⚠️  No changes detected or update failed")
                return 0
            
            # Phase 2: Verification
            verification_result = self.run_verification_phase()
            
            # Phase 3: Reporting
            exported_files = self.run_reporting_phase(
                detection_result,
                verification_result
            )
            
            # Generate PR summary
            pr_summary = self.generate_pr_summary(
                detection_result,
                verification_result
            )
            
            # Print final summary
            print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{'=' * 70}")
            print(f"{Fore.MAGENTA}{Style.BRIGHT}{'  ✅ EXECUTION COMPLETE':^70}")
            print(f"{Fore.MAGENTA}{Style.BRIGHT}{'=' * 70}\n")
            
            print(f"{Fore.GREEN}📊 Summary:")
            print(f"{Fore.GREEN}  - Sections Updated: {len(detection_result.get('sections_updated', []))}")
            print(f"{Fore.GREEN}  - Reports Generated: {len(exported_files)}")
            
            if verification_result.get('enabled', False):
                ver_summary = verification_result.get('summary', {})
                print(f"{Fore.GREEN}  - Tests Passed: {ver_summary.get('passed', 0)}/{ver_summary.get('total', 0)}")
            
            print(f"\n{Fore.CYAN}📁 Exported Files:")
            for format_type, filepath in exported_files.items():
                print(f"{Fore.CYAN}  - {format_type}: {filepath}")
            
            print(f"\n{Fore.MAGENTA}{'─' * 70}")
            print(f"\n{Fore.YELLOW}📋 PR Summary (copy this for PR description):")
            print(f"{Fore.WHITE}{pr_summary}")
            print(f"\n{Fore.MAGENTA}{'─' * 70}\n")
            
            return 0
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}⚠️  Execution interrupted by user")
            return 130
            
        except Exception as e:
            print(f"\n{Fore.RED}❌ Fatal Error: {str(e)}")
            import traceback
            traceback.print_exc()
            return 1


def main():
    """Entry point"""
    orchestrator = LivingReadmeOrchestrator()
    exit_code = orchestrator.execute()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()

# Made with Bob
