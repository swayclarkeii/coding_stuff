#!/bin/bash
#
# Start localtunnel for OAuth monitoring
# Keeps the tunnel running persistently with auto-restart
#

SUBDOMAIN="oloxa-oauth-monitor"
PORT=5432
LOG_DIR="/Users/swayclarke/coding_stuff/logs"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Kill any existing localtunnel processes
pkill -f "lt --port $PORT"
sleep 1

echo "🚀 Starting localtunnel..."
echo "   Subdomain: $SUBDOMAIN"
echo "   Port: $PORT"
echo "   URL: https://$SUBDOMAIN.loca.lt/token-status"
echo ""
echo "   Logs: $LOG_DIR/localtunnel.log"
echo ""

# Start localtunnel in background with auto-restart
while true; do
    lt --port $PORT --subdomain $SUBDOMAIN >> "$LOG_DIR/localtunnel.log" 2>&1
    echo "$(date): Localtunnel stopped, restarting in 5 seconds..." >> "$LOG_DIR/localtunnel.log"
    sleep 5
done &

TUNNEL_PID=$!
echo "✅ Localtunnel started (PID: $TUNNEL_PID)"
echo "   To stop: pkill -f 'lt --port $PORT'"
echo ""
