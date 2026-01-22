#!/bin/bash
#
# Setup script for n8n Server Health Monitor
# Run this on any Mac (laptop or desktop) to set up local monitoring
#
# Usage: ./setup-n8n-monitor.sh
#

set -euo pipefail

echo "=========================================="
echo "  n8n Server Monitor - Setup Script"
echo "=========================================="
echo ""

# Detect the current user's home directory
HOME_DIR="$HOME"
CURRENT_USER=$(whoami)

# Determine the coding_stuff path based on user
if [ "$CURRENT_USER" = "swayclarke" ]; then
    CODING_STUFF="/Users/swayclarke/coding_stuff"
elif [ "$CURRENT_USER" = "computer" ]; then
    CODING_STUFF="/Users/computer/coding_stuff"
else
    echo "Unknown user: $CURRENT_USER"
    echo "Please set CODING_STUFF path manually in this script"
    exit 1
fi

echo "Detected user: $CURRENT_USER"
echo "Coding stuff path: $CODING_STUFF"
echo ""

# Paths
SCRIPT_PATH="$CODING_STUFF/scripts/n8n-server-monitor.sh"
SSH_KEY="$CODING_STUFF/.credentials/n8n-server-ssh.key"
LOG_DIR="$CODING_STUFF/logs"
PLIST_NAME="ai.oloxa.n8n-server-monitor.plist"
PLIST_PATH="$HOME_DIR/Library/LaunchAgents/$PLIST_NAME"

# Step 1: Check if monitor script exists
echo "[1/6] Checking monitor script..."
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "ERROR: Monitor script not found at $SCRIPT_PATH"
    echo "Make sure coding_stuff is synced from GitHub first."
    exit 1
fi
echo "      Found: $SCRIPT_PATH"

# Step 2: Check if SSH key exists
echo "[2/6] Checking SSH key..."
if [ ! -f "$SSH_KEY" ]; then
    echo "ERROR: SSH key not found at $SSH_KEY"
    echo "Make sure .credentials folder is synced."
    exit 1
fi
echo "      Found: $SSH_KEY"

# Step 3: Set correct permissions on SSH key
echo "[3/6] Setting SSH key permissions..."
chmod 600 "$SSH_KEY"
echo "      Permissions set to 600"

# Step 4: Create logs directory
echo "[4/6] Creating logs directory..."
mkdir -p "$LOG_DIR"
echo "      Created: $LOG_DIR"

# Step 5: Create LaunchAgent plist
echo "[5/6] Creating LaunchAgent..."

# Make sure LaunchAgents directory exists
mkdir -p "$HOME_DIR/Library/LaunchAgents"

cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.oloxa.n8n-server-monitor</string>

    <key>ProgramArguments</key>
    <array>
        <string>$SCRIPT_PATH</string>
        <string>check</string>
    </array>

    <key>StartInterval</key>
    <integer>300</integer>

    <key>RunAtLoad</key>
    <true/>

    <key>StandardOutPath</key>
    <string>$LOG_DIR/n8n-server-monitor-launchd.log</string>

    <key>StandardErrorPath</key>
    <string>$LOG_DIR/n8n-server-monitor-launchd-error.log</string>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
    </dict>

    <key>Nice</key>
    <integer>10</integer>

    <key>ProcessType</key>
    <string>Background</string>
</dict>
</plist>
EOF

echo "      Created: $PLIST_PATH"

# Step 6: Load the LaunchAgent
echo "[6/6] Loading LaunchAgent..."

# Unload first if already loaded (ignore errors)
launchctl unload "$PLIST_PATH" 2>/dev/null || true

# Load the new plist
launchctl load "$PLIST_PATH"

echo "      LaunchAgent loaded!"
echo ""

# Verify it's running
echo "=========================================="
echo "  Verifying Setup"
echo "=========================================="
echo ""

if launchctl list | grep -q "ai.oloxa.n8n-server-monitor"; then
    echo "LaunchAgent status: RUNNING"
else
    echo "LaunchAgent status: NOT RUNNING (may need login/logout)"
fi

echo ""
echo "Testing monitor script..."
echo ""
"$SCRIPT_PATH" status

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "The monitor will now run every 5 minutes and:"
echo "  - Check server health via SSH"
echo "  - Auto-cleanup binary data when disk > 70%"
echo "  - Send macOS notifications for issues"
echo "  - Send email alerts for critical issues"
echo ""
echo "Commands:"
echo "  $SCRIPT_PATH status   - Quick status check"
echo "  $SCRIPT_PATH check    - Full health check with actions"
echo "  $SCRIPT_PATH cleanup  - Manual cleanup"
echo ""
echo "Logs: $LOG_DIR/n8n-server-monitor.log"
echo ""
