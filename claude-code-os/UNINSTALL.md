# How to Uninstall Claude Code OS

## The Good News

This is just a folder with markdown files. There's nothing installed on your system. No software, no background processes, no registry entries, no config files outside this folder.

## To Remove Everything

Open terminal and run:

```bash
rm -rf /Users/swayclarke/coding_stuff/claude-code-os
```

That's it. Done.

## What This Does NOT Affect

- Your Cursor installation
- Your other projects (oloxa_cc, lombok_blueprint_archive, etc.)
- Your GitHub account
- Your Claude Code CLI
- Any other folder on your computer

## Before You Delete

Consider saving these if you found them useful:
- `00-progress-advisor/MY-JOURNEY.md` (your personal progress log)
- Any templates you created in `09-templates/`
- Any custom agents you built in `05-hr-department/`

## If You Want to Start Fresh

Instead of deleting, you can also just reset:

```bash
# Keep the structure, reset the content
rm /Users/swayclarke/coding_stuff/claude-code-os/00-progress-advisor/MY-JOURNEY.md
# Then recreate MY-JOURNEY.md with a fresh start
```

## Questions?

If something seems broken or you're not sure if something is related to Claude Code OS, the answer is probably no. This is literally just markdown files in folders.

---

Remember: The goal was to help you, not lock you in. If it's not helping, delete it guilt-free.
