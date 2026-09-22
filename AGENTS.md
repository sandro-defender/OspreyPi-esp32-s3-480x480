# AGENTS.md — OspreyPi ESP32-S3 480×480 Smart Display

> **This file is the operating manual for AI coding agents (and humans) working
> on this repository.** Read it fully before making changes. It mirrors the
> real state of the code — if the code and this file disagree, fix both in the
> same commit.

---

## 1. What this project is

An ESPHome + LVGL 9 smart-display dashboard for Home Assistant, targeting the
**OspreyPi / osptek ESP32-S3 480×480** panel:

- **MCU**: ESP32-S3, 16 MB flash (custom partition table `partitions_16mb.csv`), 8 MB octal PSRAM @ 80 MHz
- **Display**: 3.95" IPS 480×480, ST7701S driver (3-wire SPI init + 16-bit RGB bus)
- **Touch**: FT6336 I²C
- **Firmware**: ESPHome **2026.9.0** (`min_version: 2026.9.0`), esp-idf framework, LVGL 9.5 integration
- **UI**: modular — one shared firmware, per-device YAML files, 4 selectable
  themes (Classic / Modern / Performance / Daylight), swipe navigation,
  screensaver, OTA with boot screen

Two devices ship from this repo: `Display01.yaml` and `Display02.yaml`
(02 is the same firmware, different name/API key/rotation).

---

## 2. Repository map

```text
Display01.yaml / Display02.yaml     # per-device identity ONLY (name, rotation, api key, dashboard)
partitions_16mb.csv                 # 16MB flash partition table
secrets(example).yaml               # template for secrets.yaml (never commit real secrets)
DEVICE_SPECS.md                     # full pinout + ST7701S init sequence + specs
README.md                           # main project page (keep in sync with version/themes)
AGENTS.md                           # ← you are here
tools/generate_screenshots.py       # regenerates every mockup in docs/images (Pillow)
docs/images/                        # 480×480 UI mockups (theme_*_*.png, screen_*.png, preview_*.png)
docs/wiki/                          # GitHub-wiki-style docs (Home, Themes, Installation, …)
docs/OPTIMIZATION-AND-UPGRADES.md   # history of the performance work
hardware/                           # datasheets (FT6336, ESP32-S3) + device photos
esphome-modular-lvgl-buttons/       # the shared firmware package tree
├── common/
│   ├── display.yaml                # ★ FIRMWARE ENTRY POINT: substitutions + package list
│   ├── display_core.yaml           # lvgl buffer/refresh/rotation
│   ├── display_settings.yaml       # brightness/rotation scripts, sun + time automation
│   ├── themes.yaml                 # theme REGISTRY (one package per theme below)
│   ├── themes/{classic,modern,performance,daylight}.yaml   # ★ theme palettes + LVGL styles
│   ├── theme_style.yaml            # base LVGL theme (flat, fast, no shadows)
│   ├── fonts.yaml                  # Nunito set, DejaVu Bold set, Georgian, MDI icon sets
│   ├── mdi_glyph_substitutions.yaml# every MDI icon name → codepoint (single source of truth)
│   ├── color.yaml                  # named colors (ep_orange F37320, misty_blue 9BA2BC, …)
│   ├── assets.yaml                 # LVGL images (weather, connection icons, screensaver bg)
│   ├── wifi.yaml, ota.yaml, home_assistant.yaml, ha_control.yaml
│   ├── weather_icons.yaml, time_homeassistant.yaml, time_sntp.yaml
│   └── backlignt_time.yaml         # (sic) screen timeout / backlight logic
├── dashboards/home.yaml            # ★ default dashboard: 10 cards + ALL theme repaint scripts
├── pages/
│   ├── ac_control.yaml             # AC/climate page (arc gauge, 8 state buttons, −/+ steppers)
│   ├── light_color.yaml            # WLED/Bed-LEDs page (vertical sliders + 12-segment hue ring)
│   ├── settings.yaml               # settings page + apply_settings_theme
│   ├── info.yaml                   # diagnostics page + apply_info_theme
│   ├── screensaver.yaml            # clock + GE/EN date + weather + saver-language select
│   ├── loading_480px.yaml          # boot/loading top layer
│   └── weather_simple.yaml         # optional simple weather page
├── buttons/                        # reusable LVGL button widgets (entity, dimmer, scene, …)
├── sensors/                        # per-button HA state listeners → repaint_* scripts
├── widgets/swipe_navigation.yaml   # swipe mixin for pages
├── hardware/osptek-esp32-s3-48x48.yaml  # board config (esp32, psram, display, touch, buzzer)
├── custom_components/noaa_tides/   # external component
├── homeassistant_config/           # helper YAML for the HA side
├── example_code/                   # minimal device example
└── assets/                         # fonts, images, weather icons, backgrounds
.github/workflows/esphome-validate.yml  # CI: validate both displays + auto-release on version bump
```

---

## 3. How the firmware is wired together

```
DisplayXX.yaml (device identity)
  └─ packages: common/display.yaml
                dashboards/home.yaml   (or a custom dashboard)
                common/lvgl_boot.yaml
                     │
common/display.yaml ── includes ──► wifi, home_assistant, ota_screen, colors, fonts,
                                    glyphs, weather_icons, sensors_base, theme_style,
                                    themes.yaml (all 4 themes), display_core,
                                    hardware/osptek board, assets, loading, info,
                                    screensaver, settings, display_settings
dashboards/home.yaml ── includes ──► pages/ac_control.yaml (widget ac_main),
                                    pages/light_color.yaml (widget button_7),
                                    sensors/*_button_state.yaml per card,
                                    buttons/*.yaml per card
```

**Rules that keep this valid:**

1. Device files stay tiny — only `substitutions` (identity/rotation) + `packages` + `api` key.
2. Anything shared goes in `common/` and is added to `common/display.yaml`'s package list.
3. LVGL page/widget IDs referenced across files must exist before
   `dashboards/home.yaml`'s `apply_display_theme` script runs — that is why
   theme scripts live at the END of home.yaml ("defined AFTER all pages so all
   ids exist").

### The theme system (important!)

- Palettes + LVGL styles live one-per-file in `common/themes/*.yaml`, registered
  in `common/themes.yaml`. Adding a theme = drop a file + register it.
- Runtime switching: `select` entity `current_theme` (options: Classic, Modern,
  Performance, Daylight) in `pages/settings.yaml`, persisted via `restore_value`.
- `apply_display_theme` (bottom of `dashboards/home.yaml`) recolors pages, then
  calls, in order: `ac_main_refresh`, `apply_settings_theme`, `apply_info_theme`,
  `button_7_apply_theme`, `update_settings_highlight`, `apply_dashboard_theme`,
  and every `repaint_button_N` (so on/off skins survive theme switches).
- Style IDs `depth_dark`, `depth_light`, `glow_green`, `glow_blue`, `glow_orange`,
  `glow_soft`, `glow_blue_light` are referenced by name from repaint lambdas
  everywhere — **do not rename them**.
- HA entity: `select.<device>_theme`.

### HA interplay

- Every dashboard card both triggers an HA action AND listens to its entity
  state (via `sensors/*.yaml`) so the skin reflects the real world.
- `ha_connected` gates button actions (ignored while offline).
- Require the user to enable **"Allow the device to perform Home Assistant actions"**.

---

## 4. Build, validate, run

```bash
# one-time
cp 'secrets(example).yaml' secrets.yaml   # then edit wifi/keys/lat/lon

# validate (CI does exactly this, in the esphome/esphome:2026.9.0 container)
esphome config Display01.yaml
esphome config Display02.yaml

# flash (USB first time; OTA afterwards)
esphome run Display01.yaml

# logs
esphome logs Display01.yaml
```

CI (`.github/workflows/esphome-validate.yml`):
- on every push/PR touching `**.yaml` → validates both devices
- on push to `main` after validation → reads `project_version` from
  `common/display.yaml` and publishes a GitHub release + tag **if the version
  changed** (this is why the version must be bumped — see §7).

---

## 5. Regenerating the screenshot mockups

All images in `docs/images/` are rendered programmatically at true 480×480
device resolution from the palettes/layout coordinates in the YAML, using the
bundled fonts (Nunito, DejaVu Bold, Noto Georgian, Material Design Icons) and
real assets (weather/connection icons, screensaver bg, lightbulb).

```bash
pip install pillow
python3 tools/generate_screenshots.py           # rewrites everything in docs/images
python3 tools/generate_screenshots.py some/dir  # or a custom output dir
```

**When you change any theme palette, page layout, or dashboard card, re-run
this script and commit the updated PNGs** so the docs never drift from the UI.
Add new screens to the script's `main()` and reference them from the docs.
Pixel-verify expectations when editing (corner background colors, active-tile
fills, arc accent) — the script mirrors `THEMES` in
`tools/generate_screenshots.py`; if you change a color in `common/themes/*.yaml`,
mirror it there too.

---

## 6. Documentation map (keep in sync!)

| File | Must reflect |
|---|---|
| `README.md` | version, theme count/table, galleries, project layout, AC controls, settings table |
| `AGENTS.md` | this file — architecture truth |
| `docs/README.md` | inventory of docs/images files + wiki list |
| `docs/wiki/Home.md` | version + feature list + page links |
| `docs/wiki/Themes.md` | exact palettes of all 4 themes |
| `docs/wiki/Settings.md`, `AC-Control.md`, `Performance.md`, `Installation.md`, `Hardware.md`, `Custom-Dashboard.md`, `Troubleshooting.md`, `_Sidebar.md` | their page's real behavior |
| `DEVICE_SPECS.md` | pinout/init sequence (hardware rarely changes) |

After any firmware change, grep the docs for stale version numbers or theme
counts (e.g. `grep -rn "2\.2\|3 themes\|Three" README.md docs/`).

---

## 7. 📌 VERSION POLICY — bump on every push / PR merge

> **PROMPT (execute on every push to `main` and on every pull-request merge,
> before anything else):**
>
> 1. Read `project_version` in `esphome-modular-lvgl-buttons/common/display.yaml`.
> 2. Decide the new version:
>    - **patch** (2.3 → 2.3.1): typo/comment fixes, docs-only tweaks
>    - **minor** (2.3 → 2.4): new feature, new theme, new page, behavior change,
>      dependency/ESPHome version bump
>    - **major** (2.x → 3.0): breaking config changes (users must edit their
>      device YAML or secrets)
> 3. Update `project_version` in `esphome-modular-lvgl-buttons/common/display.yaml`
>    (it is the single source of truth — CI tags/releases from it).
> 4. Update every place that displays the version:
>    - `README.md` (title line "vX.Y …", "What's New", Releases section)
>    - `docs/wiki/Home.md` ("Current: **X.Y**")
>    - `tools/generate_screenshots.py` info-screen render if it hardcodes the version
> 5. Summarize what changed since the previous tag in the release notes
>    (CI uses `--generate-notes`, but the PR description should read well).
> 6. Never downgrade a published version; never reuse a tag. Check
>    `gh release list` if unsure what is published.
> 7. If the change also alters UI appearance, re-run
>    `python3 tools/generate_screenshots.py` and commit the refreshed PNGs
>    in the same push.

Consequences of skipping the bump: CI's release job sees the version already
published and silently skips the release — users never get the new firmware tag.

---

## 8. Cookbook — common changes

### Add / change a dashboard card
Override in the device YAML or edit `dashboards/home.yaml` substitutions:
`dashboard_button_<n>_{text,entity,action,icon,height}`. Button 4 also has
`dashboard_button_4_state_entity` (action is a script, state comes from a light).
Add a matching `sensors/switch_or_light_button_state.yaml` package for state
feedback if you add a new card. Re-run the screenshot generator.

### Add a new theme
1. Copy `common/themes/classic.yaml` → `common/themes/<name>.yaml`, edit palette
   + styles (keep style-id naming: `theme_<name>_*`).
2. Register it in `common/themes.yaml`.
3. Add the option to the `current_theme` select in `pages/settings.yaml` and a
   selector button in the Theme row.
4. Extend the 4-way branches (`Classic/Modern/Performance/Daylight`) in:
   `apply_display_theme`, `apply_dashboard_theme`, `update_settings_highlight`
   (dashboards/home.yaml), `ac_main_refresh` (pages/ac_control.yaml),
   `apply_settings_theme` (pages/settings.yaml), `apply_info_theme`
   (pages/info.yaml), `button_7_apply_theme` (pages/light_color.yaml), and the
   `repaint_*` skins in `sensors/*.yaml`.
5. Add the palette to `THEMES` in `tools/generate_screenshots.py`, render
   `theme_<name>_{home,ac,settings}.png`, add gallery tables to README +
   Themes wiki.

### Add a new page
Create `pages/<name>.yaml` with `lvgl.pages: - id: <name>_page`, include it
from `common/display.yaml` (or a dashboard), and navigate with
`lvgl.page.show`. Add swipe via `widgets/swipe_navigation.yaml`.

### Add an MDI icon
Find/append the codepoint in `common/mdi_glyph_substitutions.yaml`, add the
glyph to the right icon font in `common/fonts.yaml` and/or `common/assets.yaml`.

---

## 9. Gotchas / house rules

- **Secrets never get committed.** `secrets.yaml` is git-ignored; only the
  example file is committed. CI writes its own throwaway secrets.
- **Keep LVGL cheap**: no shadows on base styles, bpp 4 fonts, `log_level: ERROR`,
  no dropdown widgets, fixed-size (non-scrolling) pages.
- Style IDs and page IDs are cross-referenced from C++ lambdas — rename with care.
- `theme_index` / `brightness_mode_index` substitutions document option order —
  keep the comments accurate (0 Classic, 1 Modern, 2 Performance, 3 Daylight).
- ESPHome version is pinned in CI (2026.9.0) and `min_version` — bump both together.
- Screenshots are committed (not generated in CI) so the repo stays usable
  offline; regenerate them locally with the tool.
- Fix typos in existing filenames only with redirects/links updated everywhere
  (e.g. `backlignt_time.yaml` is misspelled but load-bearing).

## 10. Quick facts for agents

- Current version: **2.5** (see `common/display.yaml` → `project_version`)
- Performance knobs carry `#options:` comments (stable vs fast values) — see
  `docs/CHANGELOG-v2.5-PERFORMANCE.md`
- Themes: **4** — Classic, Modern, Performance, Daylight
- Pages: home dashboard, AC, light/WLED, settings, info, screensaver,
  loading (top layer), optional weather_simple
- Dashboard cards: Bedroom (tall), Fan, Pantry, WLED, AC, play/pause,
  Sleep, Bed LEDs (tall dimmer), Settings (with HA status halo), Leave
- Swipe ring: **Home ↔ AC ↔ Light** (swipe left/right, 300 ms)
- Default HA entities: `weather.openweathermap`, `climate.midea_ac`
- Timezone default: `Asia/Tbilisi`; screensaver date language is selectable
  (Georgian default, English optional) via `screensaver_language` select —
  Settings “Saver lang” row + HA entity, persistent
