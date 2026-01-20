# Claude Code Environment Backup & Migration Guide

**Created:** January 16, 2026
**From:** MacBook (Laptop)
**To:** Desktop Mac

---

## Overview

This guide covers backing up and migrating your complete Claude Code environment from laptop to desktop, including:
- Claude Code configuration
- MCP servers and credentials
- Shell aliases and functions
- Scripts and automation tools
- API tokens and credentials

---

## 1. Pre-Migration Checklist

### On Laptop (Source)
- [ ] Save all active Claude Code sessions
- [ ] Document current MCP mode (`mcp-status`)
- [ ] Close all running Claude Code instances
- [ ] Ensure all scripts are committed to git (if applicable)

---

## 2. Files to Backup

### A. Claude Code Configuration

**Location:** `/Users/swayclarke/.claude.json`

This file contains:
- MCP server configurations with credentials
- Project-specific settings
- User preferences and theme
- GitHub tokens, Notion tokens, API keys

**Backup command:**
```bash
cp ~/.claude.json ~/Desktop/claude-config-backup.json
```

### B. Credentials Directory

**Location:** `/Users/swayclarke/coding_stuff/.credentials/`

Contains:
- `gcp-oauth.keys.json` - Google OAuth credentials
- `claude-automation-service-account.json` - Google service account
- Other API credentials

**Backup command:**
```bash
cp -r ~/coding_stuff/.credentials ~/Desktop/credentials-backup/
```

### C. Shell Configuration

**Location:** `~/.zshrc`

Contains:
- `claudia` alias (bypass permissions)
- MCP toggle aliases (`core-mode`, `pa-mode`, `mcp-status`)
- Environment variables (N8N_BASE_URL, N8N_API_KEY)
- Project shortcuts and functions

**Backup command:**
```bash
cp ~/.zshrc ~/Desktop/zshrc-backup
```

### D. Secrets File

**Location:** `~/.secrets`

Contains sensitive environment variables and tokens.

**Backup command:**
```bash
cp ~/.secrets ~/Desktop/secrets-backup
```

⚠️ **Security Note:** Keep this file encrypted or delete after migration!

### E. Scripts Directory

**Location:** `/Users/swayclarke/coding_stuff/scripts/`

Contains:
- `mcp-toggle.sh` - MCP server management
- `monitor-browser-tabs.sh` - Browser monitoring
- `token-status-server.py` - Token monitoring
- Other automation scripts

**Backup command:**
```bash
cp -r ~/coding_stuff/scripts ~/Desktop/scripts-backup/
```

### F. MCP Servers (Custom)

**Locations:**
- `/Users/swayclarke/coding_stuff/mcp-servers/google-calendar-mcp/`
- `/Users/swayclarke/coding_stuff/mcp-servers/google-sheets-mcp/`
- `/Users/swayclarke/coding_stuff/mcp-servers/google-drive-mcp/`
- `/Users/swayclarke/coding_stuff/mcp-servers/mcp-fathom-server/`

**Backup command:**
```bash
cp -r ~/coding_stuff/mcp-servers ~/Desktop/mcp-servers-backup/
```

### G. Claude Code User Directory

**Location:** `~/.claude/`

Contains:
- Session history
- Cached data
- Hooks configuration
- Project settings

**Backup command:**
```bash
cp -r ~/.claude ~/Desktop/claude-user-backup/
```

⚠️ **Note:** This is 423KB+ and may not be necessary. Consider backing up only:
- `~/.claude/hooks/` - Custom hooks
- `~/.claude/settings.json` - User settings

---

## 3. Simple Commands (Recommended!)

**Added to .zshrc for easy use:**

### On Laptop (Backup):
```bash
env-backup
```

That's it! This runs the full backup and creates a timestamped folder on your Desktop.

### On Desktop (Restore):
```bash
restore-backup
```

This automatically finds the latest backup on your Desktop and restores it.

---

## 3a. Quick Backup Script (Technical Details)

The `env-backup` alias runs this script:

```bash
#!/bin/bash
# File: ~/coding_stuff/scripts/backup-claude-env.sh

BACKUP_DIR="$HOME/Desktop/claude-env-backup-$(date +%Y-%m-%d)"
mkdir -p "$BACKUP_DIR"

echo "🔄 Backing up Claude Code environment to: $BACKUP_DIR"

# 1. Claude config
echo "📋 Backing up Claude config..."
cp ~/.claude.json "$BACKUP_DIR/claude.json"

# 2. Credentials
echo "🔑 Backing up credentials..."
cp -r ~/coding_stuff/.credentials "$BACKUP_DIR/credentials/"

# 3. Shell config
echo "🐚 Backing up shell config..."
cp ~/.zshrc "$BACKUP_DIR/zshrc"

# 4. Secrets (if exists)
if [ -f ~/.secrets ]; then
  echo "🔒 Backing up secrets..."
  cp ~/.secrets "$BACKUP_DIR/secrets"
fi

# 5. Scripts
echo "📜 Backing up scripts..."
cp -r ~/coding_stuff/scripts "$BACKUP_DIR/scripts/"

# 6. MCP servers
echo "🔌 Backing up custom MCP servers..."
cp -r ~/coding_stuff/mcp-servers "$BACKUP_DIR/mcp-servers/"

# 7. Claude hooks (if customized)
if [ -d ~/.claude/hooks ]; then
  echo "🪝 Backing up hooks..."
  cp -r ~/.claude/hooks "$BACKUP_DIR/hooks/"
fi

# 8. Claude settings
if [ -f ~/.claude/settings.json ]; then
  echo "⚙️  Backing up settings..."
  cp ~/.claude/settings.json "$BACKUP_DIR/settings.json"
fi

echo "✅ Backup complete: $BACKUP_DIR"
echo ""
echo "📦 Transfer this folder to your desktop Mac:"
echo "   scp -r '$BACKUP_DIR' user@desktop-mac:~/Desktop/"
```

**Make executable and run:**
```bash
chmod +x ~/coding_stuff/scripts/backup-claude-env.sh
~/coding_stuff/scripts/backup-claude-env.sh
```

---

## 4. Transfer to Desktop Mac

### Option A: USB Drive
```bash
# On laptop
cp -r ~/Desktop/claude-env-backup-* /Volumes/YOUR_USB/

# On desktop
cp -r /Volumes/YOUR_USB/claude-env-backup-* ~/Desktop/
```

### Option B: Network Transfer (scp)
```bash
# On laptop (replace with desktop's IP or hostname)
scp -r ~/Desktop/claude-env-backup-* sway@192.168.1.XXX:~/Desktop/
```

### Option C: Cloud Storage
```bash
# Upload to Google Drive, Dropbox, etc.
# Download on desktop Mac
```

---

## 5. Restore on Desktop Mac

### A. Install Prerequisites

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js (required for MCP servers)
brew install node

# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code
```

### B. Restore Files

```bash
#!/bin/bash
# File: restore-claude-env.sh

BACKUP_DIR="$HOME/Desktop/claude-env-backup-YYYY-MM-DD"  # Update date

echo "🔄 Restoring Claude Code environment from: $BACKUP_DIR"

# 1. Restore Claude config
echo "📋 Restoring Claude config..."
cp "$BACKUP_DIR/claude.json" ~/.claude.json

# 2. Create coding_stuff directory structure
echo "📁 Creating directory structure..."
mkdir -p ~/coding_stuff/.credentials
mkdir -p ~/coding_stuff/scripts
mkdir -p ~/coding_stuff/mcp-servers

# 3. Restore credentials
echo "🔑 Restoring credentials..."
cp -r "$BACKUP_DIR/credentials/"* ~/coding_stuff/.credentials/

# 4. Restore shell config
echo "🐚 Restoring shell config..."
cp "$BACKUP_DIR/zshrc" ~/.zshrc

# 5. Restore secrets (if exists)
if [ -f "$BACKUP_DIR/secrets" ]; then
  echo "🔒 Restoring secrets..."
  cp "$BACKUP_DIR/secrets" ~/.secrets
  chmod 600 ~/.secrets
fi

# 6. Restore scripts
echo "📜 Restoring scripts..."
cp -r "$BACKUP_DIR/scripts/"* ~/coding_stuff/scripts/
chmod +x ~/coding_stuff/scripts/*.sh

# 7. Restore MCP servers
echo "🔌 Restoring custom MCP servers..."
cp -r "$BACKUP_DIR/mcp-servers/"* ~/coding_stuff/mcp-servers/

# 8. Restore hooks (if exists)
if [ -d "$BACKUP_DIR/hooks" ]; then
  echo "🪝 Restoring hooks..."
  mkdir -p ~/.claude/hooks
  cp -r "$BACKUP_DIR/hooks/"* ~/.claude/hooks/
fi

# 9. Restore settings (if exists)
if [ -f "$BACKUP_DIR/settings.json" ]; then
  echo "⚙️  Restoring settings..."
  mkdir -p ~/.claude
  cp "$BACKUP_DIR/settings.json" ~/.claude/settings.json
fi

# 10. Set correct permissions
chmod 600 ~/.claude.json
chmod 600 ~/coding_stuff/.credentials/*

# 11. Install npm dependencies for custom MCP servers
echo "📦 Installing MCP server dependencies..."
for dir in ~/coding_stuff/mcp-servers/*/; do
  if [ -f "$dir/package.json" ]; then
    echo "  Installing $(basename $dir)..."
    (cd "$dir" && npm install --production)
  fi
done

echo "✅ Restore complete!"
echo ""
echo "🔄 Next steps:"
echo "1. Reload shell: source ~/.zshrc"
echo "2. Test claudia command: claudia --version"
echo "3. Test MCP status: mcp-status"
echo "4. Update paths in .claude.json if your username differs"
```

### C. Update Paths (If Username Differs)

If your desktop Mac has a different username:

```bash
# Open Claude config
nano ~/.claude.json

# Find and replace all instances of:
# /Users/swayclarke/ → /Users/YOUR_DESKTOP_USERNAME/

# Save and exit (Ctrl+X, Y, Enter)
```

### D. Reload Shell

```bash
source ~/.zshrc
```

---

## 6. Verify Installation

### Test Commands

```bash
# 1. Test claudia alias
claudia --version

# 2. Test MCP toggle
mcp-status

# 3. Test scripts
~/coding_stuff/scripts/mcp-toggle.sh status

# 4. Test browser monitoring
~/coding_stuff/scripts/monitor-browser-tabs.sh status

# 5. Verify environment variables
echo $N8N_BASE_URL
echo $N8N_API_KEY
```

### Test MCP Servers

```bash
# Launch Claude Code in a project
cd ~/coding_stuff
claudia

# In Claude Code chat, test each MCP server:
# - Google Calendar
# - Google Sheets
# - Notion
# - GitHub
# - n8n
# - Playwright/Playwriter
```

---

## 7. Key Aliases & Commands Reference

### Shell Aliases (from .zshrc)

```bash
# Claude Code
claudia                    # Launch Claude Code without permissions

# MCP Management
core-mode                  # Switch to core-mode (n8n, browser, sheets, drive)
pa-mode                    # Switch to PA mode (calendar, github, sheets, notion)
mcp-status                 # Check current MCP configuration
mcp-enable-all             # Enable all MCP servers

# Browser Monitoring
~/coding_stuff/scripts/monitor-browser-tabs.sh check   # Quick check
~/coding_stuff/scripts/monitor-browser-tabs.sh watch   # Continuous monitoring
```

### Important Environment Variables

```bash
N8N_BASE_URL="https://n8n.oloxa.ai"
N8N_API_KEY="eyJhbGci..."  # From .zshrc
```

---

## 8. Credentials & Tokens Inventory

### From .claude.json

- **GitHub:** `[REDACTED - see local backup]`
- **Notion:** `[REDACTED - see local backup]`
- **Fathom:** `[REDACTED - see local backup]`
- **n8n:** `[REDACTED - see local backup]` (in .zshrc and .claude.json)

### From .credentials/

- **gcp-oauth.keys.json** - Google OAuth for Calendar, Drive
- **claude-automation-service-account.json** - Google Sheets service account

---

## 9. Troubleshooting

### Issue: MCP servers not found

**Solution:**
```bash
# Reinstall npm packages for custom MCP servers
cd ~/coding_stuff/mcp-servers/google-calendar-mcp
npm install

cd ~/coding_stuff/mcp-servers/google-sheets-mcp
npm install

# Repeat for other custom servers
```

### Issue: Permission denied on scripts

**Solution:**
```bash
chmod +x ~/coding_stuff/scripts/*.sh
```

### Issue: Credentials not working

**Solution:**
```bash
# Check file permissions
chmod 600 ~/coding_stuff/.credentials/*
chmod 600 ~/.secrets

# Verify paths in .claude.json match your username
```

### Issue: claudia command not found

**Solution:**
```bash
# Reload shell config
source ~/.zshrc

# Or add to .zshrc manually:
alias claudia="claude --dangerously-skip-permissions"
```

---

## 10. Security Recommendations

### After Migration

1. **Delete backup from USB/Cloud:**
   ```bash
   rm -rf ~/Desktop/claude-env-backup-*
   ```

2. **Secure credentials:**
   ```bash
   chmod 600 ~/.claude.json
   chmod 600 ~/.secrets
   chmod 600 ~/coding_stuff/.credentials/*
   ```

3. **Rotate sensitive tokens** (if concerned about exposure during transfer):
   - GitHub Personal Access Token
   - Notion API Token
   - n8n API Key
   - Fathom API Key

4. **Enable FileVault** on desktop Mac for disk encryption

---

## 11. Optional: Git-Based Backup

For easier syncing between machines:

```bash
# On laptop
cd ~/coding_stuff
git init
git add scripts/ .credentials/ (if safe)
git commit -m "Initial backup"
git remote add origin git@github.com:yourusername/claude-env-private.git
git push -u origin main

# On desktop
git clone git@github.com:yourusername/claude-env-private.git ~/coding_stuff
```

⚠️ **Warning:** Do NOT commit credentials to public repos! Use a private repo or .gitignore.

---

## Summary

**Minimum Required Files:**
1. `~/.claude.json` - Core configuration
2. `~/.zshrc` - Aliases and environment variables
3. `~/coding_stuff/.credentials/` - API credentials
4. `~/coding_stuff/scripts/` - Automation scripts
5. `~/coding_stuff/mcp-servers/` - Custom MCP servers

**Total Backup Size:** ~50-100 MB (mostly node_modules in MCP servers)

**Estimated Time:** 15-30 minutes for complete migration

---

**Questions or issues?** Check troubleshooting section or run verification tests.
