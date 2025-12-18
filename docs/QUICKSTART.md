# Quick Start Guide

## 🚀 5 Minutes Setup

### Prerequisites

- ✅ GNS3 installed and running
- ✅ 3 Cisco IOS routers in GNS3
- ✅ Python 3.8+ installed
- ✅ Git installed
- ✅ GitHub account

### Step 1: Clone Project (30 seconds)

```bash
git clone https://github.com/yourusername/DevNetOps-GNS3-Project.git
cd DevNetOps-GNS3-Project
```

### Step 2: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

### Step 3: Configure Routers (2 minutes)

Copy-paste these commands into each router console:

**R1:**

```
enable
conf t
hostname R1
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
ip domain-name lab.local
crypto key generate rsa modulus 2048
username admin privilege 15 secret cisco123
line vty 0 4
 login local
 transport input ssh
ip ssh version 2
end
write memory
```

**R2:** (Change IP to 192.168.1.2)

```
enable
conf t
hostname R2
interface GigabitEthernet0/0
 ip address 192.168.1.2 255.255.255.0
 no shutdown
ip domain-name lab.local
crypto key generate rsa modulus 2048
username admin privilege 15 secret cisco123
line vty 0 4
 login local
 transport input ssh
ip ssh version 2
end
write memory
```

**R3:** (Change IP to 192.168.1.3)

```
enable
conf t
hostname R3
interface GigabitEthernet0/0
 ip address 192.168.1.3 255.255.255.0
 no shutdown
ip domain-name lab.local
crypto key generate rsa modulus 2048
username admin privilege 15 secret cisco123
line vty 0 4
 login local
 transport input ssh
ip ssh version 2
end
write memory
```

### Step 4: Setup Environment (30 seconds)

```bash
copy .env.example .env
# Edit .env if needed (default credentials work)
```

### Step 5: Test Scripts (1 minute)

```bash
# Test backup (safest to start with)
python scripts/backup_configs.py

# If successful, test interface config
python scripts/configure_interfaces.py
```

### Step 6: Setup GitHub Actions (30 seconds)

1. Create new repo on GitHub
2. Go to Settings → Secrets → Actions
3. Add these secrets:
   - `ROUTER_USERNAME`: admin
   - `ROUTER_PASSWORD`: cisco123
   - `ROUTER_SECRET`: cisco123

### Step 7: Push and Deploy! (30 seconds)

```bash
git remote add origin https://github.com/yourusername/DevNetOps-GNS3-Project.git
git add .
git commit -m "Initial setup"
git push -u origin main
```

🎉 **Done!** GitHub Actions will automatically run!

---

## 🎯 Quick Commands Reference

### Daily Tasks

**Change Interface IP:**

```bash
# Edit configs/interfaces.yml
notepad configs\interfaces.yml
git add configs/interfaces.yml
git commit -m "Update R1 interface IP"
git push
```

**Change Routing Protocol:**

```bash
# Edit configs/routing.yml (switch OSPF/EIGRP)
notepad configs\routing.yml
git add configs/routing.yml
git commit -m "Switch to EIGRP"
git push
```

**Add New VLAN:**

```bash
# Edit configs/vlans.yml
notepad configs\vlans.yml
git add configs/vlans.yml
git commit -m "Add VLAN 40"
git push
```

**Manual Backup:**

```bash
python scripts/backup_configs.py
git add backups/
git commit -m "Manual backup"
git push
```

### Troubleshooting

**Test Connection:**

```bash
ssh admin@192.168.1.1
# Password: cisco123
```

**View Logs:**

```bash
type interface_config.log
type routing_config.log
type vlan_config.log
type backup.log
```

**Check Router Status:**

```bash
python -c "from netmiko import ConnectHandler; device = ConnectHandler(device_type='cisco_ios', ip='192.168.1.1', username='admin', password='cisco123'); print(device.send_command('show ip int brief'))"
```

**Validate YAML:**

```bash
python -c "import yaml; yaml.safe_load(open('configs/interfaces.yml'))"
```

---

## 📋 Common Issues & Quick Fixes

### 1. "Connection Timeout"

```bash
# Check if GNS3 routers are running
# Verify IPs in configs/inventory.yml
# Test SSH: ssh admin@192.168.1.1
```

### 2. "Authentication Failed"

```bash
# Verify .env file exists
# Check credentials in .env match router config
# Re-generate SSH keys on router if needed
```

### 3. "Module Not Found"

```bash
pip install -r requirements.txt
```

### 4. "YAML Syntax Error"

```bash
# Use online YAML validator
# Check indentation (use spaces, not tabs)
```

### 5. "GitHub Actions Not Running"

```bash
# Check .github/workflows/deploy.yml exists
# Verify secrets are set in GitHub
# Check if push was to main branch
```

---

## 🔄 Workflow Triggers

| Action       | Trigger    | Jobs Run             |
| ------------ | ---------- | -------------------- |
| `git push`   | Auto       | All configs + backup |
| Schedule     | Daily 2 AM | Backup only          |
| Manual       | GitHub UI  | Select which task    |
| Pull Request | Auto       | Validation only      |

---

## 📊 Project Structure Quick View

```
DevNetOps-GNS3-Project/
├── configs/           # ← Edit these files
│   ├── inventory.yml
│   ├── interfaces.yml
│   ├── routing.yml
│   └── vlans.yml
├── scripts/           # ← Python automation
│   ├── configure_interfaces.py
│   ├── configure_routing.py
│   ├── configure_vlans.py
│   └── backup_configs.py
├── backups/           # ← Auto-generated
├── .github/
│   └── workflows/
│       └── deploy.yml # ← GitHub Actions
├── .env              # ← Your credentials
└── README.md
```

---

## 🎓 Learning Path

**Day 1:** Setup & Basic Testing

- Install and configure
- Test manual scripts
- Understand YAML files

**Day 2:** GitHub Integration

- Setup GitHub Actions
- Make first automated deployment
- Monitor workflow

**Day 3:** Customization

- Add your own routers
- Modify configurations
- Create custom tasks

**Day 4:** Advanced

- Add error handling
- Setup notifications
- Integrate with monitoring

---

## 💡 Pro Tips

1. **Always backup first**: Run backup script before making changes
2. **Test locally**: Use manual scripts before pushing to GitHub
3. **Small commits**: Make one change at a time
4. **Watch the logs**: Monitor GitHub Actions output
5. **Use branches**: Test major changes in feature branches

---

## 🆘 Get Help

- 📖 Full docs: [README.md](../README.md)
- 🇱🇰 Sinhala guide: [GNS3_SETUP_SINHALA.md](GNS3_SETUP_SINHALA.md)
- 🔄 Workflow details: [WORKFLOW.md](WORKFLOW.md)
- 🐛 Issues: GitHub Issues tab

---

**Happy Automating!** 🚀
