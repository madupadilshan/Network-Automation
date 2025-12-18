# GNS3 සිංහල Setup Guide

## 🇱🇰 සිංහලෙන් විස්තරය

මේ project එක භාවිතා කරන්න ඔබේ GNS3 එකේ routers හදාගෙන configure කරන්න ඕන.

### 1. GNS3 එකේ Routers හදන්න

1. **GNS3 open කරන්න**
2. **3 Cisco routers add කරන්න** (Cisco IOSv or IOU)

   - Left panel එකෙන් router drag කරන්න
   - R1, R2, R3 ලෙස name කරන්න

3. **Routers connect කරන්න**:

   ```
   R1 Gi0/1 <---> R2 Gi0/1
   R1 Gi0/2 <---> R3 Gi0/1
   R2 Gi0/2 <---> R3 Gi0/2
   ```

4. **Cloud/NAT add කරන්න** management access එකට:
   - Cloud node එකක් add කරන්න
   - එක R1 Gi0/0 එකට connect කරන්න
   - R2, R3 වලටත් එකම විදිහට

### 2. Routers වල Basic Configuration

සෑම router එකක්ම console open කරන්න (right-click → Console) ඔස්සේ මේ commands type කරන්න:

#### R1 Configuration:

```
enable
configure terminal

! Set hostname
hostname R1

! Configure management interface
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown
 exit

! Enable SSH
ip domain-name lab.local
crypto key generate rsa modulus 2048
username admin privilege 15 secret cisco123

! Configure VTY lines for SSH
line vty 0 4
 login local
 transport input ssh
 exit

ip ssh version 2

! Save configuration
write memory
```

#### R2 Configuration:

```
enable
configure terminal

hostname R2

interface GigabitEthernet0/0
 ip address 192.168.1.2 255.255.255.0
 no shutdown
 exit

ip domain-name lab.local
crypto key generate rsa modulus 2048
username admin privilege 15 secret cisco123

line vty 0 4
 login local
 transport input ssh
 exit

ip ssh version 2

write memory
```

#### R3 Configuration:

```
enable
configure terminal

hostname R3

interface GigabitEthernet0/0
 ip address 192.168.1.3 255.255.255.0
 no shutdown
 exit

ip domain-name lab.local
crypto key generate rsa modulus 2048
username admin privilege 15 secret cisco123

line vty 0 4
 login local
 transport input ssh
 exit

ip ssh version 2

write memory
```

### 3. SSH Test කරන්න

ඔබේ computer එකෙන් routers වලට SSH කරන්න පුළුවන්ද බලන්න:

```bash
ssh admin@192.168.1.1
# Password: cisco123
```

### 4. Project Setup කරන්න

```bash
cd C:\DevNetOps-GNS3-Project
pip install -r requirements.txt

# .env file එකක් හදන්න
copy .env.example .env

# notepad .env  (credentials update කරන්න)
```

### 5. Scripts Test කරන්න

```bash
# Test interface configuration
python scripts/configure_interfaces.py

# Test routing
python scripts/configure_routing.py

# Test VLANs
python scripts/configure_vlans.py

# Test backup
python scripts/backup_configs.py
```

### 6. GitHub එකට Push කරන්න

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial DevNetOps project setup"

# GitHub එකේ repository එකක් හදන්න
# ඊට පස්සෙ:
git remote add origin https://github.com/yourusername/DevNetOps-GNS3-Project.git
git branch -M main
git push -u origin main
```

### 7. GitHub Secrets Add කරන්න

1. GitHub repository එකේ **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** click කරන්න
3. මේ secrets add කරන්න:
   - `ROUTER_USERNAME`: `admin`
   - `ROUTER_PASSWORD`: `cisco123`
   - `ROUTER_SECRET`: `cisco123`

### 8. Test Automation

Configuration file එකක් වෙනස් කරලා push කරන්න:

```bash
# configs/interfaces.yml edit කරන්න
git add configs/interfaces.yml
git commit -m "Update interface IP addresses"
git push
```

GitHub Actions automatic ව trigger වෙයි!

## 🎯 දැන් කරන්න පුළුවන් දෙවල්

### Interface IP එකක් වෙනස් කරන්න:

1. `configs/interfaces.yml` edit කරන්න
2. IP address වෙනස් කරන්න
3. Git commit & push කරන්න
4. Auto-deploy වෙයි!

### OSPF වෙනුවට EIGRP use කරන්න:

1. `configs/routing.yml` open කරන්න
2. `ospf: enabled: false`
3. `eigrp: enabled: true`
4. Commit & push

### නව VLAN එකක් add කරන්න:

1. `configs/vlans.yml` edit කරන්න
2. New VLAN entry add කරන්න
3. Commit & push

### Manual backup එකක් run කරන්න:

```bash
python scripts/backup_configs.py
```

## ⚠️ Common Issues

### Connection Timeout

- GNS3 routers running ද check කරන්න
- IP addresses correct ද verify කරන්න
- SSH enabled ද check කරන්න

### Authentication Failed

- Username/password correct ද verify කරන්න
- .env file නිවැරදිද check කරන්න

### Module Not Found

```bash
pip install -r requirements.txt
```

## 📞 Help

Problems තියෙනවනම් GitHub Issues එකේ post කරන්න!

---

**සුභ අංකුරයි!** 🚀
