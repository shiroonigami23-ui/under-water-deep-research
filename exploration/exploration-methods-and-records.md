# Exploration Methods and Records

Status date: November 15, 2026.

## Three pillars of ocean exploration

| Pillar | Tools | What it gives | Global coverage |
|---|---|---|---|
| Mapping | Ship multibeam sonar, AUVs, crowd-sourced bathymetry, satellite altimetry (coarse) | Shape of the seafloor | **28.7%** to modern standard (Seabed 2030, Apr 2026) |
| Imaging | ROVs, crewed submersibles, towed cameras, baited landers | What lives there, behaviour, habitat | **≈0.001%** ever imaged (Bell et al. 2025) |
| Sampling | Cores, nets, slurp guns, eDNA | Species ID, chemistry, genomes | Tiny; strongly biased to a few regions |

## Mapping: Seabed 2030

- Coverage was 6% at launch (2017), 23.4% (2022), 27.3% (June 2025) and **28.7% (April 2026)**. About five million km² were added in the year to April 2026, for roughly 104 million km² mapped.
- All shared data goes into the free GEBCO global grid.
- **My working read:** ~1.4–1.6 percentage points per year is far below the ~18 points/year needed to finish by 2030 (see `png/seabed2030_progress_generated.png`). Crowd-sourced bathymetry and uncrewed surface vessels are the levers that could change that slope.

## Imaging: "How little we've seen" (Bell et al. 2025, *Science Advances*)

- Compiled ~44,000 deep dives with visual observations since 1958.
- Total area ever imaged: about 2,130–3,823 km², which is ≤0.001% of the deep seafloor (roughly a tenth of Belgium).
- **Bias:** 65% of observations fall within 200 nautical miles of the USA, Japan or New Zealand. 97% of dives come from five countries (USA, Japan, NZ, France, Germany).
- Abyssal plains and seamounts are under-observed relative to canyons and ridges. Monterey Canyon alone accounts for ~48% of global canyon observations.
- See the full analysis in [`../papers/bell-2025-how-little-weve-seen.md`](../papers/bell-2025-how-little-weve-seen.md).

## Depth records for life

| Record | Depth | Where / how | Year |
|---|---|---|---|
| Deepest fish filmed | 8,336 m | Juvenile *Pseudoliparis* snailfish, Izu-Ogasawara Trench, baited lander | Aug 2022 (published 2023) |
| Deepest fish caught | 8,022 m | *P. belyaevi*, Japan Trench, traps | 2022 |
| Deepest chemosynthetic animal community | 9,533 m | Siboglinid tubeworms + bivalves, Kuril–Kamchatka Trench, crewed sub *Fendouzhe* | 2024 dives, *Nature* 2025 |

- **Why fish stop at ~8,200–8,400 m:** pressure destabilises proteins. Fish counter this with the osmolyte TMAO, but rising TMAO raises internal osmotic concentration until it would exceed seawater at ~8,200 m. Invertebrates don't share that ceiling, which is why tubeworms live deeper than any fish.

## Platforms to know

- **Crewed:** *Fendouzhe* (China, full-ocean depth), *Alvin* (USA, upgraded to 6,500 m), *Limiting Factor* (full-ocean-depth, commercial).
- **Uncrewed:** ROVs like *SuBastian* (Schmidt Ocean Institute) and *Isis* (NOC); AUVs for mapping; landers for long-duration chemistry (the dark-oxygen work).
- **Genetic:** eDNA lets surveys detect species from water samples without capture.

## Open Questions

- Can low-cost, mass-produced cameras and landers (the Ocean Discovery League approach) lift the imaged fraction by orders of magnitude?
- How representative are hadal communities found at subduction-zone seeps? The 9,533 m paper argues they may be widespread, but only one region has been surveyed.

## Sources

- Seabed 2030 / IHO, 28.7% milestone (Apr 2026): https://iho.int/en/global-seabed-mapping-reaches-new-milestone-as-five-million-square-kilometres-added-in-a-year
- Nippon Foundation, 27.3% (2025) and 6% at 2017 launch: https://tnfsa.nippon-foundation.or.jp/news/2756701
- Bell et al. 2025, *Sci. Adv.* 11(19), doi:10.1126/sciadv.adp8602 · coverage: https://news.mongabay.com/2025/05/only-a-tiny-of-the-deep-seafloor-has-ever-been-visually-observed-study/
- Peng, Du et al. 2025, *Nature*, doi:10.1038/s41586-025-09317-z · summary: https://www.natureasia.com/ja-jp/nature/pr-highlights/15298
- Snailfish records, NHM (2023): https://nhm.ac.uk/discover/news/2023/april/deepest-ever-fish-filmed-depth-8336-metres.html
