# Performance Optimizations

Applies from v2.1 onward; values below reflect the **current** firmware
(`common/display.yaml`, `common/fonts.yaml`).

## Problem (old version)

- Settings page laggy, scroll stutter
- Boot 60 s + 20 s HA timeout
- Fonts bpp 8 = RAM heavy
- Logger WARN + many components logging
- LVGL buffer 12%
- Dropdowns create overlay list every open

## Solutions Implemented

### 1. LVGL Buffer 12% → 20% → 50%

In `common/display.yaml`:
```yaml
lvgl_buffer_size: "50%"
lvgl_refresh_interval: "16ms"
```
Uses PSRAM (octal 80 MHz) but renders faster. Tradeoff: more PSRAM, less
internal heap — okay because we have 8 MB PSRAM.

### 2. Fonts bpp 8 → 4

All fonts render at bpp 4 (halves memory vs 8, anti-aliasing still fine at
480p). Current set in `common/fonts.yaml`:

- Nunito-SemiBold: 120 (screensaver-era large), 72 (AC target temp), 36 (steppers), 24 (main UI), 20 (settings/info), 18, 14, plus compat aliases
- NotoSansGeorgian 32 (Georgian date)
- DejaVu Sans Bold: 148 (screensaver clock), 96 (weather temp), 32 (Georgian date), 28, 24
- Material Design Icons: 40 (dashboard icons), 22 (AC/info icons), 80 (play/pause)

### 3. Logger ERROR Only

```yaml
logger:
  level: ERROR
  logs:
    lvgl: ERROR
    sensor: ERROR
    display: ERROR
```

No log spam during touch, saves CPU.

### 4. API Optimizations

```yaml
api:
  reboot_timeout: 0s   # HA restart must not reboot a healthy panel
  batch_delay: 50ms    # faster state push
```

### 5. ESP32 SDK Optimizations

```yaml
CONFIG_SPIRAM_FETCH_INSTRUCTIONS: y
CONFIG_SPIRAM_RODATA: y
CONFIG_SPIRAM_SPEED_80M: y
CONFIG_ESP32S3_DATA_CACHE_64KB: y
CONFIG_ESP32S3_DATA_CACHE_LINE_64B: y
CONFIG_ESP32S3_INSTRUCTION_CACHE_32KB: y
CONFIG_COMPILER_OPTIMIZATION_PERF: y
```

Executes from PSRAM, faster cache lines. Hardware file also sets
`compiler_optimization: PERF`, `execute_from_psram: true`,
`watchdog_timeout: 60s`.

### 6. Loading Screen 20s → 8s

Delay before the offline message dropped to 8 s, spinner sped up.
File: `pages/loading_480px.yaml`

### 7. Settings Rewrite — Biggest Win

**Before:** 3 dropdowns, scrollable container, grid layout, 421 lines
**After:** 0 dropdowns, 15 buttons (17 since v2.6 — Saver-lang GE/EN row),
fixed 460 px non-scrolling flex layout,
template selects (no LVGL widget), highlight via `update_settings_highlight`,
sliders 12 px / knobs 14×14, ~830 lines including 4-theme repaint logic
(see [Settings.md](Settings.md))

### 8. Info Page 10s → 30s

Free heap/PSRAM sensors update every 30 s, flex layout, alternating flat rows.

### 9. Screensaver Flex

Flex column/row, no absolute positioning except the clock label.

### 10. Base Theme: No Shadows

```yaml
shadow_width: 0
border_width: 0
scroll_on_focus: false
```

Every shadow is a draw call — glows/shadows exist only as opt-in styles for
Modern/Daylight tiles (`depth_dark`, `depth_light`, `glow_*`).

### 11. Assets Resized Explicitly

All LVGL images sized at load (RGB565, alpha channel where needed) — no
runtime scaling.

## Theme speed ranking

1. **Performance** — flat fills, radius 4, monochrome, zero style stacking
2. **Classic** — flat fills, radius 14
3. **Daylight / Modern** — gradient tiles + borders + shadows + glow rings
   (still smooth at 480×480 with the 50% buffer)

## Measured Improvements (v2.1 baseline)

- Boot to main page: ~60% faster
- Settings open: instant vs 300–500 ms lag
- Touch response: no dropped frames

## Further Ideas

- Reduce weather icons to 2 colors
- Disable buzzer if unused (save PWM)
- Profile Modern glow styles if a future device feels slow
