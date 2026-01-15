# YouTube Transcriber

A simple command-line tool to transcribe YouTube videos using yt-dlp and OpenAI Whisper.

## Features

- Download audio from any YouTube video
- High-quality transcription using OpenAI Whisper
- Multiple model sizes (trade speed vs accuracy)
- Language support for non-English videos
- Automatic cleanup of temporary files
- Save transcripts to text files

## Installation

### 1. Install Python dependencies

```bash
cd /Users/swayclarke/coding_stuff/tools
pip install -r requirements.txt
```

Note: First time running Whisper will download the model file (varies by size: base ~140MB, medium ~1.5GB)

### 2. Verify installation

```bash
python3 youtube_transcriber.py --help
```

## Usage

### Basic usage

```bash
python3 youtube_transcriber.py "https://youtube.com/watch?v=VIDEO_ID"
```

This will:
- Download the audio
- Transcribe using the base model
- Save to `transcript_TIMESTAMP.txt`
- Show a preview in terminal
- Clean up the audio file

### Advanced options

**Use a more accurate model:**
```bash
python3 youtube_transcriber.py "URL" --model medium
```

**Specify output file name:**
```bash
python3 youtube_transcriber.py "URL" --output my_transcript.txt
```

**Keep the audio file:**
```bash
python3 youtube_transcriber.py "URL" --keep-audio
```

**Specify language (improves accuracy):**
```bash
python3 youtube_transcriber.py "URL" --language en
```

**Combine options:**
```bash
python3 youtube_transcriber.py "URL" --model small --language es --output spanish_video.txt
```

## Model Sizes

Choose based on your needs:

| Model  | Size  | Speed    | Accuracy |
|--------|-------|----------|----------|
| tiny   | ~75MB | Fastest  | Good     |
| base   | ~140MB| Fast     | Better   |
| small  | ~460MB| Medium   | Great    |
| medium | ~1.5GB| Slow     | Excellent|
| large  | ~2.9GB| Slowest  | Best     |

**Recommendation**: Start with `base` for a good balance. Use `medium` if accuracy is critical.

## Examples

Transcribe a tutorial:
```bash
python3 youtube_transcriber.py "https://youtube.com/watch?v=dQw4w9WgXcQ"
```

Transcribe a Spanish video with high accuracy:
```bash
python3 youtube_transcriber.py "https://youtube.com/watch?v=..." --model medium --language es
```

Quick transcription of a short video:
```bash
python3 youtube_transcriber.py "URL" --model tiny
```

## Output

The script creates:
- A text file with the full transcript
- Terminal preview of first 500 characters
- Timestamp-based filenames to avoid overwriting

## Troubleshooting

**"yt-dlp not found"**
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
- Longer videos take more time to transcribe
- GPU acceleration is automatic if you have CUDA/Metal support
- Keep audio files if you want to re-transcribe with different settings

## License

Free to use. Built with yt-dlp and OpenAI Whisper.
