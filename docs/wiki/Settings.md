# Settings Page — Simplified for Speed

## Why Rewrite?

Old settings page was the main source of lag:

- Used LVGL dropdown widgets — each dropdown creates a hidden list object that is measured every frame
- Scrollable container with `scrollbar_mode: auto` — forces LVGL to compute scroll area
- Grid layouts — expensive
- Many nested objs with borders/shadows

New page: **0 dropdowns, no scroll, flex only, 15 buttons**

## UI

```
Title: Settings
Row 1: Mode    [ Day ] [ Eve ] [ Night ]        — active highlighted
Row 2: Day · 100%    [orange slider]     100%
Row 3: Eve · 50%     [orange slider]      50%
Row 4: Night · 35%   [orange slider]      35%
Row 5: Timeout · 30s [blue slider]  Saver [switch]
Row 6: Theme  [ Classic ] [ Modern ] [ Perf ] [ Day ]
Row 7: Rotate [ 0° ] [ 90° ] [ 180° ] [ 270° ]
Bottom: [ Home (orange) ]            [ Info (gray) ]
```

All rows repaint per theme via `apply_settings_theme` (called on every theme
switch by `apply_display_theme`).

## Implementation

### No Dropdowns

Instead of:

```yaml
- dropdown:
    id: settings_brightness_mode
    options: [Day, Evening, Night]
```

We use:

```yaml
- button:
    id: settings_btn_day
    on_click:
      - select.set:
          id: brightness_mode
          option: "Day"
```

### Template Selects

```yaml
select:
  - platform: template
    id: brightness_mode
    options: [Day, Evening, Night]
    restore_value: true
    optimistic: true
    on_value:
      - script.execute: apply_display_brightness
```

No LVGL widget binding, so no dropdown rendering. HA can still set it, and on_value triggers brightness.

Same for theme (`current_theme`: Classic / Modern / Performance / Daylight),
rotation (`display_rotation_select`: 0/90/180/270) and screensaver language
(`screensaver_language` in `pages/screensaver.yaml`: Georgian / English,
default Georgian — its `on_value` re-runs `time_update` + highlight).

### Highlight Script

`update_settings_highlight` (in `dashboards/home.yaml`):

```cpp
auto set_btn = [](lv_obj_t* btn, bool active, std::string theme) {
  // active: 0xFF9F1C (0xFF8C00 Modern, 0x444444 Performance) + glow on Modern
  // inactive: 0x3A4352 (0x2A3142 Modern, 0x1A1A1A Performance)
}
```

Called after every apply_* script, repaints all 3 mode buttons, 4 theme
buttons and 4 rotation buttons.

### Sliders

- Day/Eve/Night: 296×12, bg `0x2A303E`, indicator orange (`0xFF9F1C` Classic,
  `0xFF8C00` Modern, `0x666666` Performance, `0xE37220` Daylight), knob 14×14 white
- Timeout: 160×10, indicator blue `0x41BDF5` (orange on Daylight)
- Trigger `on_release`, not `on_value` — less HA traffic

### Screensaver Switch

- 40×20 switch next to a "Saver" button, bg selector gray, indicator green `0x4CAF50` when on

## Persistence

All numbers and selects have `restore_value: true` so they survive reboot. Stored in flash every 10min (preferences flash_write_interval 10min)

## Sunrise/Sunset

In `common/display_settings.yaml`:

```yaml
sun:
  on_sunset: Evening   # elevation -3.5°
  on_sunrise: Day
time:
  on_time: 00:00 → Night
```

## How to Customize

Add new setting:

1. Add row + button in `pages/settings.yaml`
2. Add select/number entity
3. Add script to apply it
4. Add highlight in `update_settings_highlight` (`dashboards/home.yaml`)

Example: add 45° rotation — add button and add "45" to `display_rotation_select` options.
