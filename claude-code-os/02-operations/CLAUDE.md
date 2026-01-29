# Operations Project Instructions

## File Naming Standards

All saved files in `/02-operations/` must follow consistent naming conventions:

### Format
`descriptive_name_v{major.minor}_{YYYY-MM-DD}.{ext}`

### Examples
- `build_proposal_v1.0_2025-12-10.md`
- `workflow_diagram_v2.1_2025-12-10.pdf`
- `eugene_discovery_notes_v1.0_2025-12-09.md`
- `client_meeting_notes_v1.0_2025-12-08.md`

### Versioning Rules
- **v1.0** = Initial version
- **v1.1, v1.2, etc.** = Minor revisions (typos, clarifications, small additions)
- **v2.0, v3.0, etc.** = Major revisions (scope changes, new sections, significant rewrites)

### When to Increment
- **Minor (x.1):** Fix typos, add clarifications, update dates, minor formatting
- **Major (2.x):** Add new sections, change structure, expand scope, incorporate feedback

### Date Format
- Always use ISO 8601: `YYYY-MM-DD`
- Date represents when the file was created/modified, not content date

### File Naming Tips
- Use underscores `_` for word separation (not hyphens or spaces)
- Be descriptive but concise
- Include project name when relevant (`eugene_`, `client_x_`)
- Avoid special characters except underscore and dot

### Archival
- When creating major version bump, archive previous version to `.archive/` folder
- Keep archive structure: `.archive/filename_v1.0_2025-12-10.md`

---

## Folder Structure

### Technical Builds
All technical implementation documents go in the centralized location:

**Path:** `/02-operations/technical-builds/`

**Structure:**
```
/02-operations/technical-builds/
├── eugene/               # Eugene's AMA Capital projects
├── lombok-invest-capital/  # Lombok projects
├── shared/               # Shared/reusable components
└── [client-name]/        # Other client projects
```

**Examples:**
- `/02-operations/technical-builds/eugene/build_proposal_v1.0_2025-12-10.md`
- `/02-operations/technical-builds/shared/email_template_library_v1.0_2025-12-01.md`

**Do NOT create technical-builds folders inside individual project folders.**
✅ Correct: `/02-operations/technical-builds/eugene/`
❌ Wrong: `/02-operations/projects/eugene/technical-builds/`

---

## File Placement Rules (MANDATORY)

**CRITICAL: NEVER save files to the root `/coding_stuff/` directory. Always place files in the correct project folder.**

### Root Directory - ONLY These Files Allowed

- `CLAUDE.md` - Main instructions
- `PROJECT_REFERENCE.md` - Project reference
- `README.md` - Repository overview
- `CREDENTIALS.md` - Credentials reference

**Everything else goes into organized folders.**

### Where Files Go

| File Type | Destination |
|-----------|-------------|
| Eugene project files (iterations, docs, dual classification) | `/02-operations/technical-builds/eugene/` (use `iterations/`, `documentation/` subfolders) |
| Expense System / W2 files | `/02-operations/technical-builds/oloxa/SwaysExpenseSystem/documentation/` |
| SOP Builder files | `/02-operations/technical-builds/oloxa/SopBuilder/documentation/` |
| OAuth / monitoring system docs | `/claude-code-os/00-system-docs/` |
| Session summaries / work logs | `/session-summaries/` |
| Test reports | Inside the relevant project's `tests/` subfolder |
| Scripts (project-specific) | Inside the relevant project's `scripts/` subfolder |
| Scripts (global) | `/scripts/` |

### Before Saving ANY File

1. **What project is this for?** → Find its folder in `technical-builds/` or `projects/`
2. **What type?** → Use the correct subfolder (`documentation/`, `iterations/`, `tests/`, `scripts/`)
3. **Is it truly global?** → Only then use `00-system-docs/` or `session-summaries/`
4. **NEVER save to root** — no exceptions
