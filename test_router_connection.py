#!/usr/bin/env python3
"""
Quick test script to check router connectivity via telnet
"""

from netmiko import ConnectHandler
import sys

# Router connection details for GNS3
routers = [
    {
        'router_name': 'R1',
        'device_type': 'cisco_ios_telnet',
        'host': 'localhost',
        'port': 5003,
        'username': 'admin',
        'password': 'cisco123',
        'secret': 'cisco',
    },
    {
        'router_name': 'R2',
        'device_type': 'cisco_ios_telnet',
        'host': 'localhost',
        'port': 5004,  # Assuming R2 is on next port
        'username': 'admin',
        'password': 'cisco123',
        'secret': 'cisco',
    },
    {
        'router_name': 'R3',
        'device_type': 'cisco_ios_telnet',
        'host': 'localhost',
        'port': 5005,  # Assuming R3 is on next port
        'username': 'admin',
        'password': 'cisco123',
        'secret': 'cisco',
    }
]

def test_router(router_info):
    """Test connection to a single router"""
    router_name = router_info.pop('router_name')
    print(f"\n{'='*60}")
    print(f"Testing {router_name} on port {router_info['port']}...")
    print('='*60)
    
    try:
        # Connect to router
        device = ConnectHandler(**router_info)
        router_info['router_name'] = router_name
        device.enable()
        
        print(f"✓ Connected to {router_name}!")
        
        # Get hostname
        hostname = device.send_command("show run | include hostname")
        print(f"\n{hostname}")
        
        # Get interface status
        print("\nInterface Status:")
        print("-" * 60)
        interfaces = device.send_command("show ip interface brief")
        print(interfaces)
        
        # Check if SSH is configured
        print("\nSSH Configuration:")
        print("-" * 60)
        ssh_config = device.send_command("show ip ssh")
        print(ssh_config)
        
        # Check users
        print("\nConfigured Users:")
        print("-" * 60)
        users = device.send_command("show run | include username")
        print(users)
        
        device.disconnect()
        return True
        
    except Exception as e:
        print(f"✗ Failed to connect to {router_name}: {str(e)}")
        router_info['router_name'] = router_name
        return False

# Test all routers
print("\n" + "="*60)
print("  GNS3 Router Configuration Check")
print("="*60)

success_count = 0
for router in routers:
    if test_router(router):
        success_count += 1

print(f"\n{'='*60}")
print(f"Summary: {success_count}/{len(routers)} routers accessible")
print('='*60 + "\n")

sys.exit(0 if success_count == len(routers) else 1)
