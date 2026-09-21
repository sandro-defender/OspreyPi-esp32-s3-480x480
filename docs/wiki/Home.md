# OspreyPi Wiki — Home

Welcome to OspreyPi ESP32-S3 480×480 smart display wiki!

## What is OspreyPi?

OspreyPi is a modular ESPHome + LVGL dashboard for Home Assistant, designed for the 480×480 ST7701S + FT6336 touchscreen powered by ESP32-S3 with 16MB flash and 8MB octal PSRAM.

## Key Features v2.3 Themes Edition

- **4 Themes**: Classic (flat dark), Modern (raised tiles + orange glow), Performance (minimal, fastest), Daylight (warm raised dark cards) — switch on device or from HA, persistent
- **Fast**: 50% LVGL buffer, bpp4 fonts, no dropdowns, ERROR-only logging, theme-aware repaints
- **Modular**: Display01.yaml and Display02.yaml share the same firmware packages
- **Native HA**: entity state feedback on every card, theme/brightness/rotation select entities
- **AC page**: Power, Mode, Fan, Swing, Eco, Sleep, Turbo, Preset, 16–31 °C arc, −/+ steppers with 0.5 °C long-press, live action + humidity + room temp — colors adapt to theme
- **Light page**: Bed LEDs dimmer card → brightness/saturation sliders + 12-segment hue ring
- **Settings page**: button-based (no dropdowns), 4 theme buttons, instant highlight
- **Persistent**: brightness, timeout, theme, rotation, screensaver restored after reboot
- **Screensaver**: big clock, Georgian date, weather readout
- **Diagnostics**: info page with uptime, WiFi, signal, heap, PSRAM, HA status
- **Swipe navigation**: Home ↔ AC ↔ Light

## Pages

- [Installation](Installation.md)
- [Hardware](Hardware.md)
- [Themes](Themes.md) — all 4 themes
- [Performance Optimizations](Performance.md)
- [AC Control](AC-Control.md)
- [Settings](Settings.md)
- [Custom Dashboard](Custom-Dashboard.md)
- [Troubleshooting](Troubleshooting.md)

## Quick Links

- Project root README: ../../README.md
- AI-agent operating manual: ../../AGENTS.md
- Device specs: ../../DEVICE_SPECS.md
- Hardware photos: ../../hardware/img/
- UI mockups (regenerable via `tools/generate_screenshots.py`): ../images/

## Version

Current: **2.3 Themes Edition** — Classic / Modern / Performance / Daylight
