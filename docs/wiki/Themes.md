# Themes — 4 Selectable Designs

## Overview

v2.3 ships **4 selectable themes**, persistent and exposed as a Home Assistant
select entity. Theme definitions live in **one file per theme** under
`esphome-modular-lvgl-buttons/common/themes/`:

| File | Theme |
|------|-------|
| `common/themes/classic.yaml` | Classic palette + styles |
| `common/themes/modern.yaml` | Modern palette, raised-face gradient, glow ring styles |
| `common/themes/performance.yaml` | Performance flat monochrome |
| `common/themes/daylight.yaml` | Daylight: warm raised dark cards + orange glow |
| `common/themes.yaml` | registry that includes the four files |

- **Classic** — original flat dark: black + slate gray tiles, single orange accent
- **Modern** — mockup look: navy, raised "3D" gradient tiles, orange glowing icons, green/blue AC buttons
- **Performance** — minimal monochrome, cheapest to render, fastest
- **Daylight** — warm dark variant with raised cards and orange accents/glows
  (a bright off-white palette was tried first and dropped as unreadable behind
  the AC/light artwork; the file keeps its `theme_daylight_*` style ids and
  `depth_light` / `glow_blue_light` names, which the repaint lambdas reference)

Every page (home, AC, light, settings, info) repaints itself on switch:
`apply_display_theme` (in `dashboards/home.yaml`) recolors the pages and then
calls `ac_main_refresh`, `apply_settings_theme`, `apply_info_theme`,
`button_7_apply_theme`, `update_settings_highlight`, `apply_dashboard_theme`
and every per-card `repaint_button_*` script — so on/off skins survive a
theme switch without a reboot.

Switch on device: Settings → Theme → [Classic] [Modern] [Perf] [Day],
or in HA: `select.display01_theme`.

## Theme 1: Classic

**Goal:** keep the original look — flat, balanced, cheapest after Performance.

**Palette (classic.yaml):**
- Page bg `0x000000`, settings/info bg `0x11151C`
- Tiles `0x343645` slate, active `0xF37320` orange (single accent)
- Text white, dim `0x9BA2BC`, muted `0xBBBBBB`
- Rows `0x1E232E`, selectors `0x3A4352`, radius 14, pad 10

**Home:** flat tiles, white labels, icons `0x9BA2BC` when off / white when on,
orange fill when active.

**AC:** Power ON `0x4CAF50`, Mode cool `0x2196F3` / heat `0xFF9800` /
dry `0xFFEB3B` / fan `0x4CAF50` / auto `0x9C27B0`; inactive `0x343645`;
arc track `0x2A2E3A`, indicator `0xFF9F1C`.

**Settings:** rows `0x1E232E` radius 10, orange sliders `0xFF9F1C`,
timeout slider blue `0x41BDF5`, saver switch green `0x4CAF50`.

**Reference images:** `docs/images/theme_classic_{home,ac,settings}.png`

## Theme 2: Modern — the mockup look

**Goal:** exactly the mockup images — dark navy, raised tiles, neon glows.

**Palette (modern.yaml):**
- Page bg `0x0A0E14`, settings `0x121A26`, info `0x0F141E`, AC `0x080A0F` / top bar `0x12151E`
- Raised tile face: vertical gradient `0x323B4D → 0x1A212C`, 1 px bevel `0x3D4658`, drop shadow (`depth_dark` style)
- Active/colored states get glow rings: `glow_orange` (0xFF8C00), `glow_green` (0x00E676), `glow_blue` (0x29B6F6), `glow_soft` (steppers)
- Icons orange `0xFF8C00`, labels gray `0x9BA2BC`, radius 20, pad 14

**Home:** all 10 cards are raised gradient tiles; active cards add an orange
glow ring; icons always orange.

**AC:** Power ON `0x00E676` black text + green glow; Mode COOL `0x29B6F6`
black text + blue glow; Turbo `0xFF6D00` + orange glow; −/+ steppers get the
soft `glow_soft` halo; arc indicator `0xFF8C00`.

**Settings:** rows `0x1E2530` radius 10, sliders orange `0xFF8C00`,
active selector buttons orange with glow ring.

**Reference images:** `docs/images/theme_modern_{home,ac,settings}.png` and
`docs/images/screen_ac.png`, `screen_settings.png`

## Theme 3: Performance — minimal for max speed

**Goal:** fewest draw calls and zero color logic.

**Palette (performance.yaml):**
- Everything black `0x000000` (pages + settings + info + AC)
- Tiles `0x1A1A1A`, active `0x444444` — grays only, no color anywhere
- Text white, dim `0x888888`; radius 4, pad 6; no borders, no shadows, no gradients

**Why faster:** radius 4 (less anti-aliasing), pad 6 (less layout), flat fills
only, monochrome (no color branching), no image backgrounds.

**Reference images:** `docs/images/theme_performance_{home,ac,settings}.png`

## Theme 4: Daylight — warm raised cards

**Goal:** the warm dark-orange-glow look of `docs/images/screen_light.png`
— readable, cozy, higher contrast accents.

**Palette (daylight.yaml):**
- Page bg `0x0B0C0D`, settings/info `0x0F1216`, AC `0x0B0C0D` / top bar `0x191D23`
- Raised card face: gradient `0x1F242C → 0x151A20`, 1 px border `0x242A33`,
  soft shadow (`depth_light` style)
- Accent orange `0xE37220`, bright accent `0xF8953D` (icons), glow `0xE37220`
- Text white, dim `0xB4B8BC`, muted `0x8A9099`; radius 20, pad 14
- Active tiles: solid `0xE37220` fill + warm glow (`glow_blue_light` — id kept
  for the repaint lambdas, now warm orange)

**Home:** raised dark cards; active cards fill solid orange with a warm glow;
icons `0xF8953D` when on, `0x8A9099` when off.

**AC:** Power ON `0x4CAF50` white text, Mode COOL `0x29B6F6` white text,
raised `0x191D23` buttons with `0x242A33` borders, arc `0xE37220`, back chip
border/text `0xF8953D`.

**Settings:** rows `0x171A1F` radius 12 with `0x2E3542` border + soft shadow,
sliders `0xE37220`, knobs `0xF8953D`.

**Reference images:** `docs/images/theme_daylight_{home,ac,settings}.png` and
`docs/images/screen_light.png`

## Adding a theme

See the cookbook in [`AGENTS.md`](../../AGENTS.md#8-cookbook--common-changes):
copy a palette file, register it in `common/themes.yaml`, add the select option
+ settings button, extend the 4-way branches in every repaint lambda, and
re-run `tools/generate_screenshots.py`.
