#!/bin/bash
#
# n8n Server Health Monitor
# Runs locally on Mac, SSHs into DigitalOcean droplet to check health
# Designed to avoid circular dependency (doesn't rely on n8n being up)
#
# Created: 2026-01-22
# Location: /Users/computer/coding_stuff/scripts/n8n-server-monitor.sh

set -euo pipefail

# ============== CONFIGURATION ==============
# Auto-detect paths based on current user
CURRENT_USER=$(whoami)
if [ "$CURRENT_USER" = "swayclarke" ]; then
    CODING_STUFF="/Users/swayclarke/coding_stuff"
elif [ "$CURRENT_USER" = "computer" ]; then
    CODING_STUFF="/Users/computer/coding_stuff"
else
    CODING_STUFF="$HOME/coding_stuff"
fi

SSH_KEY="$CODING_STUFF/.credentials/n8n-server-ssh.key"
SERVER_IP="157.230.21.230"
SERVER_USER="root"
LOG_DIR="$CODING_STUFF/logs"
LOG_FILE="$LOG_DIR/n8n-server-monitor.log"
ALERT_EMAIL="sway@oloxa.ai"

# Thresholds
DISK_WARNING_PERCENT=70
DISK_CRITICAL_PERCENT=85
DISK_EMERGENCY_PERCENT=95
BINARY_DATA_PATH="/var/lib/docker/volumes/n8n_n8n-data/_data/binaryData"

# Auto-cleanup settings
AUTO_CLEANUP_ENABLED=true
CLEANUP_DAYS_WARNING=14    # Delete files older than 14 days at warning level
CLEANUP_DAYS_CRITICAL=7    # Delete files older than 7 days at critical level
CLEANUP_DAYS_EMERGENCY=3   # Delete files older than 3 days at emergency level

# ============== FUNCTIONS ==============

log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"

    # Also echo to stdout if running interactively
    if [ -t 1 ]; then
        echo "[$timestamp] [$level] $message"
    fi
}

send_notification() {
    local title="$1"
    local message="$2"
    local urgency="${3:-normal}"  # normal, critical

    # macOS notification
    osascript -e "display notification \"$message\" with title \"$title\" sound name \"Ping\"" 2>/dev/null || true

    # For critical alerts, also try terminal-notifier if available
    if [ "$urgency" = "critical" ] && command -v terminal-notifier &>/dev/null; then
        terminal-notifier -title "$title" -message "$message" -sound "Basso" -group "n8n-monitor" 2>/dev/null || true
    fi

    log "ALERT" "Notification sent: $title - $message"
}

send_email_alert() {
    local subject="$1"
    local body="$2"
    local sent=false

    # Method 1: Try Mail.app via AppleScript (most reliable on macOS)
    if ! $sent; then
        osascript <<EOF 2>/dev/null && sent=true
tell application "Mail"
    set newMessage to make new outgoing message with properties {subject:"$subject", content:"$body", visible:false}
    tell newMessage
        make new to recipient at end of to recipients with properties {address:"$ALERT_EMAIL"}
    end tell
    send newMessage
end tell
EOF
    fi

    # Method 2: Try mail command as fallback
    if ! $sent; then
        echo "$body" | mail -s "$subject" "$ALERT_EMAIL" 2>/dev/null && sent=true
    fi

    if $sent; then
        log "INFO" "Email alert sent to $ALERT_EMAIL"
        return 0
    else
        log "WARN" "Could not send email alert (all methods failed)"
        log "WARN" "Email subject: $subject"
        return 1
    fi
}

ssh_command() {
    local cmd="$1"
    local timeout="${2:-30}"

    ssh -i "$SSH_KEY" \
        -o ConnectTimeout=10 \
        -o StrictHostKeyChecking=no \
        -o BatchMode=yes \
        -o ServerAliveInterval=5 \
        -o ServerAliveCountMax=2 \
        "$SERVER_USER@$SERVER_IP" \
        "$cmd" 2>&1
}

check_ssh_connection() {
    log "INFO" "Checking SSH connection to $SERVER_IP..."

    if ssh_command "echo 'SSH OK'" 5 | grep -q "SSH OK"; then
        log "INFO" "SSH connection successful"
        return 0
    else
        log "ERROR" "SSH connection FAILED"
        send_notification "n8n Server Alert" "SSH connection to server FAILED! Server may be down." "critical"
        return 1
    fi
}

get_disk_usage() {
    # Returns disk usage percentage as integer
    ssh_command "df -h / | tail -1 | awk '{print \$5}' | tr -d '%'" 10
}

get_binary_data_size() {
    # Returns binaryData folder size in GB
    ssh_command "du -sh $BINARY_DATA_PATH 2>/dev/null | awk '{print \$1}'" 15
}

get_container_status() {
    # Returns container status
    ssh_command "cd /root/n8n && docker compose ps --format 'table {{.Name}}\t{{.Status}}'" 15
}

get_postgres_health() {
    # Check if postgres is accepting connections
    ssh_command "cd /root/n8n && docker compose exec -T postgres pg_isready -U postgres 2>&1" 10
}

cleanup_binary_data() {
    local days="$1"
    log "INFO" "Cleaning up binaryData files older than $days days..."

    local result=$(ssh_command "find $BINARY_DATA_PATH -type f -mtime +$days -delete 2>&1 && echo 'CLEANUP_DONE'" 60)

    if echo "$result" | grep -q "CLEANUP_DONE"; then
        log "INFO" "Cleanup completed successfully"
        return 0
    else
        log "ERROR" "Cleanup failed: $result"
        return 1
    fi
}

restart_containers() {
    log "WARN" "Restarting Docker containers..."

    ssh_command "cd /root/n8n && docker compose restart postgres && sleep 10 && docker compose restart n8n" 120

    log "INFO" "Container restart command sent"
}

restart_ssh_service() {
    log "WARN" "Restarting SSH service..."

    # Note: This requires SSH to already be working (used for recovery after partial failures)
    # For complete SSH failure, use DigitalOcean console
    ssh_command "systemctl restart ssh" 30

    log "INFO" "SSH restart command sent"
}

# ============== MAIN MONITORING LOGIC ==============

main() {
    # Ensure log directory exists
    mkdir -p "$LOG_DIR"

    log "INFO" "========== n8n Server Health Check Started =========="

    # Step 1: Check SSH connection
    if ! check_ssh_connection; then
        send_notification "n8n CRITICAL" "Cannot SSH to server! Manual intervention required." "critical"
        send_email_alert "🔴 n8n Server UNREACHABLE" "Cannot establish SSH connection to $SERVER_IP. The server may be down or SSH service crashed. Check DigitalOcean console immediately."
        log "ERROR" "Health check aborted - SSH unavailable"
        exit 1
    fi

    # Step 2: Check disk usage
    local disk_percent=$(get_disk_usage)

    if ! [[ "$disk_percent" =~ ^[0-9]+$ ]]; then
        log "ERROR" "Could not parse disk usage: $disk_percent"
        disk_percent=0
    fi

    log "INFO" "Disk usage: ${disk_percent}%"

    # Step 3: Get binaryData size
    local binary_size=$(get_binary_data_size)
    log "INFO" "BinaryData size: $binary_size"

    # Step 4: Check container status
    local container_status=$(get_container_status)
    log "INFO" "Container status: $container_status"

    # Step 5: Check PostgreSQL health
    local postgres_health=$(get_postgres_health)
    if echo "$postgres_health" | grep -q "accepting connections"; then
        log "INFO" "PostgreSQL: healthy (accepting connections)"
    else
        log "WARN" "PostgreSQL: may be unhealthy - $postgres_health"
        send_notification "n8n Warning" "PostgreSQL may not be healthy. Check server." "critical"
    fi

    # Step 6: Take action based on disk usage
    if [ "$disk_percent" -ge "$DISK_EMERGENCY_PERCENT" ]; then
        # EMERGENCY: >95%
        log "ERROR" "EMERGENCY: Disk at ${disk_percent}% - AUTO-CLEANUP TRIGGERED"
        send_notification "n8n EMERGENCY" "Disk at ${disk_percent}%! Emergency cleanup running." "critical"
        send_email_alert "🔴 n8n EMERGENCY - Disk ${disk_percent}% Full" "
EMERGENCY: n8n server disk is ${disk_percent}% full!

BinaryData size: $binary_size
Container status:
$container_status

Action taken: Emergency cleanup of files older than $CLEANUP_DAYS_EMERGENCY days.
Containers will be restarted.

Check server status immediately: ssh -i ~/.ssh/n8n root@$SERVER_IP
"

        if [ "$AUTO_CLEANUP_ENABLED" = true ]; then
            cleanup_binary_data "$CLEANUP_DAYS_EMERGENCY"
            restart_containers

            # Re-check disk after cleanup
            sleep 5
            local new_disk=$(get_disk_usage)
            log "INFO" "Disk after emergency cleanup: ${new_disk}%"
            send_notification "n8n Cleanup Done" "Disk now at ${new_disk}% (was ${disk_percent}%)"
        fi

    elif [ "$disk_percent" -ge "$DISK_CRITICAL_PERCENT" ]; then
        # CRITICAL: 85-95%
        log "WARN" "CRITICAL: Disk at ${disk_percent}% - cleanup triggered"
        send_notification "n8n Critical" "Disk at ${disk_percent}%! Auto-cleanup running." "critical"
        send_email_alert "🟠 n8n CRITICAL - Disk ${disk_percent}% Full" "
WARNING: n8n server disk is ${disk_percent}% full.

BinaryData size: $binary_size

Action taken: Cleanup of files older than $CLEANUP_DAYS_CRITICAL days.
"

        if [ "$AUTO_CLEANUP_ENABLED" = true ]; then
            cleanup_binary_data "$CLEANUP_DAYS_CRITICAL"

            local new_disk=$(get_disk_usage)
            log "INFO" "Disk after critical cleanup: ${new_disk}%"
        fi

    elif [ "$disk_percent" -ge "$DISK_WARNING_PERCENT" ]; then
        # WARNING: 70-85%
        log "WARN" "WARNING: Disk at ${disk_percent}%"
        send_notification "n8n Warning" "Disk at ${disk_percent}%. Consider cleanup."

        if [ "$AUTO_CLEANUP_ENABLED" = true ]; then
            cleanup_binary_data "$CLEANUP_DAYS_WARNING"
        fi

    else
        # OK: <70%
        log "INFO" "Disk usage OK: ${disk_percent}%"
    fi

    log "INFO" "========== Health Check Complete =========="
}

# ============== RUN ==============

# Handle arguments
case "${1:-check}" in
    check)
        main
        ;;
    status)
        # Quick status check without actions
        echo "=== n8n Server Quick Status ==="
        echo "SSH: $(check_ssh_connection && echo 'OK' || echo 'FAILED')"
        echo "Disk: $(get_disk_usage)%"
        echo "BinaryData: $(get_binary_data_size)"
        echo "PostgreSQL: $(get_postgres_health | head -1)"
        echo "=== Containers ==="
        get_container_status
        ;;
    cleanup)
        # Manual cleanup
        days="${2:-7}"
        echo "Running manual cleanup (files older than $days days)..."
        cleanup_binary_data "$days"
        echo "Done. New disk usage: $(get_disk_usage)%"
        ;;
    restart)
        # Restart containers
        echo "Restarting containers..."
        restart_containers
        echo "Done."
        ;;
    *)
        echo "Usage: $0 {check|status|cleanup [days]|restart}"
        echo "  check   - Full health check with auto-actions (default)"
        echo "  status  - Quick status without actions"
        echo "  cleanup - Manual cleanup, optionally specify days (default: 7)"
        echo "  restart - Restart docker containers"
        exit 1
        ;;
esac
