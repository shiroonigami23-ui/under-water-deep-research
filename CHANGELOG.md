# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).



## [Unreleased] - 2026-11-17 (homepage and tracker)
### Changed
- Homepage catalogs grouped into themed blocks with one-line blurbs; the Browse menu uses the same groups.
- Bigger hero search with suggested searches.
### Added
- Weekly GitHub Action (`update-tracker.yml`) that fetches the newest papers for each live-tracker stream from OpenAlex, adds a 'Latest research' section to the tracker page, updates the tracker date and rebuilds the site.

## [Unreleased] - 2026-11-17
### Added
- In-site reader (`wiki/read.html`): every Wikipedia link now opens the full article inside this site, with images, contents and links that stay in the site; pages we have our own article for open those instead.
### Fixed
- Portrait photos no longer crop off people's heads: crops favour the top of the image and tall portraits are shown whole on article pages.
## [Unreleased] - 2026-11-15
### Added
- More animations: scroll-reveal for cards, charts and sections; count-up hero statistics; 3D tilt on cards; reveal failsafe so content is never hidden.
### Changed
- Generator hardening (numeric subtitles), hero animation scoped per site.
- In-depth rewrite of 45 sea profiles (overview, geography, seafloor, water, climate, life, ecosystems, history, people and threats), including the Gulf of California, Mediterranean, Bay of Bengal and Arabian Sea.

## [3.2.0] - 2026-11-15 — In-depth entries, research panels, auto-sound, larger layout

### Added
- **In depth** section on every catalog entry: the full Wikipedia article (description, habitat, diet, reproduction, behaviour, conservation, research, history…) loaded live into collapsible sections, with links to pages in this encyclopedia
- **Research & studies** panel on every entry: most-cited and newest papers from OpenAlex, with free PDF links
- Sounds load and try to play automatically when a page opens, with a written 'What it sounds like' note (including when an animal is silent or has never been recorded)
- 1,072 species (+69, many from Indian waters), sound descriptions for every species

### Changed
- Fluid, larger layout that fills tablets and wide screens; Sources moved below the in-depth content

## [3.1.0] - 2026-11-15 — 1,000+ species, connections and navigation

### Added
- Species Atlas expanded to 1,003 entries, including rivers and estuaries, seabirds, plants and microbes
- 45 seas, gulfs and bays with in-depth sections; automatic links between seas, species, rivers and wrecks; 'At a glance' summaries
- Rivers & Estuaries, Shipwrecks & Discoveries, Ocean Phenomena and Research Papers catalogs
- Built-in PDF reader for openly licensed papers and `fetch-papers.yml` to mirror them
- Sounds for whales, dolphins, seals, seabirds and noisy fish; Wikipedia overviews on every entry
- Animated charts, Statistics page, animated hero
- New navigation: Browse mega-menu, instant search (`/`), mobile tab bar, compact footer with a collapsible site map, back-to-top

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
