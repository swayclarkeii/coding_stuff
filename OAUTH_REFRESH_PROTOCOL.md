# OAuth Refresh Protocol

**Last Updated:** 2025-12-30T16:38:28+01:00
**Status:** ACTIVE RULE

## Critical Rule: Autonomous OAuth Refresh

**ALWAYS use Playwright to handle OAuth token refreshes autonomously.**

### What This Means

When working with OAuth-authenticated services (Google, GitHub, Notion, etc.) and encountering expired tokens or authentication prompts:

1. **DO NOT** ask Sway to:
   - Complete pop-ups manually
   - Copy/paste URLs
   - Authenticate through browser manually
   - Handle any part of the OAuth flow

2. **ALWAYS:**
   - Use Playwright MCP tools (`mcp__playwright__*`) to automate the OAuth flow
   - Navigate to the OAuth consent screen
   - Fill in credentials programmatically
   - Complete the authorization flow
   - Capture the resulting tokens
   - Continue with the task autonomously

### Affected Services

This rule applies to ALL services requiring OAuth authentication:
- **Google Services:** Gmail, Google Drive, Google Sheets, Google Docs, Google Calendar, Google Slides
- **GitHub:** Repository access, API operations
- **Notion:** Database operations, page creation
- **Fathom:** Meeting transcripts
- **n8n:** OAuth-based node credentials
- **Any other OAuth 2.0 service**

### Implementation Pattern

When detecting expired OAuth tokens:

```typescript
// WRONG ❌
"Your Google token has expired. Please visit this URL and authorize the app..."

// CORRECT ✅
1. Use mcp__playwright__browser_navigate to OAuth consent URL
2. Use mcp__playwright__browser_snapshot to analyze the page
3. Use mcp__playwright__browser_type and browser_click to complete auth
4. Capture redirect/callback with tokens
5. Update credentials and continue
```

### Example: Google OAuth Refresh Flow

```typescript
// 1. Navigate to OAuth URL
mcp__playwright__browser_navigate({
  url: "https://accounts.google.com/o/oauth2/auth?..."
})

// 2. Take snapshot to identify elements
mcp__playwright__browser_snapshot()

// 3. Fill in credentials (if needed)
mcp__playwright__browser_type({
  element: "Email input",
  ref: "input[type='email']",
  text: "sway@oloxa.ai"
})

// 4. Click authorize
mcp__playwright__browser_click({
  element: "Authorize button",
  ref: "button[contains(text(), 'Authorize')]"
})

// 5. Capture tokens from redirect
// Continue with task
```

### When Manual Intervention IS Required

Manual intervention should only be requested when:
- **Security:** 2FA codes sent to phone (cannot be automated)
- **Account Lockout:** Account requires manual unlock by user
- **Terms of Service:** New ToS must be reviewed and accepted by user
- **Payment:** Payment authorization required

### Documentation Location

This rule is documented in:
- **Primary:** `/Users/swayclarke/coding_stuff/OAUTH_REFRESH_PROTOCOL.md` (this file)
- **Referenced in:** `/Users/swayclarke/coding_stuff/CLAUDE.md`

### Enforcement

This rule overrides default behavior. When in doubt:
1. Check if Playwright can automate the flow → Use Playwright
2. Only escalate to user if genuinely requires human intervention (2FA, payment, etc.)

### Rationale

Autonomous OAuth handling provides:
- **Efficiency:** No waiting for user to complete manual steps
- **Reliability:** Consistent, repeatable authentication flow
- **User Experience:** Sway can focus on high-level tasks, not auth flows
- **Documentation:** Auth flows are captured in conversation history

### Notes

- Playwright browser sessions persist across tool calls in the same conversation
- Store credentials securely in appropriate MCP server configs
- Always test OAuth flows in development before production use
- Log OAuth refresh attempts for debugging
