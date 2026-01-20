# [Project Name] - Version Log

**Project**: [Brief project description]
**Location**: `/path/to/project/folder`
**Current Version**: v0.0.0
**Last Updated**: [Date]

---

## Quick Reference

| Version | Status | Date | Phase | Notes |
|---------|--------|------|-------|-------|
| v0.0.0 | 🚧 Draft | YYYY-MM-DD | Planning | Initial draft |

---

## Versioning Scheme

**Format**: `MAJOR.MINOR.PATCH`

- **MAJOR (v1.x.x)**: Breaking changes, complete rewrites, new major milestones
  - Example: v1.0.0 = Foundation complete
  - Example: v2.0.0 = Full automation operational

- **MINOR (vx.1.x)**: New features, significant enhancements, backward compatible
  - Example: v1.1.0 = New workflow added
  - Example: v1.2.0 = Major feature enhancement

- **PATCH (vx.x.1)**: Bug fixes, small improvements, refinements
  - Example: v1.0.1 = Bug fix
  - Example: v1.0.2 = Configuration tweak

---

## Version History

### v0.0.0 - Project Initialization
**Date**: YYYY-MM-DD
**Status**: 🚧 Draft
**Phase**: Planning

#### Components Created
- [List what was created in this version]
- Component 1: Description
- Component 2: Description

#### What Works
✅ [List what's functional]

#### What Doesn't Work Yet
❌ [List what's not implemented]

#### Known Issues
⚠️ [List known bugs or limitations]

#### Blockers
🔴 **Critical**: [Critical blockers]
🟡 **Important**: [Important but not blocking]

#### Rollback Instructions
**To roll back from this version**:
1. [Step-by-step rollback instructions]
2. [Include IDs, file paths, commands]
3. [Verification steps]

#### Files & Resources
- [List all important files, IDs, URLs]
- Design doc: `/path/to/design.md`
- Google Drive folder ID: `1234567890`
- n8n workflow ID: `abcdefgh`

#### Next Version Goal
**v0.1.0 - [Next milestone name]**
- [What will be built]
- [Success criteria]
- [Estimated effort if applicable]

---

## Planned Versions

### v0.1.0 - [Milestone Name]
**Target Date**: TBD
**Components to Build**:
- [List components]

**Success Criteria**:
- [Define success]

### v1.0.0 - [Major Milestone]
**Target Date**: TBD
**What Makes v1.0.0**:
- [List what constitutes v1.0]
- [Minimum viable functionality]

---

## Component Inventory

### Google Drive Resources (if applicable)
| Component | ID | Version | Status |
|-----------|----|---------| ------|
| Root Folder | `folder-id-here` | v0.0.0 | ✅ Active |

### n8n Workflows (if applicable)
| Workflow | ID | Version | Status |
|----------|----|---------| ------|
| Workflow 1 | `workflow-id` | v0.0.0 | ✅ Active |

### Google Sheets (if applicable)
| Sheet | ID | Version | Status |
|-------|----|---------| ------|
| Database | `sheet-id` | v0.0.0 | ✅ Active |

### Documentation Files
| File | Location | Version | Status |
|------|----------|---------|--------|
| Design Doc | `/path/to/file.md` | v0.0.0 | ✅ Complete |
| Version Log | `/path/to/VERSION_LOG.md` | v0.0.0 | ✅ Active |

### Other Components
| Component | Type | ID/Location | Version | Status |
|-----------|------|-------------|---------|--------|
| [Name] | [Type] | [ID/path] | v0.0.0 | ✅ Active |

---

## Rollback Procedures

### General Rollback Process
1. **Identify target version** from version history
2. **Review what changed** between current and target
3. **Follow specific rollback instructions** for that version
4. **Verify all components** match target version state
5. **Update "Current Version"** at top of this document
6. **Test system** to ensure rollback successful

### Component-Specific Rollback

#### n8n Workflows
1. Navigate to workflow in n8n UI
2. Click ... menu > Versions
3. Export current workflow JSON as backup
4. Select target version to restore
5. Click "Restore" button
6. Reactivate workflow if needed
7. Test execution

#### Google Sheets
1. Navigate to sheet
2. File > Version history > See version history
3. Find version matching target timestamp
4. Export current version as backup
5. Click "Restore this version"
6. Verify column headers and data

#### Google Drive Folders
1. Identify folders created in newer version
2. Move/delete folders as needed
3. Restore folders from trash if deleted
4. Verify folder IDs match target version
5. Use `mcp__google-drive__listFolder` to verify structure

#### Local Files
1. If using git: `git checkout <commit-hash> -- <file-path>`
2. Otherwise: Restore from dated backups
3. Verify file contents match target version

---

## Version Update Checklist

**Before creating a new version**:
- [ ] Export current n8n workflows as JSON backups
- [ ] Export Google Sheets as CSV/Excel backups
- [ ] Document current system state
- [ ] Test rollback to previous version

**When creating a new version**:
- [ ] Update "Current Version" and "Last Updated" at top
- [ ] Add new version entry with complete details
- [ ] Document all components created/modified
- [ ] List what works and what doesn't
- [ ] Document known issues and blockers
- [ ] Provide clear rollback instructions
- [ ] Update component inventory with new IDs/versions
- [ ] Test new components thoroughly
- [ ] Export workflow JSONs to blueprints folder

**After creating a new version**:
- [ ] Tag version in git (if using version control)
- [ ] Update related documentation
- [ ] Archive previous version files to `_archive/`
- [ ] Update MY-JOURNEY.md with milestone (if significant)

---

## Critical Technical Notes

### [Technical Pattern 1]
- **Problem**: [What problem this solves]
- **Solution**: [How it's solved]
- **Applied In**: [Where this pattern is used]
- **Example**:
```
[Code or configuration example]
```

### [Technical Pattern 2]
- **Implementation**: [How it works]
- **Benefit**: [Why this approach]
- **Caveat**: [Any gotchas or limitations]

---

## Blueprint File Naming Convention

**Format**: `{component_name}_v{version}_{date}.json`

**Examples**:
- `workflow1_v1.0_20251230.json`
- `database_schema_v1.2_20251230.json`
- `_archived/workflow1_v0.8_20241225_ARCHIVED.json`

**Archive Format**: `_archived/{component_name}_v{version}_{date}_ARCHIVED.{ext}`

---

## Notes

- **Version numbers are permanent** - never reuse or skip
- **Document ALL breaking changes** clearly
- **Always test rollback procedures** before deployment
- **Keep JSON exports** of all workflows for each version
- **This is a living document** - update as system evolves

---

## Questions & Support

For questions about this project:
1. Review the design document (if applicable)
2. Check component inventory for IDs and URLs
3. Review known issues for current blockers
4. Consult rollback procedures for recovery steps

**Last reviewed**: YYYY-MM-DD
