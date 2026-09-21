# OspreyPi Wiki — Home

Welcome to OspreyPi ESP32-S3 480×480 smart display wiki!

## What is OspreyPi?

OspreyPi is a modular ESPHome + LVGL dashboard for Home Assistant, designed for the 480×480 ST7701S + FT6336 touchscreen powered by ESP32-S3 with 16MB flash and 8MB octal PSRAM.

## Key Features v2.1

- **Fast**: 20% LVGL buffer, 7 fonts only, no dropdowns, ERROR logging
- **Modular**: Display01.yaml and Display02.yaml share same firmware, differ only identity/rotation/API key
- **Native HA**: entity state feedback, no helper automations needed
- **AC Expanded**: Power, Mode, Fan, Swing, Eco, Sleep, Turbo, Humidity, Action
- **Settings Simplified**: Button-based, instant response, template selects
- **Persistent**: brightness, timeout, theme, rotation, screensaver restored after reboot
- **Screensaver**: time, Georgian/English date, weather temp/humidity/wind with icon
- **Diagnostics**: info page with heap, PSRAM, WiFi, IP, QR for AP mode

## Pages

- [Installation](Installation.md)
- [Hardware](Hardware.md)
- [Performance Optimizations](Performance.md)
- [AC Control](AC-Control.md)
- [Settings](Settings.md)
- [Custom Dashboard](Custom-Dashboard.md)
- [Troubleshooting](Troubleshooting.md)

## Quick Links

- Project root README: ../../README.md
- Device specs: ../../DEVICE_SPECS.md
- Hardware photos: ../../hardware/img/
- UI mockups: ../images/

## Version

Current: **2.1 Performance Edition** — see `esphome-modular-lvgl-buttons/common/display.yaml` project_version
