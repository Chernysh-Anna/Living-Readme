#!/usr/bin/env python3
"""
Living README Agent - Watcher Module
Monitors target application for changes and triggers README updates
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, TYPE_CHECKING
from datetime import datetime
import subprocess

# Add colorama for better console output
if TYPE_CHECKING:
    from colorama import Fore as ColoramaFore, Style as ColoramaStyle
    Fore = ColoramaFore
    Style = ColoramaStyle
else:
    try:
        from colorama import init, Fore, Style
        init(autoreset=True)
    except ImportError:
        # Fallback if colorama not installed
        class Fore:  # type: ignore
            GREEN = RED = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ""
        class Style:  # type: ignore
            BRIGHT = RESET_ALL = ""


class ChangeDetector:
    """Detects changes in target application files"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.target_path = Path(config['target_app']['path'])
        self.changes: List[Dict[str, Any]] = []
    
    def detect_package_changes(self) -> List[Dict[str, Any]]:
        """Detect changes in package.json dependencies"""
        package_json_path = self.target_path / 'package.json'
        
        if not package_json_path.exists():
            print(f"{Fore.YELLOW}⚠️  package.json not found at {package_json_path}")
            return []
        
        with open(package_json_path, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
        
        changes = []
        
        # Check dependencies
        if 'dependencies' in package_data:
            for dep, version in package_data['dependencies'].items():
                changes.append({
                    'type': 'dependency',
                    'category': 'production',
                    'name': dep,
                    'version': version,
                    'file': 'package.json'
                })
        
        # Check devDependencies
        if 'devDependencies' in package_data:
            for dep, version in package_data['devDependencies'].items():
                changes.append({
                    'type': 'dependency',
                    'category': 'development',
                    'name': dep,
                    'version': version,
                    'file': 'package.json'
                })
        
        return changes
    
    def detect_env_changes(self) -> List[Dict[str, Any]]:
        """Detect changes in .env file"""
        env_path = self.target_path / '.env'
        
        if not env_path.exists():
            print(f"{Fore.YELLOW}⚠️  .env file not found at {env_path}")
            return []
        
        changes = []
        watch_fields = self.config['monitoring']['files'][1]['watch_fields']
        critical_vars = self.config['monitoring']['files'][1]['critical_vars']
        
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        if key in watch_fields:
                            changes.append({
                                'type': 'env_variable',
                                'name': key,
                                'value': value.strip(),
                                'critical': key in critical_vars,
                                'file': '.env'
                            })
        
        return changes
    
    def detect_port_changes(self) -> List[Dict[str, Any]]:
        """Detect port configurations in source files"""
        changes = []
        src_path = self.target_path / 'src'
        
        if not src_path.exists():
            return changes
        
        port_patterns = self.config['monitoring']['files'][2]['watch_patterns']
        
        for ts_file in src_path.rglob('*.ts'):
            with open(ts_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                for pattern in port_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        port = match.group(1) if match.groups() else None
                        if port:
                            changes.append({
                                'type': 'port_config',
                                'port': port,
                                'file': str(ts_file.relative_to(self.target_path)),
                                'pattern': pattern
                            })
        
        return changes
    
    def detect_all_changes(self) -> Dict[str, List[Dict[str, Any]]]:
        """Detect all types of changes"""
        print(f"{Fore.CYAN}🔍 Scanning for changes...")
        
        all_changes = {
            'dependencies': self.detect_package_changes(),
            'env_variables': self.detect_env_changes(),
            'port_configs': self.detect_port_changes()
        }
        
        total_changes = sum(len(changes) for changes in all_changes.values())
        print(f"{Fore.GREEN}✓ Found {total_changes} configuration items")
        
        return all_changes


class ReadmeParser:
    """Parses and manages README.md sections"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.readme_path = Path(config['readme_management']['target_readme'])
        self.managed_sections = config['readme_management']['managed_sections']
    
    def parse_readme(self) -> Dict[str, str]:
        """Parse README and extract managed sections"""
        if not self.readme_path.exists():
            print(f"{Fore.RED}❌ README not found at {self.readme_path}")
            return {}
        
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        sections = {}
        
        for section in self.managed_sections:
            start_marker = section['marker_start']
            end_marker = section['marker_end']
            
            pattern = f"{re.escape(start_marker)}(.*?){re.escape(end_marker)}"
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                sections[section['name']] = match.group(1).strip()
            else:
                print(f"{Fore.YELLOW}⚠️  Section '{section['name']}' not found in README")
        
        return sections
    
    def update_section(self, section_name: str, new_content: str) -> bool:
        """Update a specific section in the README"""
        if not self.readme_path.exists():
            return False
        
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the section config
        section_config = next(
            (s for s in self.managed_sections if s['name'] == section_name),
            None
        )
        
        if not section_config:
            return False
        
        start_marker = section_config['marker_start']
        end_marker = section_config['marker_end']
        
        # Replace the section content
        pattern = f"({re.escape(start_marker)}).*?({re.escape(end_marker)})"
        replacement = f"\\1\n{new_content}\n\\2"
        
        new_content_full = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        with open(self.readme_path, 'w', encoding='utf-8') as f:
            f.write(new_content_full)
        
        return True


class ReadmeGenerator:
    """Generates README content from detected changes"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.templates = config['templates']
    
    def generate_requirements_section(self, dependencies: List[Dict[str, Any]]) -> str:
        """Generate the Requirements section"""
        content = "## Requirements\n\n"
        
        # Add Node.js requirements (hardcoded for now, could be dynamic)
        content += "- Node.js >= 18.0.0\n"
        content += "- npm >= 9.0.0\n"
        
        # Find TypeScript version
        ts_version = next(
            (d['version'] for d in dependencies if d['name'] == 'typescript'),
            '5.1.6'
        )
        content += f"- TypeScript >= {ts_version}\n\n"
        
        # Production dependencies
        prod_deps = [d for d in dependencies if d['category'] == 'production']
        if prod_deps:
            content += "### Dependencies\n\n"
            for dep in prod_deps:
                content += f"- {dep['name']}: {dep['version']}\n"
            content += "\n"
        
        # Dev dependencies
        dev_deps = [d for d in dependencies if d['category'] == 'development']
        if dev_deps:
            content += "### Dev Dependencies\n\n"
            for dep in dev_deps:
                content += f"- {dep['name']}: {dep['version']}\n"
        
        return content.strip()
    
    def generate_configuration_section(self, env_vars: List[Dict[str, Any]]) -> str:
        """Generate the Configuration section"""
        content = "## Configuration\n\n"
        content += "The application uses environment variables for configuration. "
        content += "Create a `.env` file in the root directory:\n\n"
        
        # Separate critical and optional variables
        critical_vars = [v for v in env_vars if v.get('critical', False)]
        optional_vars = [v for v in env_vars if not v.get('critical', False)]
        
        if critical_vars:
            content += "### Required Variables\n\n"
            for var in critical_vars:
                content += f"- `{var['name']}`: "
                # Add descriptions based on variable name
                if 'PORT' in var['name']:
                    content += f"Server port (default: {var['value']})\n"
                elif 'HOST' in var['name']:
                    content += f"Server host (default: {var['value']})\n"
                elif 'NODE_ENV' in var['name']:
                    content += "Environment mode (development/production)\n"
                else:
                    content += f"(current: {var['value']})\n"
            content += "\n"
        
        if optional_vars:
            content += "### Optional Variables\n\n"
            for var in optional_vars:
                content += f"- `{var['name']}`: "
                # Add generic descriptions
                if 'DB' in var['name']:
                    content += "Database configuration\n"
                elif 'API' in var['name']:
                    content += "API configuration\n"
                elif 'ENABLE' in var['name']:
                    content += f"Feature flag ({var['value']})\n"
                else:
                    content += f"(current: {var['value']})\n"
        
        return content.strip()
    
    def generate_running_section(self, port_configs: List[Dict[str, Any]]) -> str:
        """Generate the Running section"""
        content = "## Running the Application\n\n"
        content += "### Development Mode\n\n"
        content += "```bash\n"
        content += "npm run dev\n"
        content += "```\n\n"
        
        # Extract port from configs
        port = "3000"  # default
        if port_configs:
            port = port_configs[0]['port']
        
        content += f"The server will start on `http://localhost:{port}`\n\n"
        content += "### Production Mode\n\n"
        content += "1. Build the TypeScript code:\n\n"
        content += "```bash\n"
        content += "npm run build\n"
        content += "```\n\n"
        content += "2. Start the server:\n\n"
        content += "```bash\n"
        content += "npm start\n"
        content += "```"
        
        return content.strip()


class LivingReadmeAgent:
    """Main agent orchestrator"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None, config_path: str = 'agent/doc_rules.json', project_root: Optional[Path] = None):
        """
        Initialize the Living README Agent.
        
        Args:
            config: Pre-loaded and resolved configuration dict (preferred)
            config_path: Path to config file (used only if config is None)
            project_root: Project root directory (used only if config is None)
        """
        if config is not None:
            # Use pre-loaded, resolved config from orchestrator
            self.config = config
            self.config_path = None
            self.project_root = None
        else:
            # Fallback: load config independently (for standalone usage)
            self.config_path = Path(config_path)
            self.project_root = project_root if project_root else Path.cwd()
            self.config = self.load_config()
        
        self.detector = ChangeDetector(self.config)
        self.parser = ReadmeParser(self.config)
        self.generator = ReadmeGenerator(self.config)
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from doc_rules.json (fallback for standalone usage)"""
        if self.config_path is None:
            print(f"{Fore.RED}❌ Configuration path not set")
            sys.exit(1)
        
        if not self.config_path.exists():
            print(f"{Fore.RED}❌ Configuration file not found: {self.config_path}")
            sys.exit(1)
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def run(self) -> Dict[str, Any]:
        """Main execution flow"""
        print(f"{Fore.CYAN}{Style.BRIGHT}🤖 Living README Agent Starting...")
        print(f"{Fore.CYAN}{'=' * 50}")
        
        # Detect changes
        changes = self.detector.detect_all_changes()
        
        # Parse current README
        current_sections = self.parser.parse_readme()
        print(f"{Fore.GREEN}✓ Parsed {len(current_sections)} managed sections")
        
        # Generate new content
        updates = {}
        
        if changes['dependencies']:
            new_requirements = self.generator.generate_requirements_section(
                changes['dependencies']
            )
            updates['Requirements'] = new_requirements
        
        if changes['env_variables']:
            new_config = self.generator.generate_configuration_section(
                changes['env_variables']
            )
            updates['Configuration'] = new_config
        
        if changes['port_configs']:
            new_running = self.generator.generate_running_section(
                changes['port_configs']
            )
            updates['Running'] = new_running
        
        # Apply updates
        updated_sections = []
        for section_name, new_content in updates.items():
            if self.parser.update_section(section_name, new_content):
                updated_sections.append(section_name)
                print(f"{Fore.GREEN}✓ Updated section: {section_name}")
        
        result = {
            'timestamp': datetime.now().isoformat(),
            'changes_detected': changes,
            'sections_updated': updated_sections,
            'success': len(updated_sections) > 0
        }
        
        print(f"{Fore.CYAN}{'=' * 50}")
        print(f"{Fore.GREEN}{Style.BRIGHT}✓ Agent execution complete!")
        
        return result


def main():
    """Entry point"""
    try:
        agent = LivingReadmeAgent()
        result = agent.run()
        
        # Print summary
        print(f"\n{Fore.MAGENTA}📊 Summary:")
        print(f"  - Sections updated: {len(result['sections_updated'])}")
        print(f"  - Timestamp: {result['timestamp']}")
        
        sys.exit(0 if result['success'] else 1)
        
    except Exception as e:
        print(f"{Fore.RED}❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

# Made with Bob
