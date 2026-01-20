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
