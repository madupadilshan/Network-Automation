#!/usr/bin/env python3
"""
Configure Interfaces on Cisco IOS Routers
Task 1: Automate IP address configuration on router interfaces
"""

import yaml
import os
import sys
from netmiko import ConnectHandler
from dotenv import load_dotenv
import logging
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('interface_config.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def load_config_files():
    """Load YAML configuration files"""
    try:
        with open('configs/inventory.yml', 'r') as f:
            inventory = yaml.safe_load(f)

        with open('configs/interfaces.yml', 'r') as f:
            interfaces = yaml.safe_load(f)

        return inventory, interfaces
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        sys.exit(1)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML: {e}")
        sys.exit(1)

def configure_interface(device, interface_config):
    """Configure a single interface"""
    commands = []

    # Interface configuration commands
    commands.append(f"interface {interface_config['name']}")
    commands.append(f"ip address {interface_config['ip_address']} {interface_config['subnet_mask']}")
    commands.append(f"description {interface_config['description']}")

    if interface_config.get('enabled', True):
        commands.append("no shutdown")
    else:
        commands.append("shutdown")

    try:
        output = device.send_config_set(commands)
        return True, output
    except Exception as e:
        logger.error(f"Error configuring interface: {e}")
        return False, str(e)

def connect_and_configure(router, username, password, secret, interface_configs):
    """Connect to router and configure all interfaces"""
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

        # Configure each interface
        for interface in interface_configs:
            print(f"  Configuring {interface['name']}... ", end='')
            success, output = configure_interface(device, interface)

            if success:
                print(f"{Fore.GREEN}✓{Style.RESET_ALL}")
                logger.info(f"Successfully configured {interface['name']} on {router['name']}")
            else:
                print(f"{Fore.RED}✗{Style.RESET_ALL}")
                logger.error(f"Failed to configure {interface['name']} on {router['name']}")

        # Save configuration
        print(f"  Saving configuration... ", end='')
        device.send_command("write memory")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL}")

        device.disconnect()
        return True

    except Exception as e:
        logger.error(f"Error connecting to {router['name']}: {e}")
        print(f"\n{Fore.RED}✗ Failed to connect to {router['name']}: {e}{Style.RESET_ALL}")
        return False

def main():
    """Main execution function"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"  Interface Configuration Script")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    # Load credentials
    username = os.getenv('ROUTER_USERNAME')
    password = os.getenv('ROUTER_PASSWORD')
    secret = os.getenv('ROUTER_SECRET')

    if not all([username, password, secret]):
        logger.error("Missing credentials. Please check .env file")
        sys.exit(1)

    # Load configurations
    inventory, interface_configs = load_config_files()

    success_count = 0
    fail_count = 0

    # Process each router
    for router in inventory['routers']:
        router_name = router['name']

        # Get interface configs for this router
        router_interfaces = interface_configs.get(router_name, {}).get('interfaces', [])

        if not router_interfaces:
            logger.warning(f"No interface configuration found for {router_name}")
            continue

        if connect_and_configure(router, username, password, secret, router_interfaces):
            success_count += 1
        else:
            fail_count += 1

    # Summary
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"  Summary")
    print(f"{'='*60}{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}Successful: {success_count}{Style.RESET_ALL}")
    print(f"  {Fore.RED}Failed: {fail_count}{Style.RESET_ALL}")
    print()

    return 0 if fail_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
