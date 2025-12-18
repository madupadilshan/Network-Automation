# DevNetOps Workflow - How It Works

## 🔄 Automation Flow Diagram

```
┌─────────────────┐
│  Network        │
│  Engineer       │
└────────┬────────┘
         │
         │ 1. Edit config files
         │    (interfaces.yml, etc.)
         ▼
┌─────────────────┐
│  Git Commit     │
│  & Push         │
└────────┬────────┘
         │
         │ 2. Push to GitHub
         ▼
┌─────────────────┐
│  GitHub Actions │◄─── Triggered automatically
│  Workflow       │
└────────┬────────┘
         │
         │ 3. Run Python scripts
         ▼
┌─────────────────────────────────┐
│  Validation                      │
│  ├─ Check YAML syntax            │
│  └─ Validate configurations      │
└────────┬────────────────────────┘
         │
         │ 4. Deploy to routers (parallel)
         ▼
    ┌────┴────┐
    │         │
    ▼         ▼
┌──────┐  ┌──────┐  ┌──────┐
│  R1  │  │  R2  │  │  R3  │
│  SSH │  │  SSH │  │  SSH │
└──┬───┘  └──┬───┘  └──┬───┘
   │         │         │
   │ 5. Configure interfaces
   │    Configure routing
   │    Configure VLANs
   │         │         │
   └────┬────┴────┬────┘
        │         │
        │ 6. Verify changes
        ▼         ▼
    ┌──────────────────┐
    │  Backup Configs  │
    └─────────┬────────┘
              │
              │ 7. Commit backups
              ▼
    ┌──────────────────┐
    │  GitHub Repo     │
    │  (backups/)      │
    └──────────────────┘
```

## 📝 Detailed Step-by-Step Process

### Phase 1: Developer Makes Changes

1. **Network engineer edits configuration files**:

   - `configs/interfaces.yml` - IP addresses
   - `configs/routing.yml` - OSPF/EIGRP settings
   - `configs/vlans.yml` - VLAN definitions

2. **Local testing (optional)**:

   ```bash
   python scripts/configure_interfaces.py
   ```

3. **Commit and push changes**:
   ```bash
   git add configs/
   git commit -m "Update R1 interface IPs"
   git push origin main
   ```

### Phase 2: GitHub Actions Triggers

**Trigger Conditions**:

- ✅ Push to `main` branch
- ✅ Changes in `configs/` or `scripts/`
- ✅ Manual trigger via GitHub UI
- ✅ Scheduled (daily at 2 AM for backups)

**Workflow File**: `.github/workflows/deploy.yml`

### Phase 3: Validation Job

```yaml
validate:
  - Checkout code from repository
  - Set up Python environment
  - Install PyYAML
  - Validate all YAML files
  - Check for syntax errors
```

**If validation fails**: Workflow stops, no changes applied

### Phase 4: Deploy Jobs (Parallel Execution)

#### Job 1: Configure Interfaces

```yaml
deploy-interfaces:
  - Connect to each router via SSH
  - Apply interface configurations
  - Set IP addresses
  - Configure descriptions
  - Enable/disable interfaces
  - Save configuration
```

**Script**: `scripts/configure_interfaces.py`

#### Job 2: Configure Routing

```yaml
deploy-routing:
  - Wait for interfaces job to complete
  - Connect to routers
  - Configure OSPF or EIGRP
  - Set router IDs
  - Add network statements
  - Verify routing table
  - Save configuration
```

**Script**: `scripts/configure_routing.py`

#### Job 3: Configure VLANs

```yaml
deploy-vlans:
  - Run in parallel with routing
  - Connect to routers
  - Create subinterfaces
  - Assign VLAN tags
  - Configure IP addresses
  - Enable interfaces
  - Save configuration
```

**Script**: `scripts/configure_vlans.py`

### Phase 5: Backup Job

```yaml
backup-configs:
  - Wait for all deploy jobs
  - Connect to each router
  - Retrieve running-config
  - Save to timestamped file
  - Create latest version
  - Commit to repository
  - Push backup files
```

**Script**: `scripts/backup_configs.py`

**Backup Files**:

- `backups/R1_20250118_143045.txt` (timestamped)
- `backups/R1_latest.txt` (always current)

### Phase 6: Notification

```yaml
notify:
  - Check status of all jobs
  - Create deployment summary
  - Show success/failure status
  - Upload logs as artifacts
```

## 🔐 Security Flow

```
GitHub Secrets ─────┐
(Credentials)       │
                    ▼
              GitHub Actions
                    │
                    │ Encrypted in transit
                    ▼
              Python Scripts
                    │
                    │ SSH connection
                    ▼
               GNS3 Routers
```

**Secrets Used**:

- `ROUTER_USERNAME`: SSH username
- `ROUTER_PASSWORD`: SSH password
- `ROUTER_SECRET`: Enable secret
- `GITHUB_TOKEN`: Auto-generated for commits

## 🎛️ Configuration Management

### File Structure

```
configs/
├── inventory.yml      ─── Router list & IPs
├── interfaces.yml     ─── Interface configs
├── routing.yml        ─── OSPF/EIGRP settings
└── vlans.yml          ─── VLAN definitions
```

### Data Flow

```
YAML File → Python Script → Netmiko Library → SSH → Router CLI
```

## 🚦 Error Handling

```
┌──────────────┐
│  Try Action  │
└──────┬───────┘
       │
   Success? ─── Yes ──→ Continue
       │
      No
       │
       ▼
┌──────────────┐
│  Log Error   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Skip Router │
│  Continue    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Final       │
│  Summary     │
└──────────────┘
```

**Error Recovery**:

- Failed routers are logged
- Other routers continue processing
- Logs uploaded as artifacts
- Summary shows failures

## 📊 Monitoring & Logs

### Log Files Created:

- `interface_config.log`
- `routing_config.log`
- `vlan_config.log`
- `backup.log`

### GitHub Actions Artifacts:

- Interface logs
- Routing logs
- VLAN logs
- Router backups (90-day retention)

### View Logs:

1. Go to GitHub Actions tab
2. Click on workflow run
3. View job logs
4. Download artifacts

## 🔄 Rollback Strategy

### If deployment fails:

**Option 1: Git Revert**

```bash
git revert HEAD
git push origin main
# Re-deploys previous config
```

**Option 2: Manual Restore**

```bash
# Use backup file
scp backups/R1_latest.txt admin@192.168.1.1:
ssh admin@192.168.1.1
copy flash:R1_latest.txt running-config
```

**Option 3: Selective Rollback**

```bash
# Edit config file back to previous state
git checkout HEAD~1 configs/interfaces.yml
git commit -m "Rollback interface changes"
git push
```

## 🎯 Best Practices

1. **Test locally first**: Run scripts manually before pushing
2. **Small changes**: Make incremental updates
3. **Use branches**: Test in feature branches
4. **Review changes**: Use pull requests
5. **Monitor logs**: Check GitHub Actions output
6. **Keep backups**: Regular automated backups
7. **Document changes**: Write clear commit messages

## 🔧 Troubleshooting Workflow

```
Issue? ──→ Check Workflow Status
   │
   ├─ Validation Failed ──→ Fix YAML syntax
   │
   ├─ Connection Error ──→ Check router access
   │
   ├─ Auth Failed ──→ Verify secrets
   │
   └─ Script Error ──→ Review logs
```

## 📈 Workflow Metrics

Track in GitHub Actions:

- **Deployment frequency**: How often changes are pushed
- **Success rate**: Percentage of successful runs
- **Average duration**: Time per deployment
- **Failure patterns**: Common error types

---

**Questions?** Check the main README or open an issue!
