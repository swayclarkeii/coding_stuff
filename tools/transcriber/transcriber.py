#!/usr/bin/env python3
"""
Audio Transcriber
Transcribes audio from YouTube URLs or local files using OpenAI Whisper.
"""

import argparse
import os
import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime


def check_dependencies(need_ytdlp=False):
    """Check if required dependencies are installed."""
    try:
        import whisper
    except ImportError:
        print("❌ OpenAI Whisper not found. Install with: pip install openai-whisper")
        return False

    if need_ytdlp:
        try:
            subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ yt-dlp not found. Install with: pip install yt-dlp")
            return False

    return True


def is_local_file(path):
    """Check if the input is a local file."""
    return Path(path).exists()


def is_youtube_url(url):
    """Check if the input looks like a YouTube URL."""
    youtube_patterns = [
        'youtube.com',
        'youtu.be',
        'youtube-nocookie.com'
    ]
    return any(pattern in url.lower() for pattern in youtube_patterns)


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
    sanitized = title.replace(' ', '_')
    sanitized = re.sub(r'[<>:"/\\|?*]', '', sanitized)
    sanitized = re.sub(r'_+', '_', sanitized)
    if len(sanitized) > 80:
        sanitized = sanitized[:80]
    sanitized = sanitized.rstrip('_')
    return sanitized


def download_audio(youtube_url, output_path):
    """Download audio from YouTube video."""
    print(f"📥 Downloading audio from YouTube...")

    try:
        cmd = [
            'yt-dlp',
            '-x',
            '--audio-format', 'mp3',
            '--audio-quality', '0',
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

        print(f"📦 Loading Whisper model...")
        model = whisper.load_model(model_size)

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
        description='Transcribe audio from YouTube or local files using Whisper',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # YouTube video
  python transcriber.py "https://youtube.com/watch?v=..."

  # Local audio file
  python transcriber.py recording.mp3
  python transcriber.py /path/to/meeting.m4a --model medium

  # With options
  python transcriber.py "URL" --model medium --language en
  python transcriber.py audio.wav --output my_transcript.txt

Supported formats: mp3, mp4, m4a, wav, flac, ogg, webm

Model sizes (smaller = faster, larger = more accurate):
  tiny, base, small, medium, large
        """
    )

    parser.add_argument('input', help='YouTube URL or path to audio file')
    parser.add_argument('--model', default='base',
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper model size (default: base)')
    parser.add_argument('--language', help='Language code (e.g., en, es, fr)')
    parser.add_argument('--output', '-o', help='Output transcript file name')
    parser.add_argument('--keep-audio', action='store_true',
                       help='Keep downloaded audio file (YouTube only)')

    args = parser.parse_args()

    # Determine input type
    is_local = is_local_file(args.input)
    is_youtube = is_youtube_url(args.input)

    if not is_local and not is_youtube:
        print(f"❌ Input not recognized as a local file or YouTube URL: {args.input}")
        sys.exit(1)

    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies(need_ytdlp=is_youtube):
        sys.exit(1)
    print("✅ All dependencies found\n")

    # Setup paths
    script_dir = Path(__file__).parent
    transcripts_dir = script_dir / 'transcripts'
    transcripts_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    if is_local:
        # Local file mode
        audio_file = Path(args.input)
        print(f"📁 Using local file: {audio_file.name}\n")

        if not audio_file.exists():
            print(f"❌ File not found: {args.input}")
            sys.exit(1)

        safe_title = sanitize_filename(audio_file.stem)
        temp_audio = None  # No cleanup needed

    else:
        # YouTube mode
        print("📝 Fetching video title...")
        video_title = get_video_title(args.input)
        if video_title:
            safe_title = sanitize_filename(video_title)
            print(f"📹 Video: {video_title}\n")
        else:
            safe_title = "video"
            print("⚠️  Could not fetch video title, using generic name\n")

        temp_audio = Path(f'youtube_audio_{timestamp}.mp3')

        if not download_audio(args.input, str(temp_audio)):
            sys.exit(1)

        audio_file = temp_audio

    # Set output path
    if args.output:
        transcript_file = Path(args.output)
    else:
        transcript_file = transcripts_dir / f'{safe_title}_transcript_{timestamp}.txt'

    try:
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

        # Cleanup (YouTube downloads only)
        if temp_audio and temp_audio.exists():
            if not args.keep_audio:
                temp_audio.unlink()
                print(f"🧹 Cleaned up audio file")
            else:
                print(f"💾 Audio file saved: {temp_audio}")

        print(f"\n✨ Done! Full transcript saved to: {transcript_file}")

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        if temp_audio and temp_audio.exists():
            temp_audio.unlink()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if temp_audio and temp_audio.exists():
            temp_audio.unlink()
        sys.exit(1)


if __name__ == '__main__':
    main()
