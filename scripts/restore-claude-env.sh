#!/bin/bash
# Claude Code Environment Restore Script
# Created: January 16, 2026
# Purpose: Restore Claude Code environment on desktop Mac

set -e  # Exit on error

# Check if backup directory is provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <backup-directory>"
    echo ""
    echo "Example:"
    echo "  $0 ~/Desktop/claude-env-backup-2026-01-16-123456"
    echo ""
    exit 1
fi

BACKUP_DIR="$1"

# Verify backup directory exists
if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ Error: Backup directory not found: $BACKUP_DIR"
    exit 1
fi

echo "════════════════════════════════════════════════════════"
echo "  Claude Code Environment Restore"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📦 Restoring from: $BACKUP_DIR"
echo ""
read -p "⚠️  This will overwrite existing Claude Code configuration. Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi
echo ""

# 1. Restore Claude config
echo "📋 Restoring Claude config..."
if [ -f "$BACKUP_DIR/claude.json" ]; then
    # Backup existing if present
    if [ -f ~/.claude.json ]; then
        cp ~/.claude.json ~/.claude.json.pre-restore-backup
        echo "   ℹ️  Backed up existing config to ~/.claude.json.pre-restore-backup"
    fi
    cp "$BACKUP_DIR/claude.json" ~/.claude.json
    chmod 600 ~/.claude.json
    echo "   ✓ Restored ~/.claude.json"
else
    echo "   ⚠️  claude.json not found in backup"
fi

# 2. Create directory structure
echo ""
echo "📁 Creating directory structure..."
mkdir -p ~/coding_stuff/.credentials
mkdir -p ~/coding_stuff/scripts
mkdir -p ~/coding_stuff/mcp-servers
echo "   ✓ Created ~/coding_stuff directories"

# 3. Restore credentials
echo ""
echo "🔑 Restoring credentials..."
if [ -d "$BACKUP_DIR/credentials" ]; then
    cp -r "$BACKUP_DIR/credentials"/* ~/coding_stuff/.credentials/ 2>/dev/null || true
    chmod 600 ~/coding_stuff/.credentials/* 2>/dev/null || true
    echo "   ✓ Restored credentials to ~/coding_stuff/.credentials/"
    ls ~/coding_stuff/.credentials/ | sed 's/^/     - /'
else
    echo "   ⚠️  credentials/ not found in backup"
fi

# 4. Restore shell config
echo ""
echo "🐚 Restoring shell config..."
if [ -f "$BACKUP_DIR/zshrc" ]; then
    # Backup existing if present
    if [ -f ~/.zshrc ]; then
        cp ~/.zshrc ~/.zshrc.pre-restore-backup
        echo "   ℹ️  Backed up existing config to ~/.zshrc.pre-restore-backup"
    fi
    cp "$BACKUP_DIR/zshrc" ~/.zshrc
    echo "   ✓ Restored ~/.zshrc"
else
    echo "   ⚠️  zshrc not found in backup"
fi

# 5. Restore secrets (if exists)
echo ""
echo "🔒 Restoring secrets..."
if [ -f "$BACKUP_DIR/secrets" ]; then
    # Backup existing if present
    if [ -f ~/.secrets ]; then
        cp ~/.secrets ~/.secrets.pre-restore-backup
        echo "   ℹ️  Backed up existing secrets to ~/.secrets.pre-restore-backup"
    fi
    cp "$BACKUP_DIR/secrets" ~/.secrets
    chmod 600 ~/.secrets
    echo "   ✓ Restored ~/.secrets"
else
    echo "   ℹ️  secrets not found in backup (optional)"
fi

# 6. Restore scripts
echo ""
echo "📜 Restoring scripts..."
if [ -d "$BACKUP_DIR/scripts" ]; then
    cp -r "$BACKUP_DIR/scripts"/* ~/coding_stuff/scripts/ 2>/dev/null || true
    chmod +x ~/coding_stuff/scripts/*.sh 2>/dev/null || true
    chmod +x ~/coding_stuff/scripts/*.py 2>/dev/null || true
    echo "   ✓ Restored scripts to ~/coding_stuff/scripts/"
    ls ~/coding_stuff/scripts/ | grep -E '\.(sh|py)$' | sed 's/^/     - /'
else
    echo "   ⚠️  scripts/ not found in backup"
fi

# 7. Restore MCP servers
echo ""
echo "🔌 Restoring custom MCP servers..."
if [ -d "$BACKUP_DIR/mcp-servers" ]; then
    cp -r "$BACKUP_DIR/mcp-servers"/* ~/coding_stuff/mcp-servers/ 2>/dev/null || true
    echo "   ✓ Restored MCP servers to ~/coding_stuff/mcp-servers/"

    # Install npm dependencies for each server
    echo ""
    echo "📦 Installing MCP server dependencies..."
    for server_dir in ~/coding_stuff/mcp-servers/*/; do
        if [ -f "$server_dir/package.json" ]; then
            server_name=$(basename "$server_dir")
            echo "   Installing $server_name..."
            (cd "$server_dir" && npm install --production > /dev/null 2>&1) && \
                echo "     ✓ $server_name" || \
                echo "     ⚠️  $server_name (install failed - run manually)"
        fi
    done
else
    echo "   ⚠️  mcp-servers/ not found in backup"
fi

# 8. Restore hooks (if exists)
echo ""
echo "🪝 Restoring hooks..."
if [ -d "$BACKUP_DIR/hooks" ]; then
    mkdir -p ~/.claude/hooks
    cp -r "$BACKUP_DIR/hooks"/* ~/.claude/hooks/ 2>/dev/null || true
    echo "   ✓ Restored hooks to ~/.claude/hooks/"
else
    echo "   ℹ️  hooks/ not found in backup (optional)"
fi

# 9. Restore settings (if exists)
echo ""
echo "⚙️  Restoring settings..."
if [ -f "$BACKUP_DIR/settings.json" ]; then
    mkdir -p ~/.claude
    cp "$BACKUP_DIR/settings.json" ~/.claude/settings.json
    echo "   ✓ Restored ~/.claude/settings.json"
else
    echo "   ℹ️  settings.json not found in backup (optional)"
fi

# 10. Check for username differences
LAPTOP_USER=$(grep -o '/Users/[^/]*/' "$BACKUP_DIR/claude.json" 2>/dev/null | head -1 | tr -d '/')
DESKTOP_USER="/Users/$USER"

echo ""
if [ "$LAPTOP_USER" != "$DESKTOP_USER" ]; then
    echo "⚠️  USERNAME MISMATCH DETECTED!"
    echo "   Laptop: $LAPTOP_USER"
    echo "   Desktop: $DESKTOP_USER"
    echo ""
    read -p "   Update paths in claude.json? (Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        # Update paths in claude.json
        sed -i.bak "s|$LAPTOP_USER|$DESKTOP_USER|g" ~/.claude.json
        echo "   ✓ Updated paths in ~/.claude.json"
        echo "   ℹ️  Backup saved to ~/.claude.json.bak"
    fi
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "  ✅ Restore Complete!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo ""
echo "1. Reload shell configuration:"
echo "   source ~/.zshrc"
echo ""
echo "2. Verify installation:"
echo "   claudia --version"
echo "   mcp-status"
echo ""
echo "3. Test MCP servers:"
echo "   cd ~/coding_stuff"
echo "   claudia"
echo ""
echo "4. If npm installs failed, manually run:"
echo "   cd ~/coding_stuff/mcp-servers/[server-name]"
echo "   npm install"
echo ""
echo "5. Clean up backup files (optional):"
echo "   rm -rf $BACKUP_DIR"
echo ""
echo "⚠️  SECURITY: Delete backup from USB/cloud after verifying!"
echo ""
