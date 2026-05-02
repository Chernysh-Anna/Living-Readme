#!/usr/bin/env python3
"""
Living README Agent - Verification Module
Runs setup commands to verify README instructions are valid
"""

import subprocess
import time
import socket
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, TYPE_CHECKING
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


class CommandVerifier:
    """Verifies setup commands work as documented"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.verification_config = config.get('verification', {})
        self.results: List[Dict[str, Any]] = []
    
    def check_port_available(self, port: int, timeout: int = 5) -> bool:
        """Check if a port is available (not in use)"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        try:
            result = sock.connect_ex(('localhost', port))
            sock.close()
            return result == 0  # 0 means port is in use (server is running)
        except Exception:
            return False
    
    def run_command(
        self,
        command: str,
        working_dir: str,
        timeout: int = 60,
        check_output: bool = True
    ) -> Tuple[bool, str, str]:
        """
        Run a shell command and return success status, stdout, stderr
        
        Args:
            command: Command to execute
            working_dir: Working directory for command
            timeout: Timeout in seconds
            check_output: Whether to capture output
            
        Returns:
            Tuple of (success, stdout, stderr)
        """
        try:
            print(f"{Fore.CYAN}  ▶ Running: {command}")
            print(f"{Fore.CYAN}    Working dir: {working_dir}")
            
            # Use shell=True for Windows compatibility
            process = subprocess.Popen(
                command,
                shell=True,
                cwd=working_dir,
                stdout=subprocess.PIPE if check_output else None,
                stderr=subprocess.PIPE if check_output else None,
                text=True
            )
            
            try:
                stdout, stderr = process.communicate(timeout=timeout)
                success = process.returncode == 0
                
                if success:
                    print(f"{Fore.GREEN}  ✓ Command succeeded")
                else:
                    print(f"{Fore.YELLOW}  ⚠ Command failed with code {process.returncode}")
                
                return success, stdout or "", stderr or ""
                
            except subprocess.TimeoutExpired:
                process.kill()
                print(f"{Fore.YELLOW}  ⚠ Command timed out after {timeout}s")
                return False, "", f"Command timed out after {timeout} seconds"
                
        except Exception as e:
            print(f"{Fore.RED}  ✗ Command error: {str(e)}")
            return False, "", str(e)
    
    def verify_installation(self) -> Dict[str, Any]:
        """Verify npm install command"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}📦 Verifying Installation...")
        
        cmd_config = next(
            (c for c in self.verification_config['commands'] 
             if c['name'] == 'install_dependencies'),
            None
        )
        
        if not cmd_config:
            return {'success': False, 'error': 'No install command configured'}
        
        success, stdout, stderr = self.run_command(
            cmd_config['command'],
            cmd_config['working_dir'],
            cmd_config['timeout']
        )
        
        result = {
            'command': 'install_dependencies',
            'success': success,
            'stdout': stdout[:500] if stdout else "",  # Truncate for brevity
            'stderr': stderr[:500] if stderr else "",
            'timestamp': datetime.now().isoformat()
        }
        
        self.results.append(result)
        return result
    
    def verify_build(self) -> Dict[str, Any]:
        """Verify npm build command"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}🔨 Verifying Build...")
        
        cmd_config = next(
            (c for c in self.verification_config['commands'] 
             if c['name'] == 'build_project'),
            None
        )
        
        if not cmd_config:
            return {'success': False, 'error': 'No build command configured'}
        
        success, stdout, stderr = self.run_command(
            cmd_config['command'],
            cmd_config['working_dir'],
            cmd_config['timeout']
        )
        
        result = {
            'command': 'build_project',
            'success': success,
            'stdout': stdout[:500] if stdout else "",
            'stderr': stderr[:500] if stderr else "",
            'timestamp': datetime.now().isoformat()
        }
        
        self.results.append(result)
        return result
    
    def verify_server_start(self) -> Dict[str, Any]:
        """Verify server starts and binds to correct port"""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}🚀 Verifying Server Start...")
        
        cmd_config = next(
            (c for c in self.verification_config['commands'] 
             if c['name'] == 'start_server'),
            None
        )
        
        if not cmd_config:
            return {'success': False, 'error': 'No start command configured'}
        
        # Get expected port from config
        port_check_config = self.verification_config.get('port_check', {})
        expected_port = 3000  # default
        
        # Try to read port from .env
        env_path = Path(cmd_config['working_dir']) / '.env'
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('PORT='):
                        try:
                            expected_port = int(line.split('=')[1].strip())
                        except ValueError:
                            pass
        
        print(f"{Fore.CYAN}  Expected port: {expected_port}")
        
        # Start the server in background
        success, stdout, stderr = self.run_command(
            cmd_config['command'],
            cmd_config['working_dir'],
            cmd_config['timeout']
        )
        
        # Check if port is bound
        port_bound = False
        if cmd_config.get('verify_port', False):
            print(f"{Fore.CYAN}  Checking port {expected_port}...")
            time.sleep(2)  # Give server time to start
            port_bound = self.check_port_available(expected_port)
            
            if port_bound:
                print(f"{Fore.GREEN}  ✓ Server is listening on port {expected_port}")
            else:
                print(f"{Fore.YELLOW}  ⚠ Server not detected on port {expected_port}")
        
        result = {
            'command': 'start_server',
            'success': success or port_bound,  # Consider success if port is bound
            'port_verified': port_bound,
            'expected_port': expected_port,
            'stdout': stdout[:500] if stdout else "",
            'stderr': stderr[:500] if stderr else "",
            'timestamp': datetime.now().isoformat()
        }
        
        self.results.append(result)
        return result
    
    def run_all_verifications(self) -> Dict[str, Any]:
        """Run all verification steps"""
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{'=' * 60}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}🔍 Starting Verification Process")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'=' * 60}")
        
        if not self.verification_config.get('enabled', False):
            print(f"{Fore.YELLOW}⚠️  Verification is disabled in config")
            return {
                'enabled': False,
                'results': [],
                'summary': {'total': 0, 'passed': 0, 'failed': 0}
            }
        
        # Run verifications in order
        install_result = self.verify_installation()
        
        # Only proceed with build if install succeeded
        build_result = None
        if install_result['success']:
            build_result = self.verify_build()
        else:
            print(f"{Fore.YELLOW}⚠️  Skipping build verification (install failed)")
            build_result = {
                'command': 'build_project',
                'success': False,
                'skipped': True,
                'reason': 'Installation failed'
            }
        
        # Only proceed with server start if build succeeded
        server_result = None
        if build_result and build_result['success']:
            server_result = self.verify_server_start()
        else:
            print(f"{Fore.YELLOW}⚠️  Skipping server verification (build failed)")
            server_result = {
                'command': 'start_server',
                'success': False,
                'skipped': True,
                'reason': 'Build failed'
            }
        
        # Calculate summary
        all_results = [install_result, build_result, server_result]
        passed = sum(1 for r in all_results if r and r.get('success', False))
        failed = sum(1 for r in all_results if r and not r.get('success', False) and not r.get('skipped', False))
        
        summary = {
            'total': len(all_results),
            'passed': passed,
            'failed': failed,
            'skipped': sum(1 for r in all_results if r and r.get('skipped', False))
        }
        
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{'=' * 60}")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}📊 Verification Summary")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}{'=' * 60}")
        print(f"{Fore.GREEN}  ✓ Passed: {summary['passed']}")
        print(f"{Fore.RED}  ✗ Failed: {summary['failed']}")
        print(f"{Fore.YELLOW}  ⊘ Skipped: {summary['skipped']}")
        
        return {
            'enabled': True,
            'results': all_results,
            'summary': summary,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_results(self) -> List[Dict[str, Any]]:
        """Get all verification results"""
        return self.results


def main():
    """Test the verifier standalone"""
    import json
    
    # Load config
    config_path = Path('agent/doc_rules.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    # Run verifications
    verifier = CommandVerifier(config)
    results = verifier.run_all_verifications()
    
    # Print results
    print(f"\n{Fore.CYAN}Results:")
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()

# Made with Bob
