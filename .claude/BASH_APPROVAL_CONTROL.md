# Bash Approval Control Guide

**Location:** `/Users/swayclarke/coding_stuff/.claude/settings.local.json`

---

## Current State: FULL BASH ACCESS ENABLED

**Line 4 in settings.local.json:**
```json
"Bash(*)"
```

This wildcard enables **ALL bash commands** without approval popups.

**Scope:** Applies to ALL chats started from `/Users/swayclarke/coding_stuff/` folder.

---

## How to DISABLE Full Bash Access

### Option 1: Comment Out the Wildcard (Recommended)

**Edit:** `/Users/swayclarke/coding_stuff/.claude/settings.local.json`

**Change line 4 from:**
```json
"Bash(*)",
```

**To:**
```json
// "Bash(*)",  // Disabled - requires approval for all bash
```

**Result:** All bash commands will require approval again, BUT the 170+ specific patterns below will still be auto-approved.

---

### Option 2: Remove Wildcard Entirely

**Edit:** `/Users/swayclarke/coding_stuff/.claude/settings.local.json`

**Delete line 4:**
```json
"Bash(*)",  // ← DELETE THIS ENTIRE LINE
```

**Result:** Same as Option 1 - returns to granular approval (170+ patterns remain).

---

### Option 3: Nuclear Option - Remove ALL Bash Approvals

**Edit:** `/Users/swayclarke/coding_stuff/.claude/settings.local.json`

**Replace entire allow array with:**
```json
{
  "permissions": {
    "allow": [
      "WebSearch",
      "mcp__notion__API-post-search"
    ],
    "deny": [],
    "ask": []
  }
}
```

**Result:** EVERY bash command requires manual approval. Use only if Claude is running too many commands.

---

## Quick Reference: When to Use Each Option

| Situation | Action | Effect |
|-----------|--------|--------|
| **Testing automation** | Keep `Bash(*)` enabled | No approvals needed |
| **Bash getting overwhelming** | Comment out `Bash(*)` (Option 1) | Granular control (170+ patterns) |
| **Need full control** | Delete `Bash(*)` (Option 2) | Granular control |
| **Claude too aggressive** | Remove all patterns (Option 3) | Approve every command |

---

## How to Check Current Status

**Command:**
```bash
grep -n "Bash(\*)" /Users/swayclarke/coding_stuff/.claude/settings.local.json
```

**If you see:**
- `4:      "Bash(*)",` → Full access ENABLED
- No output → Full access DISABLED

---

## Reversal Steps (Copy-Paste Ready)

### To DISABLE full bash access:

**Step 1:** Open settings file
```bash
code /Users/swayclarke/coding_stuff/.claude/settings.local.json
```

**Step 2:** Find line 4
```json
"Bash(*)",
```

**Step 3:** Comment it out
```json
// "Bash(*)",
```

**Step 4:** Save file (⌘+S)

**Step 5:** Restart Claude Code chat
- Changes apply to NEW chats
- Existing chats keep old settings

---

## Safety Notes

1. **Per-project setting** - Only affects chats in `coding_stuff/` folder
2. **Not retroactive** - Existing chats keep old settings
3. **Reversible** - Can toggle on/off anytime
4. **170+ patterns remain** - Disabling wildcard doesn't remove specific approvals

---

**Created:** 2025-12-31
**Last Updated:** 2025-12-31
