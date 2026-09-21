# AC Control Page

## Overview

File: `esphome-modular-lvgl-buttons/pages/ac_control.yaml`

Widget name: `ac_main` (instantiated in `dashboards/home.yaml`)

Climate entity: `${climate_entity}` default `climate.midea_ac`

Swipe right anywhere on the page returns to Home (part of the
Home ↔ AC ↔ Light swipe ring).

## UI Layout

```
Top bar:   [ < Back ]   Climate Control        47% Humidity
                                            Room 24.5°C
Center:    arc 16–31 °C (224×224, 135°→45°), big target temp
           24° + hvac_action (STANDBY/COOLING/…), − + steppers (62×62)
Row 1:     [ Power ] [ Mode ] [ Fan ] [ Swing ]
Row 2:     [ Eco ] [ Sleep ] [ Turbo ] [ Preset ]
```

Each state button is a 3-line tile: title (14 pt, dim), MDI icon (22 pt),
live state text (18 pt). One script — `ac_main_refresh` — owns **all**
styling, so theme switches and state changes never disagree.

## Features

### 1. Power

- Text sensor `hvac_mode` (attribute `hvac_mode`) is the source of truth:
  "off" = OFF, anything else = ON
- ON: `0x4CAF50` green (Classic/Daylight), `0x00E676` + green glow (Modern),
  `0x444444` (Performance)
- Service: `climate.toggle`

### 2. HVAC Mode

Attribute `hvac_mode`, icon follows mode (snowflake / fire / water / fan / fan-auto)

Colors (Classic / Modern):
- cool: `0x2196F3` / `0x29B6F6` + blue glow, black text on Modern
- heat: `0xFF9800` / `0xFF6D00` + orange glow
- dry: `0xFFEB3B` / `0xFFCA28`
- fan_only: `0x4CAF50` / `0x66BB6A`
- auto: `0x9C27B0` / `0x9C27B0`
- Performance: `0x444444` for every active state

Cycle: off → cool → heat → dry → fan_only → auto → off
Service: `climate.set_hvac_mode`

### 3. Fan Mode

Attribute `fan_mode`; label AUTO/LOW/MED/HIGH; high = orange fill (Classic
`0xFF9800`, Modern `0xFF8C00` + glow)

Cycle: auto → low → medium → high → auto
Service: `climate.set_fan_mode`

### 4. Swing Mode

Attribute `swing_mode` — states: off, vertical, horizontal, both
(labels OFF/VERT/HORIZ/BOTH). Blue `0x03A9F4` when active (blue glow on Modern).

Service: `climate.set_swing_mode`

### 5. Presets

Attribute `preset_mode`:

- Eco: `eco` / `none` — green when active (Classic)
- Sleep: `sleep` / `none` — purple when active (Classic), lavender text on Modern
- Turbo/Boost: `boost` / `none` — `0xFF5722` (Classic), `0xFF6D00` + orange glow (Modern)
- Preset tile always shows the current preset (NORMAL/ECO/SLEEP/BOOST) and cycles it on tap

Service: `climate.set_preset_mode`

### 6. Temperature

- Target: 16–31 °C, shown in a 224×224 arc (135°→45°, width 13, rounded)
  with the accent color of the theme (`0xFF9F1C` Classic, `0xFF8C00` Modern,
  `0x666666` Performance, `0xE37220` Daylight), knob white border
- Drag the arc, or tap the −/+ steppers (±1 °C); **long-press a stepper for
  0.5 °C fine steps**
- Current temperature + humidity from attributes → header right ("Room 24.5°C", "47% Humidity")
- Service: `climate.set_temperature`

### 7. hvac_action

Attribute `hvac_action` shown under the target temp: idle → STANDBY,
cooling → COOLING, etc., with a thermometer/mdi icon.

## Midea AC Specific

Midea AC via the Midea Smart integration typically supports:

- hvac_modes: off, cool, heat, dry, fan_only, auto
- fan_modes: auto, low, medium, high
- swing_modes: off, vertical, horizontal, both
- preset_modes: none, eco, sleep, boost

If your entity doesn't support swing, the button still calls the service but
HA will ignore it — safe.

## Customization

Override the climate entity per display:

```yaml
substitutions:
  climate_entity: "climate.living_room_ac"
```

Or change the range in the YAML: `min_value: 16`, `max_value: 31`.

## Performance

- All sensors `internal: true`
- One repaint script per state batch instead of per-widget updates
- Shadows/glows only on Modern/Daylight; Performance stays flat
