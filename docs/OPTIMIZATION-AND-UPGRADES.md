# OspreyPi 480×480 — Setup Audit, Optimisations & Upgrade Advice

*Review of the full v2.2 firmware tree after the AC / Info / WLED / Theme-2 UI pass.
Targets: `Display01.yaml`, `Display02.yaml` on ESP32-S3 (ST7701S 480×480, FT6336).*

---

## 1. What this UI pass changed

| # | Item | Result |
|---|------|--------|
| 1 | **AC page** redesigned to the repo mockups | Header rebuilt with absolute positioning (no more overflow/clipping), humidity + room temp on the right, big orange gauge with `24° / DEGREES / action`, −/+ steppers **beside** the gauge like `theme_modern_home.png` |
| 1b | **Real AC state on buttons** | 8 two-line buttons (title + icon + live value): Power `ON/OFF`, Mode `COOL/HEAT/…`, Fan `AUTO/LOW/MED/HIGH`, Swing `OFF/VERT/HORIZ/BOTH`, Eco `SAVING/OFF`, Sleep `ON/OFF`, Turbo `TURBO/OFF`, Preset `NORMAL/…` — all driven by HA attributes |
| 1c | Fixed latent AC bugs | Power state used `attribute: state` (not a real HA attribute → never updated); the Mode button updated the wrong label id; Eco/Sleep/Turbo/Preset values never refreshed; the preset chip was a dead `obj` (now a cycling button) |
| 2 | **Theme 2 (Modern) depth** | Raised buttons: vertical gradient face + 1px bevel border + drop shadow (`depth_dark`), colored glows for active fills (`glow_green/blue/orange`), soft halo on −/+ (`glow_soft`), orange ring-glow for active dashboard tiles (matches `screen_ac.png` mockup) |
| 3 | **Info page** redesigned to `screen_settings.png` | Alternating dark rows, device header, richer values (`-61dBm / 78%`, `160 MHz / 55.4°C`, heap/PSRAM with % used, build date), green `● Connected` HA status, Restart + Exit buttons |
| 4 | **WLED page** redesigned to `screen_home.png` | “Bed LEDs” title, labeled vertical sliders (orange Brightness, red Saturation) with live `%%` readouts, glowing bulb, rainbow **C-ring** (270°, gap on the left) with knob marker, HOME button |
| 5 | Validation | Both device configs pass `esphome config` on the pinned **ESPHome 2026.9.0** exactly as CI runs it |

---

## 2. Correctness findings (fixed or to watch)

### 2.1 Fixed in this pass
- **`climate` power state** — a `homeassistant` `binary_sensor` with `attribute: state` silently
  delivers nothing (`state` is not an attribute). Power is now derived from `hvac_mode == "off"`.
- **Mode button label id mismatch** — updates went to the small gauge caption instead of the
  button value (`mode_btn_label` vs `mode_label`).
- **`ac_main_preset_box`** was a passive `obj` with stale styling hooks; it is now
  `ac_main_preset_btn` and is included in the HA-connected enable/disable set (it used to stay
  disabled forever after a disconnect because it was missing from that list).
- **Entity-state skins flattened themed buttons** — `switch_or_light_button_state.yaml` (and the
  play/pause + script variants) wrote plain `bg_color`s on every HA update, which destroyed any
  themed face. They are now theme-aware (Modern ring-glow, Classic fill, Performance flat).

### 2.2 Watch list (not blocking)
- **`lvgl: refresh_interval` is version-sensitive.** ESPHome 2026.6.x renamed it to
  `update_interval`, 2026.9.x uses `refresh_interval` again and maps it to
  `set_refresh_interval()`. `update_interval` still *validates* on 2026.9.0 but does **not**
  drive the LVGL refresh — don't “clean it up”. The `min_version: 2026.9.0` pin is what keeps
  this consistent; keep it.
- **Mockup images are mislabeled** in `docs/images/`: `screen_ac.png` shows the Home grid,
  `screen_home.png` shows the light page, `screen_info.png` shows AC, `screen_light.png` and
  `screen_settings.png` show Info. Rename/re-export before the next design pass to avoid
  re-implementing the wrong screens.
- **OTA has no password** (`ota: platform: web_server` + `platform: esphome` are both open —
  see §4 Security).
- `climate.toggle` / preset names (`none/eco/sleep/boost`) are Midea-specific. A different
  integration may expose other preset names — the buttons fall back gracefully (NORMAL etc.)
  but the Eco/Sleep/Turbo toggles won't match.

---

## 3. Optimisation opportunities

### 3.1 Build size & RAM (biggest wins first)
1. **`mdi_glyph_substitutions.yaml` is ~7,450 lines of substitutions** re-parsed on *every*
   compile. Only ~40 glyphs are actually used. Trim it (or replace with a small
   `mdi_glyphs_used.yaml`) to cut YAML parse time and memory during builds dramatically.
2. **Fonts** — 12 font objects ship today (9× Nunito incl. the unused `nunito_32` alias,
   2× Georgian at *the same 32 px size*, 3× MDI). Each costs flash + heap:
   - delete `nunito_32` (unused alias),
   - merge `georgian_48`/`georgian_32` (both are size 32 today),
   - `mdi_icons_22` (new, 16 glyphs) and `mdi_icons_40/80` could share one size with
     `text_font` overrides if you need ~15 KB more flash.
3. **Dead files** — never loaded by Display01/02, safe to move to `example_code/` or delete:
   `common/theme.yaml`, `common/theme_debug.yaml`, `common/theme_style_debug.yaml`,
   `common/ha_control.yaml` (self-declared legacy), `common/time_sntp.yaml`,
   `common/backlignt_time.yaml` (also: filename typo), `buttons/color_picker.yaml`,
   `weather/weather_*.yaml`, `pages/weather_simple.yaml`, `sensors/sensors_base-SDL.yaml`
   (keep the SDL one if you use the PC simulator — it's useful).
   Unused images in `assets.yaml`: `screensaver_bg_image2`, `sync4` (screensaver only uses
   `screensaver_bg_image3`).
4. **LVGL draw buffer** is `20%` of the frame (~46 KB). On 8 MB PSRAM consider
   `buffer_size: 32%` (or a full 480-line buffer in PSRAM) for noticeably smoother arcs and
   the new shadows — Modern's drop shadows are fill-rate heavy; the Performance theme remains
   the escape hatch (no shadows, flat).

### 3.2 Runtime behaviour
- Info page heap/PSRAM sensors run every 30 s even when the page is hidden → 60 s is plenty.
- Uptime ticks at 1 Hz now (mockup shows seconds). If you want it cheaper, render seconds only
  while `info_screen` is the active page.
- `api: batch_delay: 50ms` + `reboot_timeout: 0s` is already the right shape for a panel that
  must survive HA restarts.
- Consider `esp32: restore_from_flash`… ESPHome already defaults sensibly; just avoid
  frequent `globals.set` writes (theme/brightness selects already use `restore_value: true`
  template selects — good).

### 3.3 Structure / maintainability
- **One styling entry point per page.** The AC page now funnels all paints through
  `ac_main_refresh` so theme switches and HA updates can't disagree. Apply the same pattern to
  the light page if it grows (its capability matrix already has 4 modes).
- The `depth_dark`/`glow_*` style helpers are duplicated in 4 lambdas (AC refresh, dashboard,
  settings, entity-state skins). If you touch them again, generate a tiny `ui_skin.h` and use
  `esphome: includes:` to share one C++ helper instead.
- `sensors_base-SDL.yaml` + `example_code/` suggest a PC simulator flow exists — worth
  resurrecting: LVGL UI mockup diffs against `docs/images/` would have caught the AC/header
  drift before it shipped.

---

## 4. Security & reliability upgrades

1. **Add OTA passwords** — currently any machine on the LAN can flash the panel:
   ```yaml
   ota:
     - platform: esphome
       password: !secret ota_password
     - platform: web_server   # consider removing this one entirely
   ```
   The dashboard `Restart` button and HA `factory_reset` remain convenient attack surface too —
   acceptable on a trusted VLAN, but add `entity_category: config` everywhere (already mostly
   done).
2. **`secrets(example).yaml` is committed** — fine (it's the template), but make sure
   `secrets.yaml` stays git-ignored (it is) and rotate the sample `api_encryption_key`
   comment so nobody deploys the example key.
3. **Watchdog** — the boot sync animation can block on a dead HA. An ESPHome
   `esp32:` task watchdog (or a `script` that falls back to `main_page` after N seconds —
   partially present as “Offline — auto retry”) should also `lvgl.resume` so a paused UI can't
   wedge after OTA abort.
4. **CI upgrade**: the workflow runs `esphome config` only — that catches YAML/schema drift
   (it would *not* have caught the AC label-id bug). Add a nightly/`workflow_dispatch` job with
   `esphome compile Display01.yaml` so lambda/LVGL API breaks (like a future
   `shadow_ofs` → `shadow_offset` rename) fail loudly. Cache PlatformIO between runs to keep
   it under ~5 min.
5. **API encryption** is already enforced per device (`api_encryption_key`/`2`) — good; keep
   Display02 on its own key (it is).

---

## 5. Product/feature upgrade ideas (ranked by value/effort)

| Idea | Value | Effort | Notes |
|------|-------|--------|-------|
| Long-press AC `−/+` for 0.5° steps | High | Low | `climate.set_temperature` with ±0.5; Midea supports it |
| Swipe between Home ↔ AC ↔ Light | High | Low | `widgets/swipe_navigation.yaml` already exists — extend its page list |
| Weather strip on Home header | Medium | Low | `weather/weather_today.yaml` logic exists but is unused |
| Scene/Quick-info overlay on long-press tiles | Medium | Med | The Settings tile already does “Tap · hold for info” — copy the pattern |
| Per-page theme previews in Settings | Low | Med | Nice, but the three galleries in the README cover it |
| Battery/voltage tile (if OspreyPi exposes ADC) | Low | Med | Check `DEVICE_SPECS.md` before promising UI space |
| Adaptive brightness from an ALS sensor | High | Med | Settings already has Day/Evening/Night — an ALS would close the loop |
| `improv_serial` / `esp32_improv` for first-run Wi-Fi | Medium | Low | Nicer than the fallback AP QR alone (keep both) |

---

## 6. Quick reference — where things live now

| Concern | File |
|---------|------|
| AC layout + state logic | `esphome-modular-lvgl-buttons/pages/ac_control.yaml` (`ac_main_refresh` is the styling entry point) |
| Theme definitions + Modern depth styles | `esphome-modular-lvgl-buttons/common/themes.yaml` (`depth_dark`, `glow_*`) |
| Theme application (dashboard/settings/AC) | `esphome-modular-lvgl-buttons/dashboards/home.yaml` (`apply_display_theme`, `update_settings_highlight`, `apply_dashboard_theme`) |
| Entity-state skins | `esphome-modular-lvgl-buttons/sensors/*_state.yaml` |
| Info page | `esphome-modular-lvgl-buttons/pages/info.yaml` |
| WLED / light page | `esphome-modular-lvgl-buttons/pages/light_color.yaml` |
| Compact icon font (AC/info) | `esphome-modular-lvgl-buttons/common/assets.yaml` (`mdi_icons_22`) |
| Validation | `esphome config Display01.yaml && esphome config Display02.yaml` (ESPHome 2026.9.0) |
