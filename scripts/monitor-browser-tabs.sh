#!/bin/bash
# Browser Tab Monitor for Playwright MCP
# Monitors tab count and alerts when threshold is exceeded

# Configuration
TAB_THRESHOLD=5
ALERT_FILE="/tmp/browser-tab-alert.txt"
LOG_FILE="/tmp/browser-tab-monitor.log"

# Color codes for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Function to get current tab count from Playwright
get_tab_count() {
    # Count Chrome windows/tabs with "about:blank" or "Agents" in title
    # This is a heuristic - actual Playwright MCP integration would use MCP tools
    local count=$(osascript -e 'tell application "Google Chrome"
        set tabCount to 0
        repeat with w in windows
            set tabCount to tabCount + (count of tabs of w)
        end repeat
        return tabCount
    end tell' 2>/dev/null)

    echo "${count:-0}"
}

# Function to log message
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Function to check and alert
check_tabs() {
    local tab_count=$(get_tab_count)
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    log_message "Tab count: $tab_count"

    if [ "$tab_count" -gt "$TAB_THRESHOLD" ]; then
        # Create alert
        echo "⚠️  BROWSER TAB ALERT" > "$ALERT_FILE"
        echo "Time: $timestamp" >> "$ALERT_FILE"
        echo "Current tabs: $tab_count" >> "$ALERT_FILE"
        echo "Threshold: $TAB_THRESHOLD" >> "$ALERT_FILE"
        echo "" >> "$ALERT_FILE"
        echo "ACTION REQUIRED:" >> "$ALERT_FILE"
        echo "1. Check for about:blank loop in browser" >> "$ALERT_FILE"
        echo "2. Close unnecessary tabs" >> "$ALERT_FILE"
        echo "3. If loop detected, close browser entirely" >> "$ALERT_FILE"

        # Display alert
        echo -e "${RED}════════════════════════════════════════════${NC}"
        echo -e "${RED}⚠️  BROWSER TAB ALERT${NC}"
        echo -e "${RED}════════════════════════════════════════════${NC}"
        echo -e "${YELLOW}Time:${NC} $timestamp"
        echo -e "${YELLOW}Current tabs:${NC} ${RED}$tab_count${NC} (threshold: $TAB_THRESHOLD)"
        echo ""
        echo -e "${YELLOW}ACTION REQUIRED:${NC}"
        echo "  1. Check for about:blank loop in Chrome"
        echo "  2. Close unnecessary tabs manually"
        echo "  3. If loop detected, close browser entirely"
        echo "  4. Alert saved to: $ALERT_FILE"
        echo -e "${RED}════════════════════════════════════════════${NC}"

        log_message "ALERT: Tab count ($tab_count) exceeds threshold ($TAB_THRESHOLD)"
        return 1
    else
        # Clear alert if exists
        [ -f "$ALERT_FILE" ] && rm "$ALERT_FILE"

        echo -e "${GREEN}✓${NC} Browser tabs: $tab_count (threshold: $TAB_THRESHOLD)"
        log_message "OK: Tab count within threshold"
        return 0
    fi
}

# Main execution
main() {
    local mode="${1:-check}"

    case "$mode" in
        check)
            check_tabs
            ;;
        watch)
            echo "Starting browser tab monitor (checking every 30 seconds)..."
            echo "Press Ctrl+C to stop"
            echo ""
            while true; do
                check_tabs
                sleep 30
            done
            ;;
        status)
            local tab_count=$(get_tab_count)
            echo "Current browser tabs: $tab_count"
            if [ -f "$ALERT_FILE" ]; then
                echo ""
                cat "$ALERT_FILE"
            fi
            ;;
        clean)
            echo "Cleaning up monitor files..."
            rm -f "$ALERT_FILE" "$LOG_FILE"
            echo "Done."
            ;;
        *)
            echo "Usage: $0 {check|watch|status|clean}"
            echo ""
            echo "Commands:"
            echo "  check   - Check tab count once (default)"
            echo "  watch   - Continuously monitor tabs (30s interval)"
            echo "  status  - Show current status and any alerts"
            echo "  clean   - Remove alert and log files"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
