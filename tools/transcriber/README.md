# Audio Transcriber

A simple command-line tool to transcribe audio from YouTube videos or local files using OpenAI Whisper.

## Features

- Transcribe YouTube videos (auto-downloads audio)
- Transcribe local audio files (mp3, mp4, m4a, wav, flac, ogg, webm)
- Multiple model sizes (trade speed vs accuracy)
- Language support for non-English audio
- Automatic cleanup of temporary files
- Save transcripts to text files

## Installation

### 1. Install Python dependencies

```bash
cd /Users/swayclarke/coding_stuff/tools/transcriber
pip install -r requirements.txt
```

Note: First time running Whisper will download the model file (varies by size: base ~140MB, medium ~1.5GB)

### 2. Verify installation

```bash
python3 transcriber.py --help
```

## Usage

### Transcribe a local audio file

```bash
python3 transcriber.py recording.mp3
python3 transcriber.py /path/to/meeting.m4a
python3 transcriber.py podcast.wav --model medium
```

### Transcribe a YouTube video

```bash
python3 transcriber.py "https://youtube.com/watch?v=VIDEO_ID"
```

### Options

**Use a more accurate model:**
```bash
python3 transcriber.py audio.mp3 --model medium
```

**Specify output file name:**
```bash
python3 transcriber.py audio.mp3 --output my_transcript.txt
```

**Keep the downloaded audio (YouTube only):**
```bash
python3 transcriber.py "URL" --keep-audio
```

**Specify language (improves accuracy):**
```bash
python3 transcriber.py audio.mp3 --language en
```

**Combine options:**
```bash
python3 transcriber.py interview.m4a --model small --language es --output spanish_interview.txt
```

## Supported Audio Formats

- MP3
- MP4 / M4A
- WAV
- FLAC
- OGG
- WebM

## Model Sizes

Choose based on your needs:

| Model  | Size   | Speed    | Accuracy |
|--------|--------|----------|----------|
| tiny   | ~75MB  | Fastest  | Good     |
| base   | ~140MB | Fast     | Better   |
| small  | ~460MB | Medium   | Great    |
| medium | ~1.5GB | Slow     | Excellent|
| large  | ~2.9GB | Slowest  | Best     |

**Recommendation**: Start with `base` for a good balance. Use `medium` if accuracy is critical.

## Examples

Transcribe a voice memo:
```bash
python3 transcriber.py voice_memo.m4a
```

Transcribe a podcast with high accuracy:
```bash
python3 transcriber.py podcast.mp3 --model medium
```

Transcribe a Spanish interview:
```bash
python3 transcriber.py interview.mp3 --model medium --language es
```

Quick transcription of a short clip:
```bash
python3 transcriber.py clip.wav --model tiny
```

## Output

The script creates:
- A text file with the full transcript in the `transcripts/` folder
- Terminal preview of first 500 characters
- Timestamp-based filenames to avoid overwriting

## Troubleshooting

**"yt-dlp not found"** (only needed for YouTube)
```bash
pip install yt-dlp
```

**"OpenAI Whisper not found"**
```bash
pip install openai-whisper
```

**Slow transcription**
- Use a smaller model (`--model tiny` or `--model base`)
- Close other applications to free up resources

**Poor accuracy**
- Use a larger model (`--model medium` or `--model large`)
- Specify the language with `--language`

## Tips

- First run will download the Whisper model (one-time)
- Longer audio takes more time to transcribe
- GPU acceleration is automatic if you have CUDA/Metal support
- For YouTube, use `--keep-audio` if you want to re-transcribe with different settings

## License

Free to use. Built with yt-dlp and OpenAI Whisper.
