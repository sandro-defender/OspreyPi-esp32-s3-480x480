# AC Control Page — Expanded

## Overview

File: `esphome-modular-lvgl-buttons/pages/ac_control.yaml`

Widget name: `ac_main` (instantiated in `dashboards/home.yaml`)

Climate entity: `${climate_entity}` default `climate.midea_ac`

## UI Layout

```
Top bar: [ < Back ] [ Climate Control + action ] [ humidity ]
Center: Arc 16-31°C, big 24, current 24.0°C + mode, - + buttons
Row1 bottom: [ Power ] [ Mode ] [ Fan ] [ Swing ]
Row2 bottom: [ Eco ] [ Sleep ] [ Turbo ] [ Preset NORMAL ]
```

## Features

### 1. Power

- Binary sensor `power_state` from climate state
- Green when on, dark gray off
- Service: `climate.toggle`

### 2. HVAC Mode

Text sensor `hvac_mode` attribute `hvac_mode`

Colors:
- cool: blue 0x2196F3
- heat: orange 0xFF9800
- dry: yellow 0xFFEB3B
- fan_only: green 0x4CAF50
- auto: purple 0x9C27B0
- off: gray 0x555555

Cycle: off → cool → heat → dry → fan_only → auto → off

Service: `climate.set_hvac_mode`

### 3. Fan Mode

Attribute `fan_mode`

Cycle: auto → low → medium → high → auto

Service: `climate.set_fan_mode`

### 4. Swing Mode — NEW

Attribute `swing_mode`

States: off, vertical, horizontal, both

Cycle: off → vertical → horizontal → both → off

Blue when active, gray off

Service: `climate.set_swing_mode`

### 5. Presets — NEW

Attribute `preset_mode`

- Eco: green when active, `eco` / `none`
- Sleep: purple, `sleep` / `none`
- Turbo/Boost: deep orange, `boost` / `none`

Service: `climate.set_preset_mode`

UI also shows preset label NORMAL/ECO/SLEEP/BOOST

### 6. Temperature

- Sensor `temperature` attribute → target
- Sensor `current_temperature` → current
- Arc 16-31°C, orange indicator, knob white border
- Buttons -/+ change 1°C, clamp 16-31
- Service: `climate.set_temperature`

### 7. Extras

- `hvac_action` attribute: heating, cooling, idle, etc. shown top
- `current_humidity` attribute: shown top right as "45% RH"

## Midea AC Specific

Midea AC via Midea Smart integration typically supports:

- hvac_modes: off, cool, heat, dry, fan_only, auto
- fan_modes: auto, low, medium, high
- swing_modes: off, vertical, horizontal, both
- preset_modes: none, eco, sleep, boost

If your entity doesn't support swing, button will still call service but HA will ignore — safe.

## Customization

Override climate entity per display:

```yaml
substitutions:
  climate_entity: "climate.living_room_ac"
```

Or change range in yaml: `min_value: 16 max_value: 31`

## Performance

- All sensors `internal: true` except needed
- Lambda color changes avoid extra lvgl.obj.update calls where possible
- No shadows, simple bg 0x0F1115
