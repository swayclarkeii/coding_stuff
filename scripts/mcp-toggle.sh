#!/bin/bash
# MCP Server Toggle Script
# Manage Claude Code MCP servers to reduce token usage

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Config file path
CONFIG_FILE="$HOME/.claude.json"
PROJECT_PATH="/Users/computer/coding_stuff"

# Display usage
usage() {
    cat <<EOF
${BLUE}MCP Server Toggle Script${NC}

Usage: ./mcp-toggle.sh <command>

Commands:
  ${GREEN}status${NC}           Show current MCP server status
  ${GREEN}enable-all${NC}       Enable all MCP servers
  ${GREEN}core-mode${NC}        Enable core servers (n8n, playwriter, playwright, google-sheets, google-drive)
  ${GREEN}google-mode${NC}      Enable Google workspace mode (n8n, google-sheets, google-drive, google-slides)
  ${GREEN}pa-mode${NC}          Enable PA mode (n8n, calendar, github, sheets, notion)
  ${GREEN}minimal${NC}          Enable minimal set (n8n only)
  ${GREEN}disable-all${NC}      Disable all MCP servers
  ${GREEN}list${NC}             List all available MCP servers

Token Costs (per conversation):
  - notion:          ~20,388 tokens (21 tools)
  - google-calendar: ~8,700 tokens (12 tools)
  - github-mcp:      ~5,201 tokens (26 tools)
  - google-sheets:   ~8,000-10,000 tokens (est.)
  - google-drive:    ~8,000-10,000 tokens (est.)
  - n8n-mcp:         ~6,575 tokens (20 tools)
  - playwriter:      ~5,090 tokens (2 tools)

Examples:
  ./mcp-toggle.sh core-mode      # Daily work mode (saves ~34K tokens)
  ./mcp-toggle.sh pa-mode        # PA work: n8n + calendar + github + sheets + notion
  ./mcp-toggle.sh enable-all     # Full feature set (all 11 servers)

EOF
    exit 0
}

# Print colored status
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if jq is available
check_jq() {
    if ! command -v jq &> /dev/null; then
        print_error "jq is not installed. Install it with: brew install jq"
        exit 1
    fi
}

# Check if config file exists
check_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        print_error "Config file not found: $CONFIG_FILE"
        exit 1
    fi
}

# Show current status
show_status() {
    print_status "Current MCP Server Configuration:"
    echo ""

    # Read disabled servers from config
    DISABLED=$(jq -r --arg proj "$PROJECT_PATH" '.projects[$proj].disabledMcpServers[]' "$CONFIG_FILE" 2>/dev/null | sort)

    # All defined servers
    ALL_SERVERS=$(jq -r --arg proj "$PROJECT_PATH" '.projects[$proj].mcpServers | keys[]' "$CONFIG_FILE" 2>/dev/null | sort)

    echo -e "${GREEN}Enabled Servers:${NC}"
    for server in $ALL_SERVERS; do
        if ! echo "$DISABLED" | grep -q "^$server$"; then
            echo "  ✓ $server"
        fi
    done

    echo ""
    echo -e "${YELLOW}Disabled Servers:${NC}"
    if [ -z "$DISABLED" ]; then
        echo "  (none)"
    else
        echo "$DISABLED" | while read -r server; do
            echo "  ✗ $server"
        done
    fi
}

# Update disabled servers list
update_disabled_servers() {
    local disabled_array="$1"

    # Create backup
    cp "$CONFIG_FILE" "$CONFIG_FILE.backup"

    # Update the disabledMcpServers array
    jq --arg proj "$PROJECT_PATH" \
       --argjson disabled "$disabled_array" \
       '.projects[$proj].disabledMcpServers = $disabled' \
       "$CONFIG_FILE" > "$CONFIG_FILE.tmp"

    mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"

    print_success "Configuration updated"
    print_status "Changes will take effect in next Claude Code session"
}

# Core servers (always needed for daily work)
CORE_SERVERS=(
    "n8n-mcp"
    "playwriter"
    "playwright"
    "google-sheets"
    "google-drive"
)

# PA mode servers (focused personal assistant work)
PA_SERVERS=(
    "n8n-mcp"
    "google-calendar"
    "github-mcp"
    "google-sheets"
    "notion"
)

# Optional servers (high token cost, use when needed)
OPTIONAL_SERVERS=(
    "google-slides"
    "google-docs"
)

# Google mode servers (Google workspace + n8n)
GOOGLE_SERVERS=(
    "n8n-mcp"
    "google-sheets"
    "google-drive"
    "google-slides"
)

# Enable core mode
enable_core() {
    print_status "Enabling core mode (n8n, playwriter, playwright, google-sheets, google-drive)..."

    # Disable: PA additions + optional servers
    DISABLED='["notion","google-calendar","fathom","github-mcp","google-slides","google-docs"]'

    update_disabled_servers "$DISABLED"

    print_success "Core mode enabled"
    print_status "Token savings: ~34,000 tokens per conversation"
    echo ""
    show_status
}

# Enable PA mode (focused: n8n, calendar, github, sheets, notion)
enable_pa_mode() {
    print_status "Enabling PA mode (n8n, calendar, github, sheets, notion)..."

    # Disable: playwriter, playwright, drive, fathom, slides, docs
    DISABLED='["playwriter","playwright","google-drive","fathom","google-slides","google-docs"]'

    update_disabled_servers "$DISABLED"

    print_success "PA mode enabled"
    print_status "Includes: n8n-mcp + google-calendar + github + google-sheets + notion"
    print_status "Token cost: ~40,000-44,000 tokens per conversation"
    echo ""
    show_status
}

# Enable Google mode (Google workspace + n8n)
enable_google_mode() {
    print_status "Enabling Google mode (n8n, google-sheets, google-drive, google-slides)..."

    # Disable: everything except Google servers + n8n
    DISABLED='["playwriter","playwright","notion","google-calendar","fathom","github-mcp","google-docs"]'

    update_disabled_servers "$DISABLED"

    print_success "Google mode enabled"
    print_status "Includes: n8n-mcp + google-sheets + google-drive + google-slides"
    echo ""
    show_status
}

# Enable all servers
enable_all() {
    print_status "Enabling all MCP servers..."

    # Disable: none
    DISABLED='[]'

    update_disabled_servers "$DISABLED"

    print_success "All servers enabled"
    print_warning "Token cost: ~51,770 tokens per conversation"
    echo ""
    show_status
}

# Minimal mode (n8n only)
enable_minimal() {
    print_status "Enabling minimal mode (n8n-mcp only)..."

    # Disable: everything except n8n-mcp
    DISABLED='["playwriter","playwright","google-sheets","google-drive","notion","google-calendar","fathom","github-mcp","google-slides","google-docs"]'

    update_disabled_servers "$DISABLED"

    print_success "Minimal mode enabled"
    print_status "Token savings: ~45,000 tokens per conversation"
    echo ""
    show_status
}

# Disable all servers
disable_all() {
    print_warning "Disabling all MCP servers..."
    print_warning "You won't be able to use n8n, Notion, or other integrations!"
    echo ""
    read -p "Are you sure? (yes/no): " confirm

    if [[ "$confirm" != "yes" ]]; then
        print_status "Cancelled"
        exit 0
    fi

    # Disable: everything
    DISABLED='["n8n-mcp","playwriter","playwright","google-sheets","google-drive","notion","google-calendar","fathom","github-mcp","google-slides","google-docs"]'

    update_disabled_servers "$DISABLED"

    print_success "All servers disabled"
    echo ""
    show_status
}

# Main command handler
main() {
    check_jq
    check_config

    case "${1:-}" in
        status)
            show_status
            ;;
        list)
            show_status
            ;;
        enable-all)
            enable_all
            ;;
        core-mode)
            enable_core
            ;;
        pa-mode)
            enable_pa_mode
            ;;
        google-mode)
            enable_google_mode
            ;;
        minimal)
            enable_minimal
            ;;
        disable-all)
            disable_all
            ;;
        --help|-h|help)
            usage
            ;;
        "")
            print_error "No command specified"
            echo ""
            usage
            ;;
        *)
            print_error "Unknown command: $1"
            echo ""
            usage
            ;;
    esac
}

main "$@"
