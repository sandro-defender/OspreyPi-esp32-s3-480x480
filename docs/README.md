# Documentation

## Images

All UI mockups in `images/` are rendered at **true 480×480 device resolution**
from the palettes and layout coordinates in the firmware YAML, using the real
bundled fonts (Nunito, DejaVu Bold, Noto Georgian, Material Design Icons) and
real assets (weather/connection icons, screensaver background, lightbulb).
Regenerate after any UI change with:

```bash
pip install pillow
python3 tools/generate_screenshots.py
```

### Theme galleries (v2.3 — 4 selectable themes)

Per theme: `<theme>_home.png`, `<theme>_ac.png`, `<theme>_settings.png` for

- **Classic** — `theme_classic_*.png` — original flat dark, slate tiles, orange active
- **Modern** — `theme_modern_*.png` — mockup look: navy, raised gradient tiles, orange glow, green/blue AC
- **Performance** — `theme_performance_*.png` — minimal monochrome, fastest
- **Daylight** — `theme_daylight_*.png` — warm raised dark cards, orange accents/glows

`theme_preview_sheet.png` — all four home screens in one 2×2 sheet (1008×1008).

### General screens (480×480)

- `screen_ac.png` — AC climate page (Modern)
- `screen_light.png` — WLED / Bed LEDs light page (brightness + saturation sliders, 12-segment hue ring)
- `screen_settings.png` — settings page (Modern)
- `screen_info.png` — device info / diagnostics page
- `screen_screensaver.png` — screensaver clock + Georgian date + weather

### Hi-res home previews (960×960)

- `preview_classic_v2_home.png`
- `preview_modern_v2_home.png`
- `preview_performance_v2_home.png`
- `preview_daylight_home.png`

## Wiki

See `wiki/` folder:

- Home.md — overview (v2.3)
- Themes.md — all 4 themes detailed (Classic / Modern / Performance / Daylight)
- Installation.md
- Performance.md
- AC-Control.md
- Settings.md
- Hardware.md
- Custom-Dashboard.md
- Troubleshooting.md

Wiki linked from main README.md.

## Hardware Photos

`../hardware/img/` — official vendor images (hi-res PCB callouts, MCU + RS485
schematic excerpts, product render) + 6 user-guide screenshots with captions in
the README gallery (PCB callouts, component table, product page, 3× schematic
sheets). Full schematic: `../hardware/SCH_Esp32s3_3.95in_RS485_R2_2025-02-05.pdf`;
per-pin map: `../hardware/PINOUT.md`; folder index: `../hardware/README.md`
(datasheets + official vendor repo links).

## For AI agents

`../AGENTS.md` is the operating manual for AI editors: architecture, file map,
validation commands, screenshot regeneration and the version-bump policy.
