# 11 - Personal System

## Department Mission
Manage personal and family tasks separately from work, providing a dedicated space for household errands, family activities, and personal reminders.

## Status
**Phase:** Initial Setup
**Started:** 2025-12-14

## Overview
The Personal System department integrates with your existing Notion Tasks database and Google Calendar to help manage personal life alongside work. This system allows you to add personal tasks (like picking up groceries, family birthdays, household errands) without mixing them with work tasks.

## Key Features
- **Task Management:** Add personal tasks to Notion Tasks database
- **Calendar Integration:** Sync tasks to Google Calendar (Gmail) with reminders
- **Check-in Queries:** Ask about upcoming personal tasks
- **Family Notes:** Maintain running notes about important dates and preferences

## Integration Points

### Notion Tasks Database
- **Database ID:** `889fff97-1c29-490b-a57c-322c0736e90a`
- **URL:** https://www.notion.so/889fff971c29490ba57c322c0736e90a
- **Properties Used:**
  - Name (title): Task description
  - When (date): Due date
  - Priority (select): High🔥 / Medium / Low
  - Description (rich_text): Additional details
  - Complete (checkbox): Task status

### Google Calendar
- **Calendar:** Gmail calendar (to be configured after auth)
- **Event Types:**
  - All-day events (default when no time specified)
  - Timed events (when specific time is provided)
- **Reminders:** Day before by default, or as specified

## Usage Examples

### Adding Tasks
- "Personal task: Pick up cake for daughter's birthday by Saturday, remind me Friday"
- "Personal task: Dentist appointment Tuesday at 2pm, remind me Monday"
- "Add to personal: Get chicken for Christmas dinner December 24th"

### Check-ins
- "What personal tasks do I have this weekend?"
- "Any personal tasks for tomorrow?"
- "Show me upcoming family tasks"

### Notes Management
- "Add to my personal notes: Daughter's birthday is March 15th"
- "Add to notes: Wife prefers chocolate cake from Baker's Shop"

## Current Status
- ✅ Department structure created
- ✅ Configuration files in place
- ⏳ Google Calendar authentication pending
- ⏳ Testing workflows

## Next Steps
1. Test adding personal tasks to Notion
2. Verify query functionality
3. Fix Google Calendar authentication
4. Test calendar integration with reminders
5. Iterate based on usage patterns
