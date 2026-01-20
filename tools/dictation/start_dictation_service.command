#!/bin/bash
# Dictation Service Launcher
# This runs in user context so it has microphone access

cd "$(dirname "$0")"

# Kill any existing instances
pkill -f "dictation_service_v2.py"
sleep 1

# Remove stale PID file
rm -f dictation_service.pid

# Launch service using GUI-capable Python to enable menu bar icon
# Using Python.app instead of python3 gives rumps proper GUI context
/Library/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python dictation_service_v2.py >> dictation.log 2>> dictation_error.log &

echo "✅ Dictation service started"
echo "Menu bar icon should now appear in the top bar"
echo "You can close this window"
sleep 2
