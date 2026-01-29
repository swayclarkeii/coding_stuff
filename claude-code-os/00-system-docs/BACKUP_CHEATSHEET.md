# Environment Backup Cheat Sheet

**Quick reference for syncing Claude Code environment between laptop and desktop**

---

## 🚀 Super Simple Version

### On Laptop:
```bash
env-backup
```
Creates: `~/Desktop/claude-env-backup-YYYY-MM-DD-HHMMSS/`

### Transfer:
- Copy backup folder to USB drive
- Move to desktop Mac
- Put on Desktop

### On Desktop:
```bash
restore-backup
source ~/.zshrc
```

### Test:
```bash
claudia --version
mcp-status
```

**Done!** ✅

---

## 📋 What These Commands Do

### `env-backup`
Backs up:
- Claude Code config (`.claude.json`)
- Shell aliases (`.zshrc`)
- API tokens (`.secrets`)
- MCP servers
- Scripts
- Credentials

### `restore-backup`
Restores:
- All files to correct locations
- Installs npm dependencies
- Updates paths automatically
- Creates backups of existing files

---

## 🔄 Regular Sync Workflow

**Weekly sync between machines:**

1. **Laptop:** `env-backup`
2. **Transfer:** USB/cloud
3. **Desktop:** `restore-backup` + `source ~/.zshrc`

**Takes ~5 minutes total**

---

## 🛟 Troubleshooting

### Commands not found after restore?
```bash
source ~/.zshrc
```

### npm install failed?
```bash
cd ~/coding_stuff/mcp-servers/[server-name]
npm install
```

### Path errors?
The restore script auto-detects username differences and asks to update paths. Always say **yes**.

---

## 📦 Cleanup After Restore

```bash
# Delete backup from Desktop (after verifying it works)
rm -rf ~/Desktop/claude-env-backup-*
```

---

## 🔒 Security Notes

- Backup contains API tokens
- Keep secure during transfer
- Delete from USB/cloud after migration
- Don't commit to public GitHub repos

---

## 📚 Full Documentation

See: `/Users/swayclarke/coding_stuff/ENVIRONMENT_BACKUP_GUIDE.md`
