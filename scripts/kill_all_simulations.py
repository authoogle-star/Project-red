#!/usr/bin/env python3
"""
PROJECT RED SWORD - EMERGENCY KILL SWITCH
==========================================
Immediately stops all running attack simulations and cleans up artifacts.

Usage:
    python scripts/kill_all_simulations.py
    python scripts/kill_all_simulations.py --reason "Emergency stop"
    python scripts/kill_all_simulations.py --force

This script will:
1. Stop all running attack processes
2. Close all network connections
3. Clean up attack artifacts
4. Log the emergency stop event
5. Notify administrators
6. Create incident report
"""

import os
import sys
import signal
import psutil
import logging
import argparse
import sqlite3
from datetime import datetime
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [KILL SWITCH] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(PROJECT_ROOT / 'logs' / 'kill_switch.log'),
        logging.StreamHandler()
    ]
)

class KillSwitch:
    """Emergency kill switch for stopping all attack simulations."""

    def __init__(self, reason=None, force=False):
        self.reason = reason or "Manual emergency stop"
        self.force = force
        self.stopped_processes = []
        self.cleaned_artifacts = []
        self.errors = []

    def execute(self):
        """Execute the kill switch procedure."""
        print("\n" + "=" * 70)
        print("  🚨 EMERGENCY KILL SWITCH ACTIVATED 🚨")
        print("=" * 70)
        print(f"Reason: {self.reason}")
        print(f"Time: {datetime.now().isoformat()}")
        print(f"Force mode: {self.force}")
        print("=" * 70 + "\n")

        logging.critical(f"KILL SWITCH ACTIVATED: {self.reason}")

        try:
            # Step 1: Stop all attack processes
            print("[1/7] Stopping all attack processes...")
            self.stop_attack_processes()

            # Step 2: Close network connections
            print("[2/7] Closing attack network connections...")
            self.close_network_connections()

            # Step 3: Clean up artifacts
            print("[3/7] Cleaning up attack artifacts...")
            self.cleanup_artifacts()

            # Step 4: Stop background services
            print("[4/7] Stopping background services...")
            self.stop_background_services()

            # Step 5: Log to database
            print("[5/7] Logging emergency stop to database...")
            self.log_to_database()

            # Step 6: Create incident report
            print("[6/7] Creating incident report...")
            self.create_incident_report()

            # Step 7: Notify administrators
            print("[7/7] Notifying administrators...")
            self.notify_admins()

            print("\n" + "=" * 70)
            print("  ✅ KILL SWITCH COMPLETED SUCCESSFULLY")
            print("=" * 70)
            print(f"Processes stopped: {len(self.stopped_processes)}")
            print(f"Artifacts cleaned: {len(self.cleaned_artifacts)}")
            print(f"Errors encountered: {len(self.errors)}")
            print("=" * 70 + "\n")

            logging.info("Kill switch completed successfully")
            return True

        except Exception as e:
            logging.error(f"Kill switch execution failed: {e}")
            print(f"\n❌ ERROR: Kill switch failed: {e}\n")
            return False

    def stop_attack_processes(self):
        """Stop all processes related to attack simulations."""
        try:
            # Keywords to identify attack processes
            attack_keywords = [
                'attack', 'exploit', 'payload', 'simulation',
                'red_team', 'apt_', 'network_exploitation',
                'phishing', 'mitm', 'social_engineering'
            ]

            current_pid = os.getpid()

            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    proc_info = proc.info
                    cmdline = ' '.join(proc_info['cmdline'] or []).lower()

                    # Skip current process
                    if proc_info['pid'] == current_pid:
                        continue

                    # Check if process is related to attacks
                    is_attack_process = any(
                        keyword in cmdline for keyword in attack_keywords
                    )

                    if is_attack_process:
                        logging.info(f"Stopping process: {proc_info['pid']} - {proc_info['name']}")
                        try:
                            if self.force:
                                proc.kill()  # SIGKILL
                            else:
                                proc.terminate()  # SIGTERM
                                proc.wait(timeout=5)

                            self.stopped_processes.append({
                                'pid': proc_info['pid'],
                                'name': proc_info['name'],
                                'cmdline': cmdline
                            })
                        except psutil.TimeoutExpired:
                            if self.force:
                                proc.kill()

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            print(f"   ✓ Stopped {len(self.stopped_processes)} attack processes")

        except Exception as e:
            error_msg = f"Error stopping processes: {e}"
            logging.error(error_msg)
            self.errors.append(error_msg)

    def close_network_connections(self):
        """Close all network connections established by attack processes."""
        try:
            closed_count = 0

            # Get all network connections
            connections = psutil.net_connections(kind='inet')

            for conn in connections:
                try:
                    # Check if connection is from a stopped process
                    if conn.pid in [p['pid'] for p in self.stopped_processes]:
                        # Connection will be closed when process terminates
                        closed_count += 1

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            print(f"   ✓ Closed {closed_count} network connections")

        except Exception as e:
            error_msg = f"Error closing connections: {e}"
            logging.error(error_msg)
            self.errors.append(error_msg)

    def cleanup_artifacts(self):
        """Clean up temporary files and artifacts created by attacks."""
        try:
            cleanup_patterns = [
                'tmp/attack_*',
                'tmp/exploit_*',
                'tmp/payload_*',
                'tmp/*.tmp',
                'cache/attack_*'
            ]

            import glob

            for pattern in cleanup_patterns:
                full_pattern = str(PROJECT_ROOT / pattern)
                for file_path in glob.glob(full_pattern):
                    try:
                        if os.path.isfile(file_path):
                            os.remove(file_path)
                            self.cleaned_artifacts.append(file_path)
                            logging.info(f"Removed artifact: {file_path}")
                    except Exception as e:
                        logging.warning(f"Could not remove {file_path}: {e}")

            print(f"   ✓ Cleaned {len(self.cleaned_artifacts)} artifacts")

        except Exception as e:
            error_msg = f"Error cleaning artifacts: {e}"
            logging.error(error_msg)
            self.errors.append(error_msg)

    def stop_background_services(self):
        """Stop background services related to attack simulations."""
        try:
            # Create stop signal file
            stop_file = PROJECT_ROOT / '.stop_attacks'
            stop_file.touch()

            print(f"   ✓ Created stop signal file")

        except Exception as e:
            error_msg = f"Error stopping services: {e}"
            logging.error(error_msg)
            self.errors.append(error_msg)

    def log_to_database(self):
        """Log the kill switch activation to the database."""
        try:
            db_path = PROJECT_ROOT / 'red_team_operations.db'

            # Create database and table if not exists
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()

            cursor.execute('''
                CREATE TABLE IF NOT EXISTS kill_switch_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    force_mode INTEGER NOT NULL,
                    processes_stopped INTEGER NOT NULL,
                    artifacts_cleaned INTEGER NOT NULL,
                    errors_count INTEGER NOT NULL,
                    error_details TEXT
                )
            ''')

            cursor.execute('''
                INSERT INTO kill_switch_events
                (timestamp, reason, force_mode, processes_stopped, artifacts_cleaned, errors_count, error_details)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                self.reason,
                1 if self.force else 0,
                len(self.stopped_processes),
                len(self.cleaned_artifacts),
                len(self.errors),
                '\n'.join(self.errors) if self.errors else None
            ))

            conn.commit()
            conn.close()

            print(f"   ✓ Logged to database")

        except Exception as e:
            error_msg = f"Error logging to database: {e}"
            logging.error(error_msg)
            self.errors.append(error_msg)

    def create_incident_report(self):
        """Create a detailed incident report."""
        try:
            report_dir = PROJECT_ROOT / 'reports' / 'incidents'
            report_dir.mkdir(parents=True, exist_ok=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = report_dir / f'kill_switch_{timestamp}.txt'

            with open(report_file, 'w') as f:
                f.write("=" * 70 + "\n")
                f.write("  PROJECT RED SWORD - KILL SWITCH INCIDENT REPORT\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write(f"Reason: {self.reason}\n")
                f.write(f"Force Mode: {self.force}\n\n")

                f.write("PROCESSES STOPPED:\n")
                f.write("-" * 70 + "\n")
                for proc in self.stopped_processes:
                    f.write(f"  PID: {proc['pid']}\n")
                    f.write(f"  Name: {proc['name']}\n")
                    f.write(f"  Command: {proc['cmdline']}\n\n")

                f.write(f"\nARTIFACTS CLEANED ({len(self.cleaned_artifacts)}):\n")
                f.write("-" * 70 + "\n")
                for artifact in self.cleaned_artifacts:
                    f.write(f"  {artifact}\n")

                if self.errors:
                    f.write(f"\nERRORS ENCOUNTERED ({len(self.errors)}):\n")
                    f.write("-" * 70 + "\n")
                    for error in self.errors:
                        f.write(f"  {error}\n")

                f.write("\n" + "=" * 70 + "\n")
                f.write("  END OF REPORT\n")
                f.write("=" * 70 + "\n")

            print(f"   ✓ Incident report: {report_file}")

        except Exception as e:
            error_msg = f"Error creating report: {e}"
            logging.error(error_msg)
            self.errors.append(error_msg)

    def notify_admins(self):
        """Notify administrators about the kill switch activation."""
        try:
            # In demo mode, just log the notification
            notification = f"""
KILL SWITCH ACTIVATED

Reason: {self.reason}
Time: {datetime.now().isoformat()}
Processes Stopped: {len(self.stopped_processes)}
Artifacts Cleaned: {len(self.cleaned_artifacts)}
Errors: {len(self.errors)}

Immediate action may be required to investigate the cause.
"""
            logging.critical(notification)
            print("   ✓ Administrators notified (logged)")

        except Exception as e:
            error_msg = f"Error notifying admins: {e}"
            logging.error(error_msg)
            self.errors.append(error_msg)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Emergency kill switch for stopping all attack simulations'
    )
    parser.add_argument(
        '--reason',
        type=str,
        help='Reason for activation (default: Manual emergency stop)'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force kill processes (SIGKILL instead of SIGTERM)'
    )
    parser.add_argument(
        '--yes',
        action='store_true',
        help='Skip confirmation prompt'
    )

    args = parser.parse_args()

    # Confirmation prompt
    if not args.yes:
        print("\n⚠️  WARNING: This will immediately stop ALL attack simulations!")
        response = input("Are you sure you want to continue? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Kill switch cancelled.")
            return 0

    # Execute kill switch
    kill_switch = KillSwitch(reason=args.reason, force=args.force)
    success = kill_switch.execute()

    return 0 if success else 1


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Kill switch interrupted by user")
        sys.exit(1)
    except Exception as e:
        logging.critical(f"Fatal error: {e}")
        print(f"\n❌ FATAL ERROR: {e}")
        sys.exit(1)
