# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository serves two primary purposes:
1. **Public Issue Tracker**: GitHub Issues are used to track GameMaker bugs and feature requests
2. **Release Notes Website**: A Jekyll-based site at https://releases.gamemaker.io/ that hosts release notes for all GameMaker versions (Monthly, LTS, and Beta releases)

## Repository Structure

### Core Directories

- **docs/**: Jekyll site content and configuration
  - **release-notes/**: Organized by year (e.g., `2024/`, `2023/`, `2022/`)
    - Each major version has its own file (e.g., `1400.md`, `1300.md`, `1100.md`)
    - Individual monthly releases are numbered (e.g., `13.md` for 2024.13)
  - **_includes/**: Reusable Jekyll components (`note.html`, `important.html`, `warning.html`, `tip.html`, `image.html`)
  - **_layouts/**: Jekyll layout templates
  - **assets/**: CSS, FontAwesome, and images (monthly.jpg, beta.jpg, lts.jpg)
  - **_config.yml**: Jekyll configuration for the site
  - **index.md**: Main landing page showing current Monthly, LTS, and Beta versions

- **.github/**: GitHub configuration
  - **ISSUE_TEMPLATE/**: Multiple issue templates for different bug types:
    - `ide_bug_report.yml` - General IDE bugs
    - `build_gmrt_report.yml` / `build_gms2_report.yml` - Build system bugs
    - `in-game_gmrt_report.yml` / `in_game_gms2_report.yml` - Runtime bugs
    - `docs_bug_report.yml` - Manual/documentation bugs
    - `extension_bug_report.yml` - Extension bugs
    - `feature-request.yml` - Feature requests
    - `prefab_bug_report.yml`, `template_bug_report.yml`, `testframework_fail_report.yml`, `projecttool_bug_report.yml`
  - **workflows/**: GitHub Actions for automated issue management
    - `duplicate-detection.yml` - AI-powered semantic duplicate detection (checks new issues against last 500 issues)
    - `dedupe.yml` - Legacy duplicate detection using genai-issue-dedup action
    - `tag-duplicate.yml` - Manual duplicate tagging via `/duplicate` command

- **Tools/**: Python utility scripts for release note generation
  - `compareGMLSpec.py` - Compares two GMLSpec.xml files to identify new/deleted/changed functions, variables, constants, structs, and enums
  - `createGMLSpecReleaseNotes.bat` - Batch script that runs compareGMLSpec.py for multiple platforms (main, PS4, PS5, Switch, Xbox)

## Release Notes Format

Release notes follow a consistent structure:

### Version Numbering
- Beta versions: `2024.1400` (format: year.major_minor_build)
- Monthly releases: `2024.13.1` (format: year.month.patch)
- LTS releases: `2022.0.3`

### Release Note Structure
Each release note file includes:
- YAML frontmatter with `layout: home`
- Version number and download links for Windows, macOS, and Ubuntu
- Important notices using `{% include important.html content="..." %}`
- Sections for each beta/update with:
  - Milestone query links to GitHub Issues
  - Release date
  - Categorized changes (new features, stability fixes, IDE changes, runtime changes)
  - Issue references with `[#issue_number]` linking to GitHub

### Jekyll Includes
Use these includes for special callouts:
- `{% include important.html content="text" %}` - Important notices
- `{% include note.html content="text" %}` - General notes
- `{% include warning.html content="text" %}` - Warnings
- `{% include tip.html content="text" %}` - Tips
- `{% include inline_image.html file="filename.jpg" max-width="26" margin-bottom="-6" %}` - Inline images

## Working with Release Notes

### Adding a New Beta Release
1. Open the appropriate version file (e.g., `docs/release-notes/2024/1400.md`)
2. Add a new section at the top with format: `## Beta X - [IDE xxx/Runtime xxx Changes](GitHub_query_link) (Date)`
3. Include feature sections with issue references
4. Update the current version number in the page title

### Adding a New Monthly/LTS Release
1. Create a new markdown file in `docs/release-notes/YEAR/` (e.g., `14.md` for 2024.14)
2. Use existing files as templates for structure
3. Update `docs/index.md` to add the new release to the appropriate section (Monthly/LTS/Beta)

## Issue Reporting Guidelines

Users are directed to:
1. Update GameMaker to the latest version before reporting
2. Check logs (ui.log, compiler log) for setup issues
3. Search existing issues to avoid duplicates
4. Use the appropriate issue template
5. Use GameMaker's built-in "Report A GameMaker Bug" tool (Help menu) for automatic log/sample submission

Feature requests go through a review process:
- Reviewed by multidisciplinary team
- Evaluated for possibility, difficulty, usability, and value
- Either rejected with reason or added to backlog for voting
- Closed when implemented (may not have advance notification)

## Development Tools

### GMLSpec Comparison Tool
`compareGMLSpec.py` is used to generate markdown-formatted lists of API changes:
- Usage: `python compareGMLSpec.py <new_GMLSpec.xml> <old_GMLSpec.xml>`
- Outputs sections for: New/Deleted/Changed Functions, Variables, Constants, Structs, Enums
- Function format includes parameters with optional parameter notation `[param]`
- Can search manual for documentation URLs (commented out in current version)

The batch script `createGMLSpecReleaseNotes.bat` automates this for multiple platforms, but has hardcoded local paths that need to be updated for each environment.

## Automated Workflows

### Duplicate Issue Detection
The repository has multiple systems to prevent duplicate issue reports:

**Enhanced Duplicate Detection** (`duplicate-detection.yml`):
- Triggered on new/reopened/edited issues
- Uses semantic similarity (sentence transformers) + keyword matching to find duplicates
- Searches last 500 issues (open and closed) for potential matches
- Scoring algorithm:
  - 60% semantic similarity (using all-MiniLM-L6-v2 model)
  - 40% keyword overlap (extracts error messages, function names, code snippets)
  - Bonus: Label matching (+0.1 per matching label, up to +0.3)
- Reports top 5 matches with >75% similarity in a comment
- Automatically adds "possible duplicate" label if top match is >85% similar
- Skips issues already marked as duplicate

**Manual Duplicate Tagging** (`tag-duplicate.yml`):
- Allows maintainers to comment `/duplicate` to add the duplicate label
- Used when manual review confirms a duplicate

### Dependencies for Duplicate Detection
The enhanced workflow requires these Python packages:
- `PyGithub` - GitHub API interaction
- `sentence-transformers` - Semantic text similarity
- `scikit-learn` - Cosine similarity calculation
- `numpy` - Numerical operations (installed with scikit-learn)
