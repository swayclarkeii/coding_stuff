#!/bin/bash
# Claude Code Environment Backup Script
# Created: January 16, 2026
# Purpose: Backup complete Claude Code environment for migration

set -e  # Exit on error

BACKUP_DIR="$HOME/Desktop/claude-env-backup-$(date +%Y-%m-%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "════════════════════════════════════════════════════════"
echo "  Claude Code Environment Backup"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📦 Backup destination: $BACKUP_DIR"
echo ""

# 1. Claude config
echo "📋 Backing up Claude config..."
if [ -f ~/.claude.json ]; then
    cp ~/.claude.json "$BACKUP_DIR/claude.json"
    echo "   ✓ ~/.claude.json"
else
    echo "   ⚠️  ~/.claude.json not found"
fi

# 2. Credentials
echo ""
echo "🔑 Backing up credentials..."
if [ -d ~/coding_stuff/.credentials ]; then
    mkdir -p "$BACKUP_DIR/credentials"
    cp -r ~/coding_stuff/.credentials/* "$BACKUP_DIR/credentials/" 2>/dev/null || true
    echo "   ✓ ~/coding_stuff/.credentials/"
    ls "$BACKUP_DIR/credentials/" | sed 's/^/     - /'
else
    echo "   ⚠️  ~/coding_stuff/.credentials/ not found"
fi

# 3. Shell config
echo ""
echo "🐚 Backing up shell config..."
if [ -f ~/.zshrc ]; then
    cp ~/.zshrc "$BACKUP_DIR/zshrc"
    echo "   ✓ ~/.zshrc"
else
    echo "   ⚠️  ~/.zshrc not found"
fi

# 4. Secrets (if exists)
echo ""
echo "🔒 Backing up secrets..."
if [ -f ~/.secrets ]; then
    cp ~/.secrets "$BACKUP_DIR/secrets"
    chmod 600 "$BACKUP_DIR/secrets"
    echo "   ✓ ~/.secrets"
else
    echo "   ℹ️  ~/.secrets not found (optional)"
fi

# 5. Scripts
echo ""
echo "📜 Backing up scripts..."
if [ -d ~/coding_stuff/scripts ]; then
    mkdir -p "$BACKUP_DIR/scripts"
    cp -r ~/coding_stuff/scripts/* "$BACKUP_DIR/scripts/" 2>/dev/null || true
    echo "   ✓ ~/coding_stuff/scripts/"
    ls "$BACKUP_DIR/scripts/" | grep -E '\.(sh|py)$' | sed 's/^/     - /'
else
    echo "   ⚠️  ~/coding_stuff/scripts/ not found"
fi

# 6. MCP servers
echo ""
echo "🔌 Backing up custom MCP servers..."
if [ -d ~/coding_stuff/mcp-servers ]; then
    mkdir -p "$BACKUP_DIR/mcp-servers"

    # Copy each MCP server directory
    for server_dir in ~/coding_stuff/mcp-servers/*/; do
        if [ -d "$server_dir" ]; then
            server_name=$(basename "$server_dir")
            echo "   Backing up $server_name..."

            # Create destination directory
            mkdir -p "$BACKUP_DIR/mcp-servers/$server_name"

            # Copy source files (exclude node_modules for now)
            rsync -a --exclude 'node_modules' "$server_dir" "$BACKUP_DIR/mcp-servers/$server_name/" 2>/dev/null || true

            echo "     ✓ $server_name"
        fi
    done
else
    echo "   ⚠️  ~/coding_stuff/mcp-servers/ not found"
fi

# 7. Claude hooks (if customized)
echo ""
echo "🪝 Backing up hooks..."
if [ -d ~/.claude/hooks ]; then
    mkdir -p "$BACKUP_DIR/hooks"
    cp -r ~/.claude/hooks/* "$BACKUP_DIR/hooks/" 2>/dev/null || true
    echo "   ✓ ~/.claude/hooks/"
    ls "$BACKUP_DIR/hooks/" 2>/dev/null | sed 's/^/     - /' || echo "     (empty)"
else
    echo "   ℹ️  ~/.claude/hooks/ not found (optional)"
fi

# 8. Claude settings
echo ""
echo "⚙️  Backing up settings..."
if [ -f ~/.claude/settings.json ]; then
    cp ~/.claude/settings.json "$BACKUP_DIR/settings.json"
    echo "   ✓ ~/.claude/settings.json"
else
    echo "   ℹ️  ~/.claude/settings.json not found (optional)"
fi

# 9. Create README in backup
echo ""
echo "📝 Creating backup README..."
cat > "$BACKUP_DIR/README.txt" << 'EOF'
CLAUDE CODE ENVIRONMENT BACKUP
================================

This backup contains your complete Claude Code environment from your laptop.

CONTENTS:
---------
- claude.json        : Main Claude Code configuration with MCP servers
- zshrc              : Shell configuration with aliases (claudia, mcp-status, etc.)
- credentials/       : API credentials (Google OAuth, service accounts)
- secrets            : Environment variables and sensitive tokens
- scripts/           : Automation scripts (mcp-toggle.sh, monitor-browser-tabs.sh)
- mcp-servers/       : Custom MCP server implementations
- hooks/             : Claude Code hooks (if customized)
- settings.json      : User preferences

RESTORE ON DESKTOP MAC:
-----------------------
1. Transfer this entire folder to your desktop Mac
2. See ENVIRONMENT_BACKUP_GUIDE.md for detailed restore instructions
3. Run the restore script or manually copy files to their locations

IMPORTANT:
----------
- Keep this backup secure (contains API tokens and credentials)
- Delete from USB/cloud after successful migration
- Update paths in claude.json if your desktop username differs
- Run 'npm install' in each mcp-servers subdirectory after restore

For detailed instructions, see:
/Users/swayclarke/coding_stuff/ENVIRONMENT_BACKUP_GUIDE.md
EOF

# 10. Calculate backup size
echo ""
echo "📊 Backup summary:"
BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
FILE_COUNT=$(find "$BACKUP_DIR" -type f | wc -l | tr -d ' ')
echo "   Size: $BACKUP_SIZE"
echo "   Files: $FILE_COUNT"

echo ""
echo "════════════════════════════════════════════════════════"
echo "  ✅ Backup Complete!"
echo "════════════════════════════════════════════════════════"
echo ""
echo "📁 Backup location: $BACKUP_DIR"
echo ""
echo "Next steps:"
echo "  1. Transfer to desktop Mac via USB, scp, or cloud storage"
echo "  2. See README.txt in backup folder for restore instructions"
echo "  3. Full guide: ~/coding_stuff/ENVIRONMENT_BACKUP_GUIDE.md"
echo ""
echo "⚠️  SECURITY: This backup contains API tokens. Keep it secure!"
echo ""
