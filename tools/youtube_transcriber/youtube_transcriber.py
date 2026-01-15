#!/usr/bin/env python3
"""
YouTube Video Transcriber
Uses yt-dlp to download audio and OpenAI Whisper to transcribe.
"""

import argparse
import os
import sys
import subprocess
import re
import json
from pathlib import Path
from datetime import datetime


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import whisper
    except ImportError:
        print("❌ OpenAI Whisper not found. Install with: pip install openai-whisper")
        return False

    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ yt-dlp not found. Install with: pip install yt-dlp")
        return False

    return True


def get_video_title(youtube_url):
    """Get the video title from YouTube."""
    try:
        cmd = ['yt-dlp', '--get-title', youtube_url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def sanitize_filename(title):
    """Convert title to a safe filename."""
    # Replace spaces with underscores
    sanitized = title.replace(' ', '_')
    # Remove or replace special characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', sanitized)
    # Remove multiple underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    # Limit length to avoid filesystem issues
    if len(sanitized) > 80:
        sanitized = sanitized[:80]
    # Remove trailing underscores
    sanitized = sanitized.rstrip('_')
    return sanitized


def download_audio(youtube_url, output_path):
    """Download audio from YouTube video."""
    print(f"📥 Downloading audio from YouTube...")

    try:
        cmd = [
            'yt-dlp',
            '-x',  # Extract audio
            '--audio-format', 'mp3',
            '--audio-quality', '0',  # Best quality
            '-o', output_path,
            youtube_url
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"❌ Error downloading video: {result.stderr}")
            return False

        print("✅ Audio downloaded successfully")
        return True

    except Exception as e:
        print(f"❌ Error during download: {e}")
        return False


def transcribe_audio(audio_path, model_size='base', language=None):
    """Transcribe audio file using Whisper."""
    print(f"🎙️  Transcribing audio with Whisper ({model_size} model)...")

    try:
        import whisper

        # Load model
        print(f"📦 Loading Whisper model...")
        model = whisper.load_model(model_size)

        # Transcribe
        print(f"⏳ Transcribing (this may take a few minutes)...")
        options = {}
        if language:
            options['language'] = language

        result = model.transcribe(str(audio_path), **options)

        print("✅ Transcription complete")
        return result['text']

    except Exception as e:
        print(f"❌ Error during transcription: {e}")
        return None


def save_transcript(transcript, output_file):
    """Save transcript to file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f"💾 Transcript saved to: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error saving transcript: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Transcribe YouTube videos using Whisper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python youtube_transcriber.py "https://youtube.com/watch?v=..."
  python youtube_transcriber.py "URL" --model medium --language en
  python youtube_transcriber.py "URL" --keep-audio --output my_transcript.txt

Model sizes (smaller = faster, larger = more accurate):
  tiny, base, small, medium, large
        """
    )

    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('--model', default='base',
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper model size (default: base)')
    parser.add_argument('--language', help='Language code (e.g., en, es, fr)')
    parser.add_argument('--output', '-o', help='Output transcript file name')
    parser.add_argument('--keep-audio', action='store_true',
                       help='Keep downloaded audio file after transcription')

    args = parser.parse_args()

    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ All dependencies found\n")

    # Get video title for filename
    print("📝 Fetching video title...")
    video_title = get_video_title(args.url)
    if video_title:
        safe_title = sanitize_filename(video_title)
        print(f"📹 Video: {video_title}\n")
    else:
        safe_title = "video"
        print("⚠️  Could not fetch video title, using generic name\n")

    # Setup paths
    script_dir = Path(__file__).parent
    transcripts_dir = script_dir / 'transcripts'
    transcripts_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    audio_file = Path(f'youtube_audio_{timestamp}.mp3')

    if args.output:
        transcript_file = Path(args.output)
    else:
        transcript_file = transcripts_dir / f'{safe_title}_transcript_{timestamp}.txt'

    try:
        # Download audio
        if not download_audio(args.url, str(audio_file)):
            sys.exit(1)

        # Transcribe
        transcript = transcribe_audio(audio_file, args.model, args.language)
        if not transcript:
            sys.exit(1)

        # Save transcript
        if not save_transcript(transcript, transcript_file):
            sys.exit(1)

        # Display preview
        print("\n" + "="*50)
        print("📄 Transcript Preview:")
        print("="*50)
        preview = transcript[:500] + "..." if len(transcript) > 500 else transcript
        print(preview)
        print("="*50 + "\n")

        # Cleanup
        if not args.keep_audio:
            audio_file.unlink()
            print(f"🧹 Cleaned up audio file")
        else:
            print(f"💾 Audio file saved: {audio_file}")

        print(f"\n✨ Done! Full transcript saved to: {transcript_file}")

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        if audio_file.exists():
            audio_file.unlink()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if audio_file.exists():
            audio_file.unlink()
        sys.exit(1)


if __name__ == '__main__':
    main()
