#!/usr/bin/env python3
"""
Configure VLANs and Subinterfaces on Cisco IOS Routers
Task 3: Automate VLAN configuration
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
        logging.FileHandler('vlan_config.log'),
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

        with open('configs/vlans.yml', 'r') as f:
            vlans = yaml.safe_load(f)

        return inventory, vlans
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        sys.exit(1)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML: {e}")
        sys.exit(1)

def configure_subinterface(device, subinterface_config):
    """Configure a router subinterface for VLAN"""
    commands = []

    # Subinterface configuration
    commands.append(f"interface {subinterface_config['interface']}")
    commands.append(f"encapsulation dot1Q {subinterface_config['vlan']}")
    commands.append(f"ip address {subinterface_config['ip_address']} {subinterface_config['subnet_mask']}")
    commands.append(f"description {subinterface_config['description']}")
    commands.append("no shutdown")

    try:
        output = device.send_config_set(commands)
        return True, output
    except Exception as e:
        logger.error(f"Error configuring subinterface: {e}")
        return False, str(e)

def connect_and_configure(router, username, password, secret, vlan_config):
    """Connect to router and configure VLANs"""
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

        router_name = router['name']

        # Get subinterface configs for this router
        subinterfaces = vlan_config.get('router_subinterfaces', {}).get(router_name, [])

        if not subinterfaces:
            print(f"  {Fore.YELLOW}No VLAN configuration for this router{Style.RESET_ALL}")
            device.disconnect()
            return True

        # Configure each subinterface
        for subintf in subinterfaces:
            print(f"  Configuring {subintf['interface']} (VLAN {subintf['vlan']})... ", end='')
            success, output = configure_subinterface(device, subintf)

            if success:
                print(f"{Fore.GREEN}✓{Style.RESET_ALL}")
                logger.info(f"Successfully configured {subintf['interface']} on {router_name}")
            else:
                print(f"{Fore.RED}✗{Style.RESET_ALL}")
                logger.error(f"Failed to configure {subintf['interface']} on {router_name}")

        # Show VLAN summary
        print(f"  Verifying subinterfaces... ", end='')
        verification = device.send_command("show ip interface brief | include \\.")
        print(f"{Fore.GREEN}✓{Style.RESET_ALL}")

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
    print(f"  VLAN Configuration Script")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    # Load credentials
    username = os.getenv('ROUTER_USERNAME')
    password = os.getenv('ROUTER_PASSWORD')
    secret = os.getenv('ROUTER_SECRET')

    if not all([username, password, secret]):
        logger.error("Missing credentials. Please check .env file")
        sys.exit(1)

    # Load configurations
    inventory, vlan_config = load_config_files()

    # Display VLAN information
    vlans = vlan_config.get('vlans', [])
    if vlans:
        print(f"VLANs to configure:")
        for vlan in vlans:
            print(f"  - VLAN {vlan['id']}: {vlan['name']} ({vlan['description']})")
        print()

    success_count = 0
    fail_count = 0

    # Process each router
    for router in inventory['routers']:
        if connect_and_configure(router, username, password, secret, vlan_config):
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
