Backup ONLY the claude-code-os folder from the current machine to GitHub.

Execute the following git commands in sequence:

```bash
cd ~/coding_stuff && git add claude-code-os/ && git commit -m "Backup claude-code-os $(date '+%Y-%m-%d %H:%M')" && git push
```

If there are no changes to commit, let me know "Nothing to backup in claude-code-os."

If the push succeeds, confirm with a summary of what was committed.

If there are any errors, explain the issue and suggest how to resolve it.
