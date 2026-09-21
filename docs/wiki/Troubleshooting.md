# Troubleshooting

## Card Does Nothing

1. Check HA connected — the Settings card status icon on its colored halo should be the connected (mint/green) state, not amber (connecting) or red (offline)
2. Enable **Allow the device to perform Home Assistant actions** in ESPHome integration → device → settings
3. Check action matches domain: light.toggle for light, switch.toggle for switch
4. Check ESPHome logs: `esphome logs Display01.yaml` — look for "Home Assistant is offline; ignored"

## State Color Wrong

- Card action target and state source must be same entity, or use `state_entity` for button 4
- Example: button 4 action `script.wled_light_togle_animated` but state `light.wled_new` — correct because script has no state
- If you set `dashboard_button_1_entity: light.office` but action `switch.toggle` — mismatch, use light.toggle

## Display 02 Upside Down

Display 02 starts 180° for mounting. Change in settings page Rotation → 0°, or in YAML:

| Rotation | display_rotation | display_rotation_index |
|---|---|---|
| 0° | "0" | "0" |
| 90° | "90" | "1" |
| 180° | "180" | "2" |
| 270° | "270" | "3" |

Both must match.

## WiFi Unavailable

- Fallback AP `Display 01 Setup` open, no password
- Info page shows QR code when disconnected: scan to connect phone, then set WiFi via captive portal
- Check secrets.yaml ssid/password
- 2.4GHz only, not 5GHz

## Settings Laggy

- You are on old version <2.1 — update, new settings has no dropdowns
- If still laggy after update: check LVGL buffer 20%, log_level ERROR, fonts bpp 4

## AC Swing/Eco Not Working

- Check HA → Developer Tools → States → climate.midea_ac → attributes
- Must have `swing_modes` and `preset_modes`
- Midea AC integration (Midea Smart) supports them, but generic thermostat may not
- Service calls are safe — HA ignores unsupported

## Memory / Rendering Problems

- Keep `lvgl_buffer_size` 20% max, 12% min — higher uses more PSRAM but faster
- Don't add entire icon ranges — include only used glyphs in `common/assets.yaml`
- Keep images 480×480 max, RGB565, resize explicit
- Avoid large JPEG backgrounds >200KB
- Check free heap in info page — should be >80KB internal, >4MB PSRAM

## Boot Loop

- Check `watchdog_timeout: 60s` — if RGB task blocks, watchdog resets
- Reduce `pclk_frequency` 16MHz → 12MHz if unstable
- Check power supply 5V 2A minimum — display draws ~500mA peak

## OTA Fails

- Use USB first time
- OTA widget shows progress — if stuck at 0%, check WiFi signal >-70dBm
- Logs: `ota_state` on_error prints error code

## Time / Weather Wrong

- Check `latitude`/`longitude` in secrets.yaml
- Check `weather_entity` in `common/display.yaml` — default `weather.openweathermap`, change to `weather.home`
- System time from HA — ensure HA time correct

## Touch Not Working / Mirrored

- In `hardware/osptek-esp32-s3-48x48.yaml` touchscreen transform:

```yaml
transform:
  mirror_x: false
  mirror_y: false
```

Try true/false combos if axes mirrored.

## Validation Fails in CI

- GitHub Actions uses ESPHome 2026.9.0 pinned
- Run locally `esphome config Display01.yaml` — fix errors
- Common: missing glyph in mdi_icons_40, wrong font id (nunito_32 exists as alias now)

## Still Stuck?

- Open issue with logs, YAML substitutions, and photo of screen
- Include info page values: heap, PSRAM, signal, uptime
