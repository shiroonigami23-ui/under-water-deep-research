# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## [3.0.0] - 2026-11-15 — Encyclopedia website

### Added
- Multi-page site generator `scripts/build_site.py` (Markdown + JSON → static site) with search, dark/light theme, TOC, sources page, glossary, timeline and about pages
- Species Atlas (72 entries) and Seas & Oceans (26 entries) catalogs with filters, sortable table and depth charts
- 39 footnoted articles in 8 sections, including new climate pages (ocean heat 2025, acidification boundary, deoxygenation) and impacts pages (bottom trawling, plastics, MPAs and 30×30, UNCLOS/ISA/BBNJ)
- Live research tracker shown on every page as a collapsible bar, plus a tracker page with anchored, expandable streams
- Paper analyses exported to PDF (open in a new tab or download)
- Real species and sea photos loaded live from Wikimedia Commons with credits; `wiki/photo-status.html` and `prompts.md` give Nano Banana prompts for anything missing

### Changed
- The root `index.html` is now the generated encyclopedia home page
- CI builds the site and link-checks the generated HTML

### Removed
- Cross-links to the outer-space repository (the two hubs are now fully separate)

## [2.0.0] - 2026-11-15 — Research hub

### Added
- Three new tracks: `exploration/`, `governance-and-mining/`, `ocean-change/` (notes + 8 generated figures)
- `papers/`: structured deep reads of Peng 2025, Jones 2025, Sweetman 2024, Bell 2025, Portmann 2026 + reading list
- `labs/dive-profile-lab.html`: interactive depth explorer (pressure, light, temperature, Boyle's law, life zones, records)
- `index.html` GitHub Pages hub homepage (+ `.nojekyll`)
- `GLOSSARY.md`, `scripts/generate_figures.py`, `scripts/check_links.py`, `.github/workflows/validate.yml`

### Changed
- Tracker fully refreshed to 15 Nov 2026 (status board, details, monthly digest; April snapshot archived)
- `biology/ongoing-studies-2025-2026.md`: Ocean Census year 3, hadal records, mining-impact biology; High Seas Treaty status confirmed
- README, ROADMAP, ARCHITECTURE and IMAGE-SOURCES updated

## [1.0.1] - 2026-11-13

### Documentation
- Rewrote README with badges, preview, feature & tech-stack tables, architecture diagram and roadmap
- Added `docs/ARCHITECTURE.md` (components, data flow, design decisions)
- Added `docs/ROADMAP.md` (milestones and long-term vision)
- Added project banner (`assets/banner.svg`), SSH / GitHub CLI / ZIP / Codespaces access options and a `.devcontainer`

## [1.0.0] - 2026-04-19

### Added
- Biology track
- Structure track
- Physics & chemistry
- Deep-water types
- Mutation & adaptation
- Live Evolution Lab
- Evolution Timeline Tree
- Research tracker
