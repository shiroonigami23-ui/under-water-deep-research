"""Generate the hub's original figures from cited values.

Run:  python scripts/generate_figures.py      (needs numpy, matplotlib, pillow)
Values and sources are listed next to each function and in IMAGE-SOURCES.md.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BG, FG, MUTED, GRID = "#04121f", "#e6f1fb", "#8fb3cc", "#16324a"
C = ["#4fc3f7", "#26a69a", "#ffb74d", "#ef5350", "#ab47bc", "#9ccc65", "#90caf9"]
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "axes.edgecolor": GRID, "axes.labelcolor": FG, "text.color": FG,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.6, "font.size": 11,
    "axes.titleweight": "bold", "axes.titlesize": 14, "legend.frameon": False,
})


def save(fig, track, name):
    d = os.path.join(ROOT, track, "png"); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name); fig.tight_layout(); fig.savefig(p, dpi=150); plt.close(fig)
    print("wrote", os.path.relpath(p, ROOT))


# ------------------------------------------------------------ exploration
def mapping_progress():
    # Seabed 2030 announcements: 6% (2017 launch), 23.4% (2022), 27.3% (Jun 2025), 28.7% (Apr 2026)
    yrs, pct = [2017, 2022, 2025, 2026], [6, 23.4, 27.3, 28.7]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(yrs, pct, color=C[0], marker="o", lw=2.5, ms=9, label="Mapped to modern standards")
    for y, p in zip(yrs, pct):
        ax.annotate(f"{p}%", (y, p), xytext=(0, 10), textcoords="offset points", ha="center")
    ax.plot([2026, 2030], [28.7, 100], color=C[2], ls="--", lw=1.5, label="Pace needed for 100% by 2030")
    slope = (28.7 - 27.3) / 0.85
    ax.plot([2026, 2030], [28.7, 28.7 + slope * 4], color=C[3], ls=":", lw=2, label="Current pace (≈1.6 pts/yr)")
    ax.set_ylim(0, 105); ax.set_xlim(2016, 2031)
    ax.set_xlabel("Year"); ax.set_ylabel("% of global seafloor mapped")
    ax.set_title("Seabed 2030: mapping progress vs the 2030 goal"); ax.legend(loc="upper left")
    save(fig, "exploration", "seabed2030_progress_generated.png")


def seen_vs_mapped():
    # Bell et al. 2025 (Sci. Adv.): <=0.001% imaged; Seabed 2030: 28.7% mapped
    fig, ax = plt.subplots(figsize=(9, 4.2))
    labels = ["Mapped (sonar, Seabed 2030 2026)", "Ever seen by camera (Bell et al. 2025)"]
    vals = [28.7, 0.001]
    ax.barh(labels, vals, color=[C[0], C[2]])
    ax.set_xscale("log"); ax.set_xlim(1e-4, 100)
    for i, v in enumerate(vals):
        ax.text(v * 1.3, i, f"{v}%", va="center", fontsize=12, weight="bold")
    ax.set_xlabel("% of deep seafloor (log scale)")
    ax.set_title("We have mapped ~29% of the seafloor but seen only ~0.001%")
    save(fig, "exploration", "seen_vs_mapped_generated.png")


def depth_records():
    recs = [("Deepest fish filmed\n(snailfish, 2022)", 8336), ("Deepest fish caught\n(2022)", 8022),
            ("Deepest chemosynthetic\ncommunity (2024 dive)", 9533), ("Challenger Deep\n(ocean max)", 10935),
            ("Typical abyssal plain", 4500), ("Sunlight ends", 200)]
    recs.sort(key=lambda r: r[1])
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh([r[0] for r in recs], [r[1] for r in recs], color=[C[6], C[1], C[1], C[5], C[0], C[3]])
    for i, (_, d) in enumerate(recs):
        ax.text(d + 250, i, f"{d:,} m", va="center", ha="right", weight="bold")
    ax.invert_xaxis(); ax.yaxis.tick_right(); ax.set_xlim(12500, 0)
    ax.set_xlabel("Depth (m)"); ax.set_title("Life and records down the water column")
    save(fig, "exploration", "depth_records_generated.png")


# ------------------------------------------------------------ governance
def governance_timeline():
    D = lambda y, m, d=1: date(y, m, d).toordinal()
    ev = [(D(1979, 1), "1979 test-mining track\nin CCZ (studied 2023)", C[6]),
          (D(2023, 6, 19), "High Seas Treaty\nadopted", C[1]),
          (D(2024, 7, 22), "'Dark oxygen'\npaper", C[4]),
          (D(2025, 3, 26), "44-yr recovery\npaper (Nature)", C[5]),
          (D(2025, 9, 19), "60th BBNJ\nratification", C[1]),
          (D(2026, 1, 17), "BBNJ enters\ninto force", C[1]),
          (D(2026, 1, 21), "NOAA consolidated\npermit rule", C[3]),
          (D(2026, 7, 24), "ISA Council ends —\nno Mining Code", C[2]),
          (D(2026, 10, 13), "NOAA hearing on\nTMC application", C[3]),
          (D(2027, 1, 15), "BBNJ COP1\n(due ~Jan 2027)", C[1])]
    fig, ax = plt.subplots(figsize=(12, 4.6))
    xs = list(range(len(ev)))
    ax.plot(xs, [0] * len(xs), color=C[0], lw=3)
    for i, (_, l, c) in enumerate(ev):
        y = 0.55 if i % 2 == 0 else -0.65
        ax.plot([i, i], [0, y * 0.7], color=MUTED, lw=1)
        ax.scatter(i, 0, color=c, s=90, zorder=5)
        ax.text(i, y, l, ha="center", va="center", fontsize=9)
    ax.set_ylim(-1.2, 1.2); ax.axis("off")
    ax.set_title("Deep-sea governance & mining evidence timeline (event order, not to scale)")
    save(fig, "governance-and-mining", "governance_timeline_generated.png")


def recovery_bars():
    # Jones et al. 2025: qualitative pattern — mobile/small fauna partially return, sessile large fauna rare
    groups = ["Sediment & tracks", "Small mobile fauna", "Xenophyophores", "Large attached fauna\n(sponges, corals)"]
    status = [5, 55, 50, 10]  # illustrative recovery score
    fig, ax = plt.subplots(figsize=(9, 4.6))
    ax.barh(groups, status, color=[C[6], C[5], C[1], C[3]])
    ax.set_xlim(0, 100); ax.set_xlabel("Recovery after 44 years (illustrative scale, 100 = like unmined)")
    ax.set_title("1979 mining track, revisited 2023: who came back?")
    ax.text(60, -0.45, "Qualitative summary of Jones et al. 2025;\nnot measured percentages", color=MUTED, fontsize=9)
    save(fig, "governance-and-mining", "mining_track_recovery_generated.png")


# ------------------------------------------------------------ ocean change
def bleaching():
    ev = ["1st (1998)", "2nd (2010)", "3rd (2014–17)", "4th (2023–25)"]
    pct = [21, 37, 68.2, 84.4]
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(ev, pct, color=[C[2], C[2], C[3], C[3]])
    for b, p in zip(bars, pct):
        ax.text(b.get_x() + b.get_width() / 2, p + 1.5, f"{p}%", ha="center", weight="bold")
    ax.set_ylim(0, 100); ax.set_ylabel("% of reef area at bleaching-level heat stress")
    ax.set_title("Global coral bleaching events keep getting bigger (NOAA CRW)")
    save(fig, "ocean-change", "coral_bleaching_events_generated.png")


def amoc():
    fig, ax = plt.subplots(figsize=(9, 5))
    t = np.linspace(2000, 2100, 200)
    def path(frac):
        return 100 - frac * 100 * np.clip((t - 2000) / 100, 0, 1) ** 1.3
    ax.fill_between(t, path(0.43), path(0.59), color=C[3], alpha=0.3, label="Observation-constrained range: 43–59% weaker by 2100")
    ax.plot(t, path(0.51), color=C[3], lw=2.5, label="Central estimate ≈ 51%")
    ax.plot(t, path(0.20), color=C[5], lw=2, ls="--", label="Strong emission cuts ≈ 20%")
    ax.set_ylim(30, 105); ax.set_xlabel("Year"); ax.set_ylabel("AMOC strength (% of 2000 level)")
    ax.set_title("AMOC weakening projections (Portmann et al. 2026, schematic paths)")
    ax.legend(loc="lower left", fontsize=9)
    save(fig, "ocean-change", "amoc_projection_generated.png")


def pressure_light():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 6))
    z = np.linspace(0, 11000, 400)
    ax1.plot(1 + z / 10.06, z, color=C[0], lw=2.5)
    ax1.invert_yaxis(); ax1.set_xlabel("Pressure (atm) ≈ 1 + depth/10 m"); ax1.set_ylabel("Depth (m)")
    for d, l in [(200, "Twilight zone"), (1000, "Midnight zone"), (4000, "Abyss"), (6000, "Hadal zone")]:
        ax1.axhline(d, color=MUTED, lw=0.8, ls="--"); ax1.text(20, d - 120, l, color=MUTED, fontsize=9)
    ax1.set_title("Pressure: linear, ~1,090 atm at the bottom")
    z2 = np.linspace(0, 1000, 400)
    ax2.plot(100 * np.exp(-z2 / 23.0), z2, color=C[2], lw=2.5)
    ax2.set_xscale("log"); ax2.set_xlim(1e-10, 120); ax2.invert_yaxis(); ax2.set_xlabel("Surface light remaining (%), log")
    ax2.axhline(200, color=MUTED, lw=0.8, ls="--"); ax2.text(1e-9, 185, "~200 m: too dark for photosynthesis", color=MUTED, fontsize=9)
    ax2.set_title("Light: exponential, ~1% left by ~100 m")
    save(fig, "ocean-change", "pressure_light_profile_generated.png")


if __name__ == "__main__":
    mapping_progress(); seen_vs_mapped(); depth_records()
    governance_timeline(); recovery_bars()
    bleaching(); amoc(); pressure_light()
