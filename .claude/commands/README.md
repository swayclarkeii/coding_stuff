# Backup & Sync Commands Reference

Quick reference for syncing your `coding_stuff` folder between laptop and desktop via GitHub.

---

## Commands Overview

| Command | Description |
|---------|-------------|
| `/backup-laptop` | Push all changes from laptop to GitHub |
| `/backup-desktop` | Push all changes from desktop to GitHub |
| `/backup-claude-code-os` | Push only the claude-code-os folder |
| `/restore-laptop` | Pull latest from GitHub to laptop |
| `/restore-desktop` | Pull latest from GitHub to desktop |
| `/sync-force-laptop` | Pull when laptop has uncommitted changes |
| `/sync-force-desktop` | Pull when desktop has uncommitted changes |

---

## Common Scenarios

### Scenario 1: Clean Switch Between Machines

**You're done on laptop, switching to desktop:**
```
Laptop:  /backup-laptop      (push your work)
Desktop: /restore-desktop    (pull the work)
```

**You're done on desktop, switching to laptop:**
```
Desktop: /backup-desktop     (push your work)
Laptop:  /restore-laptop     (pull the work)
```

---

### Scenario 2: Both Machines Have Uncommitted Changes

This happens when you forgot to backup before switching.

**Solution - pick one machine to go first:**

```
1. Desktop: /backup-desktop        → Push desktop changes
2. Laptop:  /sync-force-laptop     → Pull + keep laptop changes
3. Laptop:  /backup-laptop         → Push combined changes
4. Desktop: /restore-desktop       → Pull combined changes
```

Or starting from laptop:

```
1. Laptop:  /backup-laptop         → Push laptop changes
2. Desktop: /sync-force-desktop    → Pull + keep desktop changes
3. Desktop: /backup-desktop        → Push combined changes
4. Laptop:  /restore-laptop        → Pull combined changes
```

---

### Scenario 3: Only Backup Specific Folder

When you only want to backup claude-code-os without affecting other uncommitted work:

```
/backup-claude-code-os
```

---

## Handling Merge Conflicts

If `/sync-force-*` reports conflicts (both machines edited the same file):

1. Open the conflicting files in Cursor
2. Look for conflict markers:
   ```
   <<<<<<< HEAD
   (your local changes)
   =======
   (incoming changes from GitHub)
   >>>>>>> stash
   ```
3. Edit the file to keep what you want (remove the markers)
4. Save the file
5. Run: `git add <filename>`
6. Then backup: `/backup-laptop` or `/backup-desktop`

---

## Golden Rule

**Always backup before switching machines.**

```
Leaving laptop?  → /backup-laptop
Leaving desktop? → /backup-desktop
```

This prevents the "both have changes" situation entirely.

---

## What Gets Synced

Everything in `~/coding_stuff` EXCEPT:
- `node_modules/`
- `.env` files and credentials
- `Fathom Transcripts` (synced via Google Drive instead)
- See `.gitignore` for full exclusion list

---

## Troubleshooting

**"Nothing to backup"**
- No changes detected. You're already synced.

**"Push rejected"**
- GitHub has newer commits. Run `/sync-force-*` first, then backup again.

**"Stash pop failed"**
- Your stashed changes conflict with pulled changes
- Run `git stash show` to see what's stashed
- Resolve manually, then `git stash drop`

**Need to undo a sync-force?**
- Your original changes are still in the stash
- Run `git stash list` to see them
- Run `git stash pop` to reapply (after fixing issues)
