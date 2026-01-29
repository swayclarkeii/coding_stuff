# Voice Dictation Service

System-wide voice dictation for macOS with automatic transcription and pasting.

## Quick Start

1. **Start the service:**
   ```bash
   Double-click: start_dictation_service.command
   ```

2. **Use it:**
   - **Double-press Control** → Start recording (🔴 appears in menu bar)
   - **Speak clearly**
   - **Single-press Control** → Stop and auto-paste

## Features

✅ **Auto-paste** - Transcribed text pastes automatically at cursor
✅ **Menu bar icon** - Shows status (🎙️ → 🔴 → ⚙️ → ✨ → 📋)
✅ **Smart Cleaning toggle** - Turn on/off GPT cleaning via menu bar (ON by default)
✅ **GPT cleaning** - Removes filler words with minimal changes to preserve meaning
✅ **Single paragraph** - No line breaks (prevents accidental submit)
✅ **Background service** - Runs without terminal
✅ **Long recordings** - Auto-chunks recordings >3 minutes into 60s segments for faster processing

## Files

```
dictation_service_v2.py          # Main service (don't run directly)
start_dictation_service.command  # Launcher (double-click this)
.env                            # API key (OPENAI_API_KEY=xxx)
requirements.txt                # Python dependencies
venv/                          # Python environment
dictation.log                  # Output logs
dictation_error.log           # Error logs
```

## Setup (First Time)

1. **Install dependencies:**
   ```bash
   cd /Users/swayclarke/coding_stuff/tools/dictation
   python3 -m venv venv
   ./venv/bin/pip install -r requirements.txt
   ```

2. **Add OpenAI API key:**
   ```bash
   echo "OPENAI_API_KEY=your-key-here" > .env
   ```

3. **Grant microphone permission:**
   - Double-click `start_dictation_service.command`
   - Click "OK" when prompted for microphone access

## Auto-Start on Login

1. Open **System Settings** → **General** → **Login Items**
2. Click **+** button
3. Add `start_dictation_service.command`

## Troubleshooting

### Menu bar icon not appearing
- The service uses GUI-capable Python to display the icon
- Check Activity Monitor - should see "Python" process running
- Try: `pkill -f dictation_service` then restart
- Icon appears in top-right of screen near clock/Wi-Fi

### No audio captured (max amplitude: 0.0000)
- Check System Settings → Privacy & Security → Microphone
- Ensure Python has microphone access
- Restart the service

### Service not responding
```bash
pkill -f dictation_service
# Then restart by double-clicking start_dictation_service.command
```

### View logs
```bash
tail -f dictation.log
```

### Technical terms being changed incorrectly
The service now preserves:
- "Claude" (not "cloud")
- Agent names like "weekly-strategist-agent"
- File types like "MD file", "Claude MD file"
- Technical commands and terminology

## How It Works

1. **Listen** - Monitors Control key double-press
2. **Record** - Captures audio via MacBook microphone
3. **Transcribe** - Uses Whisper (local) to convert speech to text
4. **Clean** - GPT-4o-mini removes filler words and fixes grammar
5. **Paste** - Automatically pastes at cursor location

## Smart Cleaning Toggle

Click the **menu bar icon** (🎙️) to access settings:
- **Smart Cleaning: ON ✓** - GPT cleans transcript (removes filler words, minimal changes)
- **Smart Cleaning: OFF** - Raw Whisper output (no processing)

**When to turn OFF:**
- You want exact transcription with all "ums" and "ahs"
- Cleaning is changing your meaning
- You prefer raw output for later editing

**When to keep ON:**
- Most general use (default setting)
- You want polished text without filler words
- Professional communications

## Technical Details

- **Transcription**: OpenAI Whisper API (via OpenAI API)
  - Recordings ≤180 seconds: transcribed as single file
  - Recordings >180 seconds: auto-chunked into 60-second segments
  - Chunking provides faster processing for long recordings
- **Cleaning**: GPT-4o-mini API (minimal changes, preserves meaning)
  - Only removes obvious filler words (um, uh, ah, like, you know)
  - Does NOT restructure sentences or change questions to statements
  - Toggle on/off via menu bar
- **Audio**: 16kHz, mono, float32
- **Hotkey**: Control key double-press (0.3s threshold)
- **Output**: Single continuous paragraph (no line breaks)
