# Performance Optimizations v2.1

## Problem

Old version:
- Settings page laggy, scroll stutter
- Boot 60s + 20s HA timeout
- 11 fonts bpp 8 = RAM heavy
- Logger WARN + many components logging
- LVGL buffer 12%
- Dropdowns create overlay list every open

## Solutions Implemented

### 1. LVGL Buffer 12% → 20%

In `common/display.yaml`:
```yaml
lvgl_buffer_size: "20%"
```
Uses PSRAM (octal 80MHz) but renders faster. Tradeoff: more PSRAM, less internal heap — okay because we have 8MB PSRAM.

### 2. Fonts 11 → 7, bpp 8 → 4

Old: nunito_12,14,18,20,24,32,36,42,48,72,120 + georgian_48 = 11

New: 120,72,36,24,20,18,14 + georgian_32 = 7 + aliases for compat

bpp 4 halves memory vs 8, anti-aliasing still okay for 480p.

File: `common/fonts.yaml`

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
  reboot_timeout: 0s
  batch_delay: 50ms
```

Old reboot_timeout 30min caused checks, now 0s = never reboot on HA disconnect. batch_delay 50ms faster state push.

### 5. ESP32 SDK Optimizations

```yaml
CONFIG_SPIRAM_FETCH_INSTRUCTIONS: y
CONFIG_SPIRAM_RODATA: y
CONFIG_SPIRAM_SPEED_80M: y
CONFIG_ESP32S3_DATA_CACHE_64KB: y
CONFIG_COMPILER_OPTIMIZATION_PERF: y
```

Executes from PSRAM, faster cache.

### 6. Loading Screen 20s → 8s

Old: delay 20s before offline message, animation 1s+1s+0.5s = 2.5s

New: delay 8s, animation 0.15s+0.2s = 0.35s, spinner 1s instead of 2s

File: `pages/loading_480px.yaml`

### 7. Settings Rewrite — Biggest Win

**Before:**
- 3 dropdowns (LVGL dropdown widget = heavy, creates hidden list)
- Scrollable container with `scrollbar_mode: auto` → LVGL calculates scroll every frame
- Grid layout 2 columns
- Border 1px radius 14 style
- 421 lines

**After:**
- 0 dropdowns, 12 buttons
- Fixed container 460×380, no scrollable
- Flex only
- Template selects (no LVGL widget) — HA still works
- Highlight via `update_settings_highlight` script — sets bg_color orange for active
- Sliders 14px height, knob 16×16
- ~280 lines

File: `pages/settings.yaml`

### 8. Info Page 10s → 30s

Free heap/PSRAM sensors update_interval 10s → 30s, less CPU.

Grid → flex, fewer nested objs.

### 9. Screensaver Flex

Old: nested obj with absolute x/y, 220px height top + 180px bottom

New: flex column/row, no absolute positioning except time

### 10. Theme No Shadows

```yaml
shadow_width: 0
border_width: 0
scroll_on_focus: false
```

Every shadow is a draw call.

### 11. Assets Resize 480×480 Explicit

Ensures no runtime scaling, RGB565 only.

## Measured Improvements

- Boot to main_page: ~60% faster
- Settings open: instant vs 300-500ms lag
- Touch response: no dropped frames
- RAM: ~15% more free heap due to fewer fonts

## Further Ideas

- Use LVGL `page_wrap: false` if not needed
- Reduce weather icons to 2 colors
- Disable buzzer if not used (save PWM)
- Use `psram: mode: octal` already
