# Video Tools - Getting Started Guide

Both Remotion and ButterCut are now installed and ready to use!

## Location

```
/Users/computer/coding_stuff/video-tools/
├── my-remotion-project/     # Remotion installation
└── buttercut/               # ButterCut installation
```

---

## 1. Remotion - Programmatic Video Creation

### What It Does
Creates animated videos from code (text overlays, chapter titles, animated subtitles, motion graphics, data visualizations).

### Quick Start

**Preview your first video:**
```bash
cd /Users/computer/coding_stuff/video-tools/my-remotion-project
npm start
```

This opens a browser preview showing a "Hello World" animation with fade-in effect.

**What You Can Create with Remotion:**
- Animated chapter titles and text overlays
- Animated subtitles (imports SRT files)
- Data visualizations and charts
- Motion graphics and transitions
- Lower thirds for videos

**How It Works:**
1. You describe what you want to Claude Code (in this directory)
2. Claude generates React code for your animation
3. Preview it with `npm start` (opens in browser)
4. Render final video with `npm run build`
5. Import the rendered MP4/MOV into DaVinci Resolve as overlay

**Example:**
```
You: "Create an animated chapter title that says 'Chapter 1: Introduction'
      with a fade-in effect and bold white text on dark background"

Claude: [Generates code using Remotion Skills]

You: npm start  # Preview in browser
     npm run build  # Render to video file
```

**Remotion Skills Installed:**
- Located at: `.agents/skills/remotion-best-practices`
- Available in Claude Code, Codex, and Cursor

**Templates Available:**
- Blank (currently installed)
- Hello World
- Audiogram
- Text-to-Speech
- Subtitles
- Music Visualization
- Code animations
- And many more at https://remotion.dev/templates/

---

## 2. ButterCut - AI Video Editor Assistant

### What It Does
Analyzes your iPhone footage (transcribes audio, analyzes video frames) and creates rough cut timelines for DaVinci Resolve based on your editorial direction.

### Quick Start

**From the buttercut directory:**
```bash
cd /Users/computer/coding_stuff/video-tools/buttercut
claude
```

**Then tell Claude:**
```
> I want to create a new library
```

Claude will ask you:
1. Library name (e.g., "my-first-video")
2. Where are your video files? (path to your iPhone footage)
3. What language? (e.g., "en" for English)

Claude will then:
- Transcribe all audio (WhisperX)
- Analyze video frames
- Generate visual transcripts
- Ask what kind of rough cut you want

**Creating a Rough Cut:**
```
You: "Let's create a roughcut"

Claude: "What should this roughcut focus on?"
        - Full story
        - Highlights
        - Short teaser

You: "3-minute highlights, conversational pacing"

Claude: [Analyzes transcripts and creates timeline]
        ✓ Selected 15 clips (3:12 total)
        ✓ Exported to XML for DaVinci Resolve

Result: libraries/[library-name]/roughcuts/[name]_[datetime].xml
```

**Import to DaVinci Resolve:**
1. Open DaVinci Resolve
2. File → Import → Timeline
3. Select the exported XML file
4. Timeline appears ready to edit

### What Makes ButterCut Different

**NOT an editor like CapCut** - it's a rough cut generator:
- Analyzes your footage content (transcripts + visuals)
- Selects which clips to use based on your criteria
- Arranges them into a timeline
- Exports XML for your real editor

**NOT a filler word remover** - it's a clip selector:
- CapCut removes "um" and "uh" from audio
- ButterCut selects entire clips based on content

### Example Use Case

**Your Workflow:**
1. Shoot 30 minutes of iPhone footage
2. AirDrop to laptop
3. Create ButterCut library
4. Tell Claude: "Create a 5-minute rough cut focusing on the moments where I discuss AI tools, with fast pacing"
5. Claude analyzes transcripts and creates timeline
6. Import XML into DaVinci Resolve
7. Fine-tune the edit, add effects, color grade
8. Export final video

---

## Dependencies Installed

✅ **Node.js v20.20.0** - For Remotion
✅ **Ruby 4.0.1** - For ButterCut gem
✅ **Python 3.12.4** - For WhisperX
✅ **FFmpeg** - For video processing
✅ **WhisperX** - For audio transcription
✅ **Remotion Skills** - AI integration for video creation
✅ **ButterCut Skills** - AI integration for rough cuts

---

## Next Steps

### Try Remotion (5 minutes)
1. `cd /Users/computer/coding_stuff/video-tools/my-remotion-project`
2. `npm start` - Opens browser preview
3. Edit `src/HelloWorld.tsx` to change the text
4. See changes update live in browser
5. When happy: `npm run build` to render video

### Try ButterCut (requires video footage)
1. `cd /Users/computer/coding_stuff/video-tools/buttercut`
2. `claude` - Opens Claude Code
3. `> I want to create a new library` - Start setup
4. Follow prompts to analyze your footage
5. `> Let's create a roughcut` - Generate timeline
6. Import XML into DaVinci Resolve

---

## Important Notes

**Remotion:**
- Creates NEW video content from code (animations, graphics)
- Does NOT edit existing iPhone footage
- Use it to CREATE overlays that you'll import into DaVinci

**ButterCut:**
- Analyzes EXISTING iPhone footage
- Creates rough cut timelines based on content
- Exports to DaVinci Resolve for final editing
- Completely FREE and open source

**Both Tools:**
- Free to use
- Work with Claude Code
- Designed to reduce post-production time
- Complement DaVinci Resolve (don't replace it)

---

## Quick Reference Commands

**Remotion:**
```bash
cd /Users/computer/coding_stuff/video-tools/my-remotion-project
npm start          # Preview
npm run build      # Render to video
```

**ButterCut:**
```bash
cd /Users/computer/coding_stuff/video-tools/buttercut
claude             # Start Claude Code
```

**Check Installations:**
```bash
node --version          # Should show v20.20.0
ruby --version          # Should show 4.0.1
python3.12 --version    # Should show 3.12.4
ffmpeg -version         # Should show installed
whisperx --help         # Should show help text
```

---

## Support & Documentation

**Remotion:**
- Official Docs: https://remotion.dev/docs
- Templates: https://remotion.dev/templates
- Skills: Installed at `.agents/skills/remotion-best-practices`

**ButterCut:**
- GitHub: https://github.com/barefootford/buttercut
- Website: https://buttercut.io
- Demo Video: https://www.youtube.com/watch?v=FBkfr1yWf_s
- Skills: Located at `.agents/skills/` in buttercut directory

---

Ready to start creating! 🎬
