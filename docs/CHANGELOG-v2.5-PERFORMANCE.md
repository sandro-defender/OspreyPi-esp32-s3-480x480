# v2.5 — Performance & Response Changelog

**Date:** 2026-09-22 · **Version:** 2.4 → 2.5 · **Scope:** `esphome-modular-lvgl-buttons/` shared firmware (applies to `Display01` and `Display02`)

Every tuning point in the YAML now carries a `#options:` comment marking the
**stable** value (what shipped in v2.1–v2.3) and the **fast** value applied in
v2.5 (or a commented alternative to enable and test on the device). Grep for
`#options:` to find them all:

```bash
grep -rn "#options:" esphome-modular-lvgl-buttons/
```

Validation: both `Display01.yaml` and `Display02.yaml` pass `esphome config`
(scratch-validated against ESPHome 2026.6.5 — the newest build that runs in this
sandbox — after neutralizing only the three documented 2026.6↔2026.9 schema
differences in the scratch copy: the `min_version` pin, the `lvgl:
refresh_interval` key name, and the `image: platform: file` key. CI still
validates on 2026.9.0 and the repo files use 2026.9 syntax).

---

## 1. Applied changes (active immediately after flashing)

### 1.1 Touch response

| What | File | Change | Why |
|---|---|---|---|
| Touch polling interval | `hardware/osptek-esp32-s3-48x48.yaml` → `touchscreen:` | **added `update_interval: 10ms`** (was: 50 ms ESPHome default) | The FT6336 IRQ pin is **not connected** on this board (see DEVICE_SPECS), so touch is polled. 10 ms polling registers taps/swipes up to **5× sooner**; one register read costs <1 ms at 400 kHz I²C. `#options: stable: 50ms \| fast: 10ms (applied)` |
| Dropped quick taps | `pages/light_color.yaml` → `${widget_name}_light_btn_control` `on_click` | **`min_length: 50ms` → `10ms`** | Taps shorter than 50 ms (a light flick is often 30–60 ms) were silently **ignored** and felt like a dead device. The 800 ms long-press threshold still separates cleanly. `#options: stable: 50ms (drops quick taps) \| fast: 10ms (applied)` |
| Redundant wake calls | `dashboards/home.yaml` → bottom `touchscreen: on_touch:` | **`wake_display` gated** to `lvgl.is_paused` **or** `lvgl.page.is_showing: screensaver_page` | Previously `wake_display` (a `mode: restart` script doing a full `light.turn_on` brightness service call) restarted on **every touch report**, even while the panel was awake and a finger was held down. Wake behavior when actually asleep/screensaving is unchanged. `#options: stable: wake on every touch \| fast: gated wake (applied)` |
| Homescreen status halo dead zone | `dashboards/home.yaml` → Settings card widgets | **`clickable: false` on `dashboard_status_halo` and `dashboard_connection_status`** | The 68 px halo disc + status icon in the middle of the Settings card were clickable, so taps (and swipe starts) landing on them never reached the button — a dead zone that felt like the screen ignoring input. Touches now pass through: tap = Settings, long-press = Info. |

### 1.2 Navigation feel

| What | File | Change | Why |
|---|---|---|---|
| Page slide animation ×4 | `dashboards/home.yaml` (Home→AC, Home→Light), `pages/ac_control.yaml` (AC→Home), `pages/light_color.yaml` (Light→Home), plus `widgets/swipe_navigation.yaml` mixin kept consistent | **`time: 300ms` → `150ms`** | The swipe ring feels ~2× more instant; the eye barely reads animation detail past 150 ms. `#options: stable: 300ms \| fast: 150ms (applied)` |

### 1.3 CPU / rendering

| What | File | Change | Why |
|---|---|---|---|
| Light-page glow halo | `pages/light_color.yaml` → script `${widget_name}_update_lightbulb_color` | **shadow width `34` → `16`** in the live-halo lambda | The halo is re-rendered on **every slider drag tick**; a 34 px blurred shadow around the bulb forces a large expensive repaint per tick. 16 px ≈ half the redraw cost, glow stays visible (visually: tighter halo — flip back via the `#options:` comment if you prefer the wide look). `#options: stable: 34 (wide halo) \| fast: 16 (applied)` |
| Info page 1 s timer | `pages/info.yaml` → `interval:` | **gated to `lvgl.page.is_showing: info_screen`** | `update_uptime` used to run every second forever, even with the Info page hidden for days. Now the timer body is a no-op unless the page is visible. Display precision unchanged. `#options: stable: 1s ungated \| fast: 1s only while info page showing (applied)` |
| Unused fonts removed | `common/fonts.yaml` | **deleted `nunito_120`, `nunito_32`, `georgian_48`, `georgian_32`** | Verified **zero references** across the whole tree (Georgian text renders via `bold_geo_32` on the screensaver; `nunito_12`/`nunito_18` remain in use). Cuts roughly ~400 KB of compiled font rodata → smaller firmware, **faster OTA upload**, less PSRAM rodata pressure. |

### 1.4 Network / boot latency

| What | File | Change | Why |
|---|---|---|---|
| WiFi connect time | `common/wifi.yaml` | **`fast_connect: false` → `true`** | With one known AP, boot associates in ~1–2 s instead of ~5–8 s (skips the full channel scan). Trade-off: no roaming; the commented backup-network block cannot be used while `true`. Revert if you add a 2nd AP. `#options: stable: false (scan) \| fast: true (applied, single AP)` |
| API state latency | `common/display.yaml` → `api:` | **`batch_delay: 50ms` → `20ms`** | Button press → HA action → echoed state repaint round-trips sooner (ESPHome default is 100 ms; v2.1–v2.3 shipped 50 ms). Packet overhead still negligible. `#options: stable: 50ms \| fast: 20ms (applied)` |
| UART logging off | `common/display.yaml` → `logger:` | **enabled `baud_rate: 0`** (was commented out) | Frees the log task even though level was already ERROR. ⚠️ Do **not** re-enable if the experimental RS485 Modbus on UART0 (pins 43/44) is ever used. `#options: stable: UART logging \| fast: baud_rate 0 (applied)` |

---

## 2. Test-on-device options (kept commented, current value marked stable)

These are one-line flips guarded by `#options:` comments. Enable **one at a
time**, flash via OTA, and keep only what is stable on your panel.

| Knob | File (block) | Stable (active) | Fast option (commented) | If it misbehaves |
|---|---|---|---|---|
| PSRAM clock | `hardware/osptek-esp32-s3-48x48.yaml` → `psram:` + `common/display.yaml` → sdkconfig | `speed: 80MHz` / `CONFIG_SPIRAM_SPEED_80M` | `120MHz` / `CONFIG_SPIRAM_SPEED_120M` | boot loop / artifacts → revert; **keep both files in sync** |
| Pixel clock | `hardware/osptek-esp32-s3-48x48.yaml` → `display: pclk_frequency` | `16MHz` (~60.4 fps, zero headroom at 480×480) | `20MHz` (~75 fps headroom) | vertical scan lines/flicker → revert |
| LVGL draw buffer | `common/display.yaml` → `lvgl_buffer_size` substitution | `50%` | `100%` (single flush per frame, ~450 KB more PSRAM) | internal heap too low on Info page → revert |
| Code/rodata XIP from PSRAM | `common/display.yaml` → `CONFIG_SPIRAM_FETCH_INSTRUCTIONS` / `CONFIG_SPIRAM_RODATA` **and** hardware file `execute_from_psram` | `"y"/"y"` + `true` (fast OTA, boot) | `"n"/"n"` + `false` (frees PSRAM bus during RGB DMA) | — flip the **whole group together** only if Modern/Daylight animations stutter; OTA-page behavior is the reason it shipped enabled |

These four trade bus bandwidth (PSRAM/pclk), RAM (buffer) and bus contention
(XIP) against each other — test individually, e.g. XIP-off + PSRAM-120 may beat
either alone.

---

## 3. Audited and intentionally NOT changed

| Item | File | Reason |
|---|---|---|
| `includes: <sstream>` / `<algorithm>` | `common/display.yaml` | Zero runtime cost (system headers, nothing in the binary); `<algorithm>` is what makes the `std::clamp` lambda in `display_settings.yaml` compile. A comment now documents why they stay. |
| `logger: level: ERROR` + per-component ERROR | `common/display.yaml` | Already optimal since v2.1. |
| `api: reboot_timeout: 0s` | `common/display.yaml` | Correct (HA restart must not reboot the panel). |
| `wifi: power_save_mode: none` | `common/wifi.yaml` | Correct for latency (modem power-save adds 100s of ms wake delay). |
| `esp32: cpu_frequency: 240MHz`, 64 KB data cache / 32 KB instruction cache, `CONFIG_FREERTOS_HZ: 1000`, `COMPILER_OPTIMIZATION_PERF` | hardware + display yaml | Already at maximum sensible values. |
| `preferences: flash_write_interval: 10min` | hardware yaml | Prevents NVS flash churn (would stall the CPU on frequent writes). |
| `display: update_interval: never` + LVGL-driven redraw | hardware yaml | Correct for RGB + LVGL 9 (continuous mode). |
| Brightness sliders `trigger: on_release` | `pages/settings.yaml` | Already prevents HA write floods while dragging. |
| Boot screen delay 8 s | `pages/loading_480px.yaml` | Already reduced in v2.1 (was 20 s). |
| Theme shadow/glow styles (Modern/Daylight) | `common/themes/*.yaml` | Left untouched — they define the themes' look. If a specific theme feels slow, use **Settings → Theme → Perf** (Performance theme is flat, zero shadows, fastest) before trimming glow styles. |

---

## 4. Expected impact (perceived, on device)

- Tap → reaction: **up to ~50 ms sooner** (polling) + no more swallowed taps on
  the Light page.
- Swipe navigation: transition cut 300 ms → 150 ms and no more redundant
  brightness calls mid-gesture.
- Boot to connected: **several seconds faster** (`fast_connect`, no UART task).
- HA round-trip echo: ~30 ms sooner (batch_delay 50→20 ms) + sooner state pushes.
- Slider drags on the Light page: fewer dropped frames (smaller halo repaint).
- OTA updates: ~7 % faster + slightly shorter boot decode (4 fonts removed).

---

## 5. Files touched

```
esphome-modular-lvgl-buttons/common/display.yaml          # version 2.5, api batch_delay, baud_rate 0, sdkconfig #options, buffer #options, includes note
esphome-modular-lvgl-buttons/common/wifi.yaml             # fast_connect: true
esphome-modular-lvgl-buttons/common/fonts.yaml            # removed 4 unused fonts, header updated
esphome-modular-lvgl-buttons/hardware/osptek-esp32-s3-48x48.yaml  # touch 10ms, PSRAM/PCLK/execute_from_psram #options
esphome-modular-lvgl-buttons/dashboards/home.yaml         # 150ms transitions, gated touchscreen on_touch wake
esphome-modular-lvgl-buttons/pages/ac_control.yaml        # 150ms transition
esphome-modular-lvgl-buttons/pages/light_color.yaml       # 150ms transition, min_length 10ms, halo 34->16
esphome-modular-lvgl-buttons/pages/info.yaml              # 1s uptime tick gated to info page
esphome-modular-lvgl-buttons/widgets/swipe_navigation.yaml# 150ms (mixin, kept consistent)
README.md, docs/wiki/Home.md, AGENTS.md                   # version 2.5 mentions
```
