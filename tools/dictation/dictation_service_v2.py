#!/usr/bin/env python3
"""
System-wide dictation service for macOS
- Press Control key twice to start recording
- Press Control once to stop and transcribe
- Auto-pastes cleaned text at cursor location
- Shows status via notifications and menu bar icon
"""

import os
import sys
import time
import tempfile
import threading
import queue
import subprocess
from pathlib import Path
from datetime import datetime

# Add Homebrew bin to PATH for ffmpeg (needed when run via LaunchAgent)
os.environ['PATH'] = '/opt/homebrew/bin:' + os.environ.get('PATH', '')

try:
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    from pynput import keyboard
    from pynput.keyboard import Key, Controller
    import openai
    from groq import Groq
    from dotenv import load_dotenv
    import rumps
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("\nPlease install required packages:")
    print("pip install sounddevice soundfile numpy pynput openai groq python-dotenv rumps")
    sys.exit(1)

# Load environment variables from .env file
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not OPENAI_API_KEY:
    print("❌ Error: OPENAI_API_KEY not found!")
    print("\nPlease add to .env file:")
    print("OPENAI_API_KEY=your-api-key-here")
    sys.exit(1)

if not GROQ_API_KEY:
    print("❌ Error: GROQ_API_KEY not found!")
    print("\nPlease add to .env file:")
    print("GROQ_API_KEY=your-api-key-here")
    print("\nGet a free key at: https://console.groq.com/keys")
    sys.exit(1)

SAMPLE_RATE = 16000
CHANNELS = 1

# PID file for preventing multiple instances
PID_FILE = Path(__file__).parent / "dictation_service.pid"

def ensure_single_instance():
    """Ensure only one instance of the service is running"""
    if PID_FILE.exists():
        try:
            old_pid = int(PID_FILE.read_text().strip())
            # Check if process is still running
            os.kill(old_pid, 0)
            print(f"❌ Service already running (PID: {old_pid})")
            print("Stop the existing instance first or delete the PID file if it's stale")
            sys.exit(1)
        except (OSError, ValueError):
            # Process doesn't exist, remove stale PID file
            PID_FILE.unlink()

    # Write our PID
    PID_FILE.write_text(str(os.getpid()))
    print(f"✅ PID file created: {PID_FILE}")

def cleanup_pid_file():
    """Remove PID file on exit"""
    try:
        if PID_FILE.exists():
            PID_FILE.unlink()
            print("✅ PID file removed")
    except:
        pass

CLEANING_PROMPT = '''# Role

You are an expert linguistic editor and communication specialist, skilled at transforming raw, messy transcripts into clean, clear, and logically structured text.
You combine precision, restraint, and linguistic discipline to preserve meaning while eliminating noise.
Your refined outputs empower users to convert spoken or rough-written material into publication- or prompt-ready clarity.

⸻

# Task

Clean and refine transcripts according to the following process:
	1.	Concise — Remove filler words such as "um," "ah," "you know," "like," "so yeah," "I mean," etc. Keep sentences short, direct, and to the point.
	2.	Logical — Delete repetitions or restated thoughts. Reorder only if needed for smooth, step-by-step logic.
	3.	Explicit — Complete broken or unfinished sentences so they read clearly and fully. State output formats explicitly.
	4.	Adaptive — Rephrase incomplete lines only for readability. Do not infer missing meaning or invent content. If something is unclear, insert [unclear phrase].
	5.	Reflective — Perform an internal verification check: confirm that meaning is preserved, clarity is achieved, and the output is ready to paste.

⸻

# Specifics
	•	Always output one section only:
	•	Clean Transcript — A filler-free, natural, and readable version of the input.
	•	Use the format marker below:

              ### Clean Transcript
              [Your cleaned transcript here]

⸻

# Context

Our organization produces a wide range of analytical and creative content that begins as spoken transcripts or loosely structured notes.
Your task is a critical quality-control step in this process: every refined transcript you produce becomes the foundation for prompt design, data interpretation, or client-facing documentation.
By ensuring clarity and structural precision, you help maintain the professional integrity of our work and the credibility of our communication.
Your attention to detail directly affects the success and clarity of all downstream outputs.

⸻

# Notes
	•	Always assume every input is a transcript unless explicitly stated: "This is not a transcript."
	•	Never provide commentary, analysis, or conversational remarks.
	•	Avoid inference: if meaning is unclear, use [unclear phrase].
	•	Prioritize meaning preservation over stylistic flair.
	•	Handle sensitive content with neutrality; do not alter tone or intent.
	•	Your disciplined accuracy ensures trust and reliability across every phase of the workflow.
	•	CRITICAL: Output as a single continuous paragraph with NO line breaks or paragraph separations. All text must flow as one block.

⸻

# Technical Terms Preservation

EXTREMELY IMPORTANT: Preserve technical terms, agent names, commands, file types, and proper nouns EXACTLY as spoken:
	•	"Claude" must NEVER be changed to "cloud" - Claude is a proper noun (AI assistant name)
	•	Agent names like "weekly-strategist-agent", "full-transcript-workflow-agent" must remain EXACTLY as spoken with hyphens
	•	Commands like "run the X-agent" must keep exact phrasing
	•	File extensions: "MD file", "Claude MD file", "PDF", "PNG" must remain unchanged
	•	Technical terms: preserve exact terminology even if it sounds unusual
	•	When in doubt between a common word and a technical term, prefer the technical interpretation
'''


class DictationMenuBarApp(rumps.App):
    """Menu bar application with microphone icon and status display"""

    def __init__(self, dictation_service):
        super(DictationMenuBarApp, self).__init__("🎙️", quit_button=None)
        self.dictation_service = dictation_service
        self.status_item = rumps.MenuItem("Status: Ready")
        self.menu = [
            self.status_item,
            rumps.separator,
            rumps.MenuItem("Controls:", callback=None),
            rumps.MenuItem("  Double-press Control → Start", callback=None),
            rumps.MenuItem("  Single-press Control → Stop", callback=None),
            rumps.separator,
            rumps.MenuItem("Quit", callback=self.quit_app)
        ]

    def update_status(self, status):
        """Update status in menu and title"""
        self.status_item.title = f"Status: {status}"
        # Also show brief status in title when active
        if status != "Ready":
            status_emoji = {
                "Recording...": "🔴",
                "Processing...": "⚙️",
                "Transcribing...": "🔄",
                "Cleaning...": "✨",
                "Pasting...": "📋"
            }
            self.title = status_emoji.get(status, "🎙️")
        else:
            self.title = "🎙️"

    def quit_app(self, _):
        """Quit the application"""
        rumps.quit_application()


class DictationService:
    def __init__(self, menu_app):
        self.is_recording = False
        self.audio_data = []
        self.whisper_model = None
        self.keyboard_controller = Controller()
        self.temp_dir = tempfile.mkdtemp()
        self.menu_app = menu_app

        # For detecting double Control press
        self.last_ctrl_press_time = 0
        self.ctrl_double_press_threshold = 0.3

        # Thread-safe queue for audio chunks
        self.audio_queue = queue.Queue()
        self.recording_stream = None

        # Initialize API clients
        print("Initializing API clients...")
        self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.groq_client = Groq(api_key=GROQ_API_KEY)
        print("✅ OpenAI (Whisper API) + Groq (cleaning) ready")

    def show_notification(self, title, message, sound=True):
        """Show macOS notification banner"""
        try:
            # Use osascript for native notifications
            sound_param = "sound name \"Glass\"" if sound else ""
            script = f'display notification "{message}" with title "{title}" {sound_param}'
            subprocess.run(['osascript', '-e', script], check=False, capture_output=True)
        except:
            pass

    def audio_callback(self, indata, frames, time_info, status):
        """Callback for audio recording"""
        if status:
            print(f"Audio status: {status}")
        self.audio_queue.put(indata.copy())

    def start_recording(self):
        """Start audio recording"""
        if self.is_recording:
            return

        self.is_recording = True
        self.audio_data = []
        print("🎙️  Recording started... (Press Control to stop)")

        # Update UI
        self.menu_app.update_status("Recording...")
        self.show_notification("🎙️ Recording", "Speak now...", sound=True)

        # Start recording stream - explicitly use default input device
        default_input = sd.query_devices(kind='input')
        print(f"🎤 Using input device: {default_input['name']}", flush=True)

        self.recording_stream = sd.InputStream(
            device=None,  # Use default input
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            callback=self.audio_callback,
            dtype=np.float32
        )
        self.recording_stream.start()

    def stop_recording(self):
        """Stop recording and process audio"""
        if not self.is_recording:
            return

        self.is_recording = False

        # Stop the stream
        if self.recording_stream:
            self.recording_stream.stop()
            self.recording_stream.close()
            self.recording_stream = None

        print("⏹️  Recording stopped. Processing...")

        # Update UI
        self.menu_app.update_status("Processing...")

        # Collect all audio data
        while not self.audio_queue.empty():
            self.audio_data.append(self.audio_queue.get())

        if not self.audio_data:
            print("❌ No audio recorded")
            self.menu_app.update_status("Ready")
            self.show_notification("❌ Error", "No audio recorded", sound=False)
            return

        # Process in background thread
        threading.Thread(target=self.process_audio, daemon=True).start()

    def transcribe_audio(self, audio_array):
        """Transcribe audio using OpenAI Whisper API"""
        audio_duration = len(audio_array) / SAMPLE_RATE

        # Save audio to temporary file
        temp_audio_path = os.path.join(self.temp_dir, f"recording_{int(time.time())}.wav")
        sf.write(temp_audio_path, audio_array, SAMPLE_RATE)

        try:
            print(f"🔄 Sending {audio_duration:.1f}s audio to OpenAI Whisper API...", flush=True)

            with open(temp_audio_path, "rb") as audio_file:
                response = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )

            return response.strip()
        finally:
            # Clean up temp file
            try:
                os.remove(temp_audio_path)
            except:
                pass

    def process_audio(self):
        """Transcribe and clean audio"""
        try:
            # Show transcribing status
            self.menu_app.update_status("Transcribing...")
            self.show_notification("🔄 Transcribing", "Processing your speech...", sound=False)

            # Combine audio chunks
            audio_array = np.concatenate(self.audio_data, axis=0)

            # Diagnostic info
            audio_duration = len(audio_array) / SAMPLE_RATE
            audio_max = np.max(np.abs(audio_array)) if len(audio_array) > 0 else 0
            print(f"🎤 Audio captured: {audio_duration:.2f}s, max amplitude: {audio_max:.4f}, chunks: {len(self.audio_data)}", flush=True)

            print("🔄 Transcribing with OpenAI Whisper API...", flush=True)
            raw_text = self.transcribe_audio(audio_array)

            print(f"📝 Raw transcript: {raw_text[:100]}...", flush=True)
            print(f"📝 Raw transcript (full length: {len(raw_text)} chars)", flush=True)

            # Clean the transcript
            self.menu_app.update_status("Cleaning...")
            self.show_notification("✨ Cleaning", "Refining your text...", sound=False)

            cleaned_text = self.clean_transcript(raw_text)
            print(f"✨ Cleaned: {cleaned_text[:100]}...", flush=True)

            # If cleaned text is just "[unclear phrase]" or empty, use raw text instead
            if cleaned_text.strip() in ["[unclear phrase]", "[unclear phrase].", ""] or len(cleaned_text.strip()) < 3:
                print("⚠️  Cleaned text unclear, using raw transcript instead", flush=True)
                cleaned_text = raw_text

            # Paste the cleaned text
            self.menu_app.update_status("Pasting...")
            self.show_notification("📋 Pasting", "Inserting text...", sound=False)

            self.paste_text(cleaned_text)

            # Update status
            self.menu_app.update_status("Ready")
            self.show_notification("✅ Done!", "Text pasted successfully", sound=True)

        except Exception as e:
            print(f"❌ Error processing audio: {e}")
            import traceback
            traceback.print_exc()
            self.menu_app.update_status("Ready")
            self.show_notification("❌ Error", f"Processing failed: {str(e)[:50]}", sound=False)

    def clean_transcript(self, raw_text):
        """Clean transcript using Groq (ultra-fast inference)"""
        try:
            print("✨ Cleaning transcript with Groq...", flush=True)

            response = self.groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": CLEANING_PROMPT},
                    {"role": "user", "content": raw_text}
                ],
                temperature=0.3,
                max_tokens=2000
            )

            cleaned = response.choices[0].message.content.strip()

            # Extract content after "### Clean Transcript"
            if "### Clean Transcript" in cleaned:
                content = cleaned.split("### Clean Transcript")[1].strip()

                # Remove any subsequent ### sections
                if "###" in content:
                    content = content.split("###")[0].strip()

                # Remove "[No input provided.]" artifact
                content = content.replace("[No input provided.]", "").strip()

                # Ensure single paragraph - remove all line breaks
                content = " ".join(content.split())
                return content

            # Fallback: remove artifact from raw cleaned text
            cleaned = cleaned.replace("[No input provided.]", "").strip()
            # Ensure single paragraph - remove all line breaks
            cleaned = " ".join(cleaned.split())
            return cleaned

        except Exception as e:
            print(f"❌ Error cleaning transcript: {e}")
            return raw_text

    def paste_text(self, text):
        """Copy text to clipboard and auto-paste"""
        try:
            # Ensure single paragraph (extra safety)
            text = " ".join(text.split())

            # Copy to clipboard
            subprocess.run(['pbcopy'], input=text.encode('utf-8'), check=True)

            # Small delay to ensure clipboard is ready
            time.sleep(0.2)

            # Auto-paste using Cmd+V
            self.keyboard_controller.press(Key.cmd)
            self.keyboard_controller.press('v')
            self.keyboard_controller.release('v')
            self.keyboard_controller.release(Key.cmd)

            print("✅ Text pasted successfully")

        except Exception as e:
            print(f"❌ Paste failed: {e}")
            self.show_notification("❌ Error", "Failed to paste text", sound=False)

    def on_press(self, key):
        """Handle key press events"""
        try:
            if key == Key.ctrl_l or key == Key.ctrl_r:
                current_time = time.time()

                if self.is_recording:
                    self.stop_recording()
                    self.last_ctrl_press_time = 0
                elif current_time - self.last_ctrl_press_time < self.ctrl_double_press_threshold:
                    self.start_recording()
                    self.last_ctrl_press_time = 0
                else:
                    self.last_ctrl_press_time = current_time

        except Exception as e:
            print(f"Error in key handler: {e}")
            import traceback
            traceback.print_exc()

    def on_release(self, key):
        """Handle key release events"""
        pass

    def run(self):
        """Start the dictation service"""
        print("=" * 60)
        print("🎙️  Dictation Service Started")
        print("=" * 60)
        print("Controls:")
        print("  • Press Control twice quickly → Start recording")
        print("  • Press Control once → Stop recording and transcribe")
        print("=" * 60)
        print("Listening for hotkey...\n")

        # Start keyboard listener in background thread
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()


def main():
    # Ensure only one instance runs
    ensure_single_instance()

    # Register cleanup on exit
    import atexit
    atexit.register(cleanup_pid_file)

    try:
        # Create menu bar app first
        print("🎨 Initializing menu bar app...", flush=True)
        menu_app = DictationMenuBarApp(None)
        print("✅ Menu bar app created", flush=True)

        # Create dictation service
        service = DictationService(menu_app)
        menu_app.dictation_service = service

        # Start the dictation service
        service.run()

        # Run menu bar app in main thread (blocks)
        print("🚀 Starting menu bar app (this should make icon appear)...", flush=True)
        menu_app.run()

    except KeyboardInterrupt:
        print("\n\n👋 Dictation service stopped")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
