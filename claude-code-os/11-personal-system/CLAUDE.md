# Personal System - Claude Instructions

## Purpose
This file configures how Claude handles personal and family tasks within the 11-personal-system department.

## Notion Integration

### Database Configuration
- **Database ID:** `889fff97-1c29-490b-a57c-322c0736e90a`
- **Database URL:** https://www.notion.so/889fff971c29490ba57c322c0736e90a

### Adding Personal Tasks

When the user requests to add a personal task, use `mcp__notion__API-post-page` to create a new task with these properties:

```json
{
  "parent": { "database_id": "889fff97-1c29-490b-a57c-322c0736e90a" },
  "properties": {
    "Name": {
      "title": [{ "text": { "content": "Task name here" } }]
    },
    "When": {
      "date": { "start": "YYYY-MM-DD" }
    },
    "Priority": {
      "select": { "name": "Medium" }  // Options: "High🔥", "Medium", "Low"
    },
    "Description": {
      "rich_text": [{ "text": { "content": "Additional details" } }]
    }
  }
}
```

**Defaults:**
- Priority: "Medium" (unless user specifies High or Low)
- Complete: false (unchecked by default)
- When: Parse from user's natural language (e.g., "Saturday", "December 24th", "tomorrow")

### Querying Personal Tasks

For check-in queries like "What personal tasks do I have this weekend?", use `mcp__notion__API-post-database-query`:

```json
{
  "database_id": "889fff97-1c29-490b-a57c-322c0736e90a",
  "filter": {
    "and": [
      { "property": "Complete", "checkbox": { "equals": false } },
      { "property": "When", "date": { "on_or_after": "start_date" } },
      { "property": "When", "date": { "on_or_before": "end_date" } }
    ]
  },
  "sorts": [{ "property": "When", "direction": "ascending" }]
}
```

**Common Query Patterns:**
- "this weekend": Friday to Sunday of current week
- "tomorrow": Next day
- "this week": Monday to Sunday of current week
- "upcoming": Next 7 days

## Google Calendar Integration

### Calendar Configuration
- **Calendar:** Gmail calendar (primary)
- **Calendar ID:** To be determined after authentication

### Adding Events

When adding personal tasks, also create calendar events using `mcp__google-calendar__create-event`:

**All-Day Events** (when no time specified):
```json
{
  "calendarId": "primary",
  "summary": "Task name",
  "start": "2025-12-24",
  "end": "2025-12-25",
  "reminders": {
    "useDefault": false,
    "overrides": [{ "method": "popup", "minutes": 1440 }]  // 1 day before
  }
}
```

**Timed Events** (when specific time given):
```json
{
  "calendarId": "primary",
  "summary": "Task name",
  "start": "2025-12-24T14:00:00",
  "end": "2025-12-24T15:00:00",
  "reminders": {
    "useDefault": false,
    "overrides": [{ "method": "popup", "minutes": 1440 }]
  }
}
```

**Reminder Settings:**
- Default: Day before (1440 minutes)
- Custom: Parse from user (e.g., "remind me Friday" when task is Saturday)

### Time Parsing Rules
- **No time specified:** Create all-day event
- **Time specified:** (e.g., "at 2pm", "3:30pm") Create timed event
- **Duration:** Default 1 hour for timed events unless specified

## Natural Language Processing

### Trigger Phrases for Personal Tasks
- "Personal task: ..."
- "Add personal: ..."
- "Family task: ..."
- "Add to personal: ..."
- "Remind me to ..." (if context indicates personal)

### Date Parsing Examples
- "Saturday" → Next Saturday
- "December 24th" → 2025-12-24
- "tomorrow" → Current date + 1
- "next week" → 7 days from now
- "this weekend" → Next Saturday

### Priority Parsing
- "urgent", "important", "asap" → High🔥
- "low priority", "whenever" → Low
- Default → Medium

## Notes Management

The `notes.md` file in this directory stores:
- Family birthdays and important dates
- Recurring reminders
- Personal preferences and context
- Quick reference information

When user says "Add to my personal notes: ...", append to the notes.md file.

## Workflow Examples

### Example 1: Simple Task
**User:** "Personal task: Pick up cake for daughter's birthday by Saturday"

**Actions:**
1. Add to Notion with Name="Pick up cake for daughter's birthday", When=next Saturday, Priority=Medium
2. Add to Google Calendar as all-day event on Saturday with reminder Friday
3. Confirm to user: "Added personal task to Notion and Calendar"

### Example 2: Timed Task with Custom Reminder
**User:** "Personal task: Dentist appointment Tuesday at 2pm, remind me Monday"

**Actions:**
1. Add to Notion with Name="Dentist appointment", When=next Tuesday, Priority=Medium
2. Add to Google Calendar as timed event Tuesday 2:00-3:00pm with reminder Monday
3. Confirm to user

### Example 3: Check-in Query
**User:** "What personal tasks do I have this weekend?"

**Actions:**
1. Query Notion for incomplete tasks with When between Friday and Sunday
2. Present results in readable format with dates and priorities
3. Optionally suggest which tasks are most urgent

## Important Notes

- **Simplicity:** Don't overcomplicate - just add tasks to existing database
- **No special filtering:** User will manage personal vs work tasks themselves
- **Flexible time handling:** Support both all-day and timed events based on user input
- **Experimentation:** User will determine if both Notion and Calendar are useful or if one is sufficient
