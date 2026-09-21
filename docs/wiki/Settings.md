# Settings Page — Simplified for Speed

## Why Rewrite?

Old settings page was the main source of lag:

- Used LVGL dropdown widgets — each dropdown creates a hidden list object that is measured every frame
- Scrollable container with `scrollbar_mode: auto` — forces LVGL to compute scroll area
- Grid layouts — expensive
- Many nested objs with borders/shadows

New page: **0 dropdowns, no scroll, flex only, 12 buttons**

## UI

```
Title: Settings
Row1: Mode [ Day ] [ Eve ] [ Night ]  — orange highlight active
Row2: Day · 100% + slider orange 430x14
Row3: Evening · 50% + slider
Row4: Night · 35% + slider
Row5: Timeout · 30s + slider blue + [ Saver switch ]
Row6: [ Dark ] [ Light ] + [ 0° ] [ 90° ] [ 180° ] [ 270° ]
Bottom: [ Home orange ] [ Info gray ]
```

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

Same for theme and rotation.

### Highlight Script

`update_settings_highlight` in `display_settings.yaml`:

```cpp
auto set_btn = [](lv_obj_t* btn, bool active) {
  if (active) bg 0xFF9F1C else 0x3A4352
}
```

Called after every apply_* script.

### Sliders

- Width 430, height 14
- bg 0x2A303E, indicator orange 0xFF9F1C or blue 0x41BDF5
- Knob white 16×16 radius 8 — minimal
- Trigger on_release, not on_value — less HA traffic

### Screensaver Switch

- 44×22, bg 0x3A4352, indicator green 0x4CAF50 when on

## Persistence

All numbers and selects have `restore_value: true` so survive reboot. Stored in flash every 10min (preferences flash_write_interval 10min)

## Sunrise/Sunset

In `display_settings.yaml`:

```yaml
sun:
  on_sunset: Evening
  on_sunrise: Day
time:
  on_time: 00:00 → Night
```

## How to Customize

Add new setting:

1. Add button in settings page
2. Add select/number entity
3. Add script to apply
4. Add highlight in `update_settings_highlight`

Example: add 45° rotation — add button and add "45" to select options.
