#!/usr/bin/env python3
"""
Backup Router Configurations
Task 4: Automate configuration backup to GitHub
"""

import yaml
import os
import sys
from netmiko import ConnectHandler
from dotenv import load_dotenv
import logging
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('backup.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def load_inventory():
    """Load inventory configuration file"""
    try:
        with open('configs/inventory.yml', 'r') as f:
            inventory = yaml.safe_load(f)
        return inventory
    except FileNotFoundError as e:
        logger.error(f"Inventory file not found: {e}")
        sys.exit(1)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML: {e}")
        sys.exit(1)

def backup_router_config(router, username, password, secret, backup_dir):
    """Connect to router and backup running configuration"""
    device_params = {
        'device_type': router['device_type'],
        'ip': router['ip'],
        'username': username,
        'password': password,
        'secret': secret,
        'port': router.get('port', 22),
        'timeout': 10,
    }

    try:
        logger.info(f"Connecting to {router['name']} ({router['ip']})...")
        device = ConnectHandler(**device_params)
        device.enable()

        print(f"\n{Fore.GREEN}✓ Connected to {router['name']}{Style.RESET_ALL}")

        # Get running configuration
        print(f"  Retrieving running configuration... ", end='')
        running_config = device.send_command("show running-config")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL}")

        # Get additional information
        print(f"  Gathering device information... ", end='')
        version_info = device.send_command("show version | include Version")
        hostname = device.send_command("show run | include hostname")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL}")

        # Create backup filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{router['name']}_{timestamp}.txt"
        filepath = os.path.join(backup_dir, filename)

        # Create latest backup without timestamp
        latest_filename = f"{router['name']}_latest.txt"
        latest_filepath = os.path.join(backup_dir, latest_filename)

        # Write backup to file
        print(f"  Writing backup to file... ", end='')
        with open(filepath, 'w') as f:
            f.write(f"! Backup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"! Router: {router['name']}\n")
            f.write(f"! IP Address: {router['ip']}\n")
            f.write(f"! {version_info}\n")
            f.write(f"!\n")
            f.write(f"! {'-'*70}\n")
            f.write(f"!\n")
            f.write(running_config)

        # Also write to latest file
        with open(latest_filepath, 'w') as f:
            f.write(f"! Backup Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"! Router: {router['name']}\n")
            f.write(f"! IP Address: {router['ip']}\n")
            f.write(f"! {version_info}\n")
            f.write(f"!\n")
            f.write(f"! {'-'*70}\n")
            f.write(f"!\n")
            f.write(running_config)

        print(f"{Fore.GREEN}✓{Style.RESET_ALL}")

        # Get file size
        file_size = os.path.getsize(filepath)
        print(f"  Backup saved: {filename} ({file_size} bytes)")

        device.disconnect()
        logger.info(f"Successfully backed up {router['name']} to {filename}")
        return True, filename

    except Exception as e:
        logger.error(f"Error backing up {router['name']}: {e}")
        print(f"\n{Fore.RED}✗ Failed to backup {router['name']}: {e}{Style.RESET_ALL}")
        return False, None

def create_backup_index(backup_dir, successful_backups):
    """Create an index file listing all backups"""
    index_file = os.path.join(backup_dir, 'README.md')

    with open(index_file, 'w') as f:
        f.write("# Router Configuration Backups\n\n")
        f.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("## Latest Backups\n\n")

        for router_name, filename in successful_backups:
            f.write(f"- **{router_name}**: [{filename}]({filename})\n")

        f.write("\n## All Backups\n\n")
        f.write("Check the `backups/` directory for historical backups.\n")
        f.write("\n## Backup Naming Convention\n\n")
        f.write("- Format: `{RouterName}_{YYYYMMDD_HHMMSS}.txt`\n")
        f.write("- Latest: `{RouterName}_latest.txt`\n")

def main():
    """Main execution function"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"  Configuration Backup Script")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    # Load credentials
    username = os.getenv('ROUTER_USERNAME')
    password = os.getenv('ROUTER_PASSWORD')
    secret = os.getenv('ROUTER_SECRET')

    if not all([username, password, secret]):
        logger.error("Missing credentials. Please check .env file")
        sys.exit(1)

    # Create backup directory if it doesn't exist
    backup_dir = 'backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        logger.info(f"Created backup directory: {backup_dir}")

    # Load inventory
    inventory = load_inventory()

    success_count = 0
    fail_count = 0
    successful_backups = []

    # Process each router
    for router in inventory['routers']:
        success, filename = backup_router_config(router, username, password, secret, backup_dir)
        if success:
            success_count += 1
            successful_backups.append((router['name'], filename))
        else:
            fail_count += 1

    # Create backup index
    if successful_backups:
        print(f"\n  Creating backup index... ", end='')
        create_backup_index(backup_dir, successful_backups)
        print(f"{Fore.GREEN}✓{Style.RESET_ALL}")

    # Summary
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"  Summary")
    print(f"{'='*60}{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Successful: {success_count}{Style.RESET_ALL}")
    print(f"  {Fore.RED}Failed: {fail_count}{Style.RESET_ALL}")
    print(f"  Backup location: {os.path.abspath(backup_dir)}")
    print()

    return 0 if fail_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
