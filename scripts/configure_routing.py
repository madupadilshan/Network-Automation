#!/usr/bin/env python3
"""
Configure Routing Protocols (OSPF/EIGRP) on Cisco IOS Routers
Task 2: Automate dynamic routing configuration
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
        logging.FileHandler('routing_config.log'),
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

        with open('configs/routing.yml', 'r') as f:
            routing = yaml.safe_load(f)

        return inventory, routing
    except FileNotFoundError as e:
        logger.error(f"Configuration file not found: {e}")
        sys.exit(1)
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML: {e}")
        sys.exit(1)

def configure_ospf(device, router_name, ospf_config):
    """Configure OSPF on router"""
    commands = []

    process_id = ospf_config['process_id']
    router_id = ospf_config['router_id_map'].get(router_name)

    # OSPF configuration
    commands.append(f"router ospf {process_id}")
    if router_id:
        commands.append(f"router-id {router_id}")

    # Add networks
    areas = ospf_config['areas'].get(router_name, [])
    for area_config in areas:
        area = area_config['area']
        for network in area_config['networks']:
            commands.append(f"network {network['network']} {network['wildcard']} area {area}")

    try:
        output = device.send_config_set(commands)
        return True, output
    except Exception as e:
        logger.error(f"Error configuring OSPF: {e}")
        return False, str(e)

def configure_eigrp(device, router_name, eigrp_config):
    """Configure EIGRP on router"""
    commands = []

    as_number = eigrp_config['as_number']

    # EIGRP configuration
    commands.append(f"router eigrp {as_number}")
    commands.append("no auto-summary")

    # Add networks
    networks = eigrp_config['networks'].get(router_name, [])
    for network in networks:
        commands.append(f"network {network['network']} {network['wildcard']}")

    try:
        output = device.send_config_set(commands)
        return True, output
    except Exception as e:
        logger.error(f"Error configuring EIGRP: {e}")
        return False, str(e)

def connect_and_configure(router, username, password, secret, routing_config):
    """Connect to router and configure routing"""
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
        success = False

        # Configure OSPF if enabled
        if routing_config.get('ospf', {}).get('enabled'):
            print(f"  Configuring OSPF... ", end='')
            success, output = configure_ospf(device, router_name, routing_config['ospf'])
            if success:
                print(f"{Fore.GREEN}✓{Style.RESET_ALL}")
                logger.info(f"Successfully configured OSPF on {router_name}")
            else:
                print(f"{Fore.RED}✗{Style.RESET_ALL}")

        # Configure EIGRP if enabled
        if routing_config.get('eigrp', {}).get('enabled'):
            print(f"  Configuring EIGRP... ", end='')
            success, output = configure_eigrp(device, router_name, routing_config['eigrp'])
            if success:
                print(f"{Fore.GREEN}✓{Style.RESET_ALL}")
                logger.info(f"Successfully configured EIGRP on {router_name}")
            else:
                print(f"{Fore.RED}✗{Style.RESET_ALL}")

        # Verify routing
        print(f"  Verifying routing table... ", end='')
        routing_table = device.send_command("show ip route")
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
    print(f"  Routing Protocol Configuration Script")
    print(f"{'='*60}{Style.RESET_ALL}\n")

    # Load credentials
    username = os.getenv('ROUTER_USERNAME')
    password = os.getenv('ROUTER_PASSWORD')
    secret = os.getenv('ROUTER_SECRET')

    if not all([username, password, secret]):
        logger.error("Missing credentials. Please check .env file")
        sys.exit(1)

    # Load configurations
    inventory, routing_config = load_config_files()

    # Check if any routing protocol is enabled
    ospf_enabled = routing_config.get('ospf', {}).get('enabled', False)
    eigrp_enabled = routing_config.get('eigrp', {}).get('enabled', False)

    if not (ospf_enabled or eigrp_enabled):
        logger.warning("No routing protocol is enabled in configuration")
        print(f"{Fore.YELLOW}⚠ No routing protocol is enabled{Style.RESET_ALL}")
        return 0

    print(f"Protocol: {Fore.GREEN}OSPF{Style.RESET_ALL}" if ospf_enabled else f"Protocol: {Fore.GREEN}EIGRP{Style.RESET_ALL}")

    success_count = 0
    fail_count = 0

    # Process each router
    for router in inventory['routers']:
        if connect_and_configure(router, username, password, secret, routing_config):
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
