# DevNetOps GNS3 Automation Project

## 🌐 සිංහලෙන් විස්තරය

මේක network engineer කෙනෙක්ට GNS3 එකේ Cisco routers 3ක් automate කරන්න හදපු project එකක්. GitHub එකට code push කරාම automatic ව routers වල configurations වෙනස් වෙනවා.

## 📋 Project Overview

This DevNetOps project automates common network engineering tasks on 3 Cisco IOS routers in GNS3 using:

- **Python** with Netmiko for device automation
- **GitHub Actions** for CI/CD pipeline
- **Ansible** (optional) for configuration management
- **YAML** configuration files for easy management

## 🎯 Automated Tasks

1. **Interface IP Configuration** - Assign IPs to router interfaces
2. **OSPF/EIGRP Routing** - Configure dynamic routing protocols
3. **VLAN Management** - Create and manage VLANs
4. **Configuration Backup** - Backup running configs to GitHub

## 🏗️ Network Topology

```
        Cloud1
          |
    [R1]─────[R2]─────[R3]
    .1        .2        .3
```

## 📁 Project Structure

```
DevNetOps-GNS3-Project/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions workflow
├── scripts/
│   ├── configure_interfaces.py # Task 1: IP configuration
│   ├── configure_routing.py    # Task 2: OSPF/EIGRP setup
│   ├── configure_vlans.py      # Task 3: VLAN management
│   └── backup_configs.py       # Task 4: Backup configs
├── configs/
│   ├── inventory.yml           # Router inventory
│   ├── interfaces.yml          # Interface configurations
│   ├── routing.yml             # Routing configurations
│   └── vlans.yml               # VLAN configurations
├── backups/                    # Config backups stored here
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## 🚀 Setup Instructions

### 1. GNS3 Setup

1. Open GNS3 and create 3 Cisco IOS routers (R1, R2, R3)
2. Configure basic connectivity:
   ```
   R1: 192.168.1.1
   R2: 192.168.1.2
   R3: 192.168.1.3
   ```
3. Enable SSH on all routers:

   ```
   Router(config)# hostname R1
   Router(config)# ip domain-name lab.local
   Router(config)# crypto key generate rsa modulus 2048
   Router(config)# username admin privilege 15 secret cisco123
   Router(config)# line vty 0 4
   Router(config-line)# login local
   Router(config-line)# transport input ssh
   Router(config-line)# exit
   Router(config)# ip ssh version 2
   ```

4. Configure management interface (example for R1):
   ```
   Router(config)# interface GigabitEthernet0/0
   Router(config-if)# ip address 192.168.1.1 255.255.255.0
   Router(config-if)# no shutdown
   ```

### 2. Local Development Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/DevNetOps-GNS3-Project.git
   cd DevNetOps-GNS3-Project
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create `.env` file from template:

   ```bash
   copy .env.example .env
   ```

4. Edit `.env` with your router credentials:
   ```
   ROUTER_USERNAME=admin
   ROUTER_PASSWORD=cisco123
   ROUTER_SECRET=cisco123
   ```

### 3. Test Manual Execution

Test each script manually before using GitHub Actions:

```bash
# Test interface configuration
python scripts/configure_interfaces.py

# Test routing configuration
python scripts/configure_routing.py

# Test VLAN configuration
python scripts/configure_vlans.py

# Test backup
python scripts/backup_configs.py
```

### 4. GitHub Actions Setup

1. Add repository secrets in GitHub:

   - Go to: Settings → Secrets and variables → Actions
   - Add secrets:
     - `ROUTER_USERNAME`: admin
     - `ROUTER_PASSWORD`: cisco123
     - `ROUTER_SECRET`: cisco123

2. Push changes to trigger automation:
   ```bash
   git add .
   git commit -m "Update router configurations"
   git push origin main
   ```

## 🔄 How It Works

1. **Developer makes changes** to YAML config files
2. **Commits and pushes** to GitHub
3. **GitHub Actions triggers** automatically
4. **Scripts execute** and configure routers
5. **Configs backed up** to repository
6. **Notifications sent** on success/failure

## 📝 Configuration Files

### `configs/interfaces.yml`

Define interface IPs for all routers.

### `configs/routing.yml`

Configure OSPF or EIGRP parameters.

### `configs/vlans.yml`

Define VLANs and assignments.

### `configs/inventory.yml`

Router IP addresses and connection details.

## 🛠️ Common Tasks

### Change Interface IP

1. Edit `configs/interfaces.yml`
2. Commit and push
3. GitHub Actions will apply changes

### Add New VLAN

1. Edit `configs/vlans.yml`
2. Commit and push
3. VLANs created automatically

### Backup Configs Manually

```bash
python scripts/backup_configs.py
```

## 📊 Workflow Triggers

- **Push to main**: Full deployment
- **Pull Request**: Validation only
- **Manual trigger**: Via GitHub Actions UI
- **Scheduled**: Daily backup at 2 AM UTC

## ⚠️ Important Notes

1. **GNS3 must be running** when GitHub Actions execute
2. **Routers must be accessible** via network
3. **SSH must be enabled** on all routers
4. **Use strong passwords** in production
5. **Test in lab** before production use

## 🔒 Security Best Practices

- Never commit passwords to repository
- Use GitHub Secrets for credentials
- Enable SSH key authentication when possible
- Regularly rotate credentials
- Review audit logs

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📚 Resources

- [Netmiko Documentation](https://github.com/ktbyers/netmiko)
- [GNS3 Documentation](https://docs.gns3.com/)
- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Cisco IOS Command Reference](https://www.cisco.com/c/en/us/support/ios-nx-os-software/ios-15-4m-t/products-command-reference-list.html)

## 🐛 Troubleshooting

### Connection Timeout

- Check GNS3 routers are running
- Verify IP addresses in `inventory.yml`
- Test manual SSH connection

### Authentication Failed

- Verify credentials in `.env` or GitHub Secrets
- Check router user configuration

### Script Errors

- Check Python version (3.8+)
- Verify all dependencies installed
- Review error logs in GitHub Actions

## 📄 License

MIT License

## 👨‍💻 Author

Network DevOps Engineer

---

**ස්තූතියි!** Questions? Open an issue on GitHub.
