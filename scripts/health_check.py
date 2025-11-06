#!/usr/bin/env python3
"""
PROJECT RED SWORD - HEALTH CHECK SCRIPT
========================================
Verifies that all systems are operational and safe to start attack simulations.

Usage:
    python scripts/health_check.py
    python scripts/health_check.py --mode preflight
    python scripts/health_check.py --mode monitoring
    python scripts/health_check.py --fix
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [HEALTH CHECK] - %(levelname)s - %(message)s'
)

class HealthCheck:
    """System health check and validation."""

    def __init__(self, mode='full', fix=False):
        self.mode = mode
        self.fix = fix
        self.checks_passed = 0
        self.checks_failed = 0
        self.warnings = 0

    def run(self):
        """Run health checks based on mode."""
        print("\n" + "=" * 70)
        print(f"  PROJECT RED SWORD - HEALTH CHECK ({self.mode.upper()})")
        print("=" * 70 + "\n")

        if self.mode in ['full', 'preflight']:
            self.check_python_environment()
            self.check_configuration_files()
            self.check_database()
            self.check_directories()
            self.check_dependencies()

        if self.mode in ['full', 'monitoring']:
            self.check_monitoring_systems()
            self.check_safety_mechanisms()

        if self.mode in ['full', 'permissions']:
            self.check_file_permissions()

        # Summary
        print("\n" + "=" * 70)
        print("  HEALTH CHECK SUMMARY")
        print("=" * 70)
        print(f"✓ Checks Passed: {self.checks_passed}")
        print(f"❌ Checks Failed: {self.checks_failed}")
        print(f"⚠  Warnings: {self.warnings}")
        print("=" * 70 + "\n")

        if self.checks_failed > 0:
            print("❌ Health check FAILED. System is not ready.")
            return False
        elif self.warnings > 0:
            print("⚠  Health check passed with warnings.")
            return True
        else:
            print("✅ Health check PASSED. System is ready.")
            return True

    def check_python_environment(self):
        """Check Python environment."""
        print("[CHECK] Python Environment")
        try:
            # Check Python version
            import sys
            version = sys.version_info
            if version.major >= 3 and version.minor >= 8:
                print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
                self.checks_passed += 1
            else:
                print(f"  ❌ Python version too old: {version.major}.{version.minor}")
                self.checks_failed += 1

        except Exception as e:
            print(f"  ❌ Error checking Python: {e}")
            self.checks_failed += 1

    def check_configuration_files(self):
        """Check required configuration files."""
        print("\n[CHECK] Configuration Files")
        required_files = [
            '.env',
            'config/attack_config.yaml',
            'config/safe_mode.yaml',
            'config/targets.yaml'
        ]

        for file_path in required_files:
            full_path = PROJECT_ROOT / file_path
            if full_path.exists():
                print(f"  ✓ {file_path}")
                self.checks_passed += 1
            else:
                print(f"  ❌ {file_path} not found")
                self.checks_failed += 1

                if self.fix:
                    print(f"     Attempting to create {file_path}...")
                    # Could create default files here

    def check_database(self):
        """Check database connectivity."""
        print("\n[CHECK] Database")
        try:
            from database.models import SessionLocal, engine
            from sqlalchemy import text

            # Test connection
            session = SessionLocal()
            session.execute(text('SELECT 1'))
            session.close()

            print(f"  ✓ Database connection OK")
            self.checks_passed += 1

        except Exception as e:
            print(f"  ❌ Database error: {e}")
            self.checks_failed += 1

    def check_directories(self):
        """Check required directories."""
        print("\n[CHECK] Directories")
        required_dirs = [
            'logs',
            'reports',
            'reports/generated',
            'reports/incidents',
            'backups',
            'tmp',
            'cache'
        ]

        for dir_path in required_dirs:
            full_path = PROJECT_ROOT / dir_path
            if full_path.exists():
                print(f"  ✓ {dir_path}/")
                self.checks_passed += 1
            else:
                print(f"  ⚠  {dir_path}/ not found")
                self.warnings += 1

                if self.fix:
                    full_path.mkdir(parents=True, exist_ok=True)
                    print(f"     Created {dir_path}/")

    def check_dependencies(self):
        """Check critical Python dependencies."""
        print("\n[CHECK] Dependencies")
        critical_deps = [
            'panel',
            'datashader',
            'numpy',
            'pandas',
            'sqlalchemy',
            'psutil'
        ]

        for dep in critical_deps:
            try:
                __import__(dep)
                print(f"  ✓ {dep}")
                self.checks_passed += 1
            except ImportError:
                print(f"  ❌ {dep} not installed")
                self.checks_failed += 1

    def check_monitoring_systems(self):
        """Check monitoring systems."""
        print("\n[CHECK] Monitoring Systems")
        try:
            # Check if monitoring modules can be imported
            from modules.real_time_monitoring import RealTimeMonitoring
            print(f"  ✓ RealTimeMonitoring module")
            self.checks_passed += 1

            from modules.blockchain_logger import BlockchainLogger
            print(f"  ✓ BlockchainLogger module")
            self.checks_passed += 1

        except Exception as e:
            print(f"  ❌ Monitoring system error: {e}")
            self.checks_failed += 1

    def check_safety_mechanisms(self):
        """Check safety mechanisms."""
        print("\n[CHECK] Safety Mechanisms")

        # Check kill switch script
        kill_switch = PROJECT_ROOT / 'scripts' / 'kill_all_simulations.py'
        if kill_switch.exists():
            print(f"  ✓ Kill switch script available")
            self.checks_passed += 1
        else:
            print(f"  ❌ Kill switch script not found")
            self.checks_failed += 1

        # Check environment variables
        import os
        from dotenv import load_dotenv
        load_dotenv()

        safe_mode = os.getenv('SAFE_MODE', 'false').lower() == 'true'
        if safe_mode:
            print(f"  ✓ Safe mode enabled")
            self.checks_passed += 1
        else:
            print(f"  ⚠  Safe mode disabled")
            self.warnings += 1

        # Check stop signal files
        stop_files = ['.stop_attacks', '.kill_switch']
        for stop_file in stop_files:
            if (PROJECT_ROOT / stop_file).exists():
                print(f"  ⚠  Stop signal file exists: {stop_file}")
                self.warnings += 1
                if self.fix:
                    (PROJECT_ROOT / stop_file).unlink()
                    print(f"     Removed {stop_file}")

    def check_file_permissions(self):
        """Check file permissions."""
        print("\n[CHECK] File Permissions")

        # Check if scripts are executable
        scripts = [
            'scripts/kill_all_simulations.py',
            'scripts/start_red_team.sh',
            'scripts/health_check.py'
        ]

        for script in scripts:
            script_path = PROJECT_ROOT / script
            if script_path.exists():
                if os.access(script_path, os.X_OK):
                    print(f"  ✓ {script} is executable")
                    self.checks_passed += 1
                else:
                    print(f"  ⚠  {script} is not executable")
                    self.warnings += 1
                    if self.fix:
                        os.chmod(script_path, 0o755)
                        print(f"     Made {script} executable")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Health check for Project Red Sword'
    )
    parser.add_argument(
        '--mode',
        type=str,
        choices=['full', 'preflight', 'monitoring', 'permissions'],
        default='full',
        help='Health check mode'
    )
    parser.add_argument(
        '--fix',
        action='store_true',
        help='Attempt to fix issues automatically'
    )

    args = parser.parse_args()

    health_check = HealthCheck(mode=args.mode, fix=args.fix)
    success = health_check.run()

    return 0 if success else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nHealth check interrupted")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)
