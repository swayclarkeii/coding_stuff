Sync the laptop when it has uncommitted changes AND GitHub has newer commits.

This command:
1. Stashes (temporarily saves) your uncommitted laptop changes
2. Pulls the latest from GitHub
3. Reapplies your laptop changes on top

Execute the following git commands:

```bash
cd ~/coding_stuff && git stash push -m "Auto-stash before sync $(date '+%Y-%m-%d %H:%M')" && git pull && git stash pop
```

**After running, explain what happened:**
- If successful: "Synced successfully. Your laptop changes have been reapplied on top of the pulled changes."
- If merge conflicts occur: List the conflicting files and explain that the user needs to manually resolve them, then run `git add <file>` for each resolved file.
- If stash pop fails: Explain that the stashed changes conflicted and are still in the stash. User can run `git stash show` to see them and `git stash drop` after resolving.

**Important:** Remind the user to run `/backup-laptop` after resolving any conflicts to push the combined changes.
