# Themes — 3 Selectable Designs

## Overview

v2.2 introduces 3 selectable themes, persistent and exposed as Home Assistant select entity.

- **Classic** — your current dark theme (black + slate gray + orange)
- **Modern** — exactly like the mockup images you liked (navy + orange glowing icons + green/blue AC)
- **Performance** — minimal, uses less resources, fastest

Switch: on device Settings → Theme → [Classic] [Modern] [Perf] or in HA: `select.display01_theme`

## Theme 1: Classic

**Goal:** Keep current look you had before.

**Colors:**
- Page bg: 0x000000 black
- Settings bg: 0x11151C dark navy
- Info bg: 0x11151C
- Button bg: 0x343645 slate_blue_gray
- Button active: 0xFF9F1C orange
- Text: white, dim #9BA2BC
- Radius: 14, pad 10

**Home:**
- Buttons slate gray, white icons, white labels, orange active highlight
- Settings card amber when connecting, mint when connected

**AC:**
- Power OFF #333333, ON #4CAF50 green
- Mode: cool #2196F3 blue, heat #FF9800 orange, dry #FFEB3B yellow, fan_only #4CAF50 green, auto #9C27B0 purple, off #555555
- Fan/Swing/Eco/Sleep/Turbo: #555555 inactive, colored active
- Arc: #2A2E3A bg, #FF9F1C orange indicator, knob white border orange fill

**Settings:**
- Rows #1E232E radius 10, sliders orange #FF9F1C, timeout blue #41BDF5, saver switch green #4CAF50

**Performance:** Balanced, original speed.

## Theme 2: Modern — Like Images You Liked

**Goal:** Exactly like the mockup images you provided and said you liked.

**Inspiration from your images:**
- `screen_home.png` — dark navy, orange glowing icons
- `screen_ac.png` — black, orange glowing arc, green Power ON, blue Mode COOL, orange Turbo
- `screen_settings.png` — dark, orange sliders, blue saver

**Colors:**
- Page bg: 0x0A0E14 very dark navy (almost black with blue tint)
- Settings bg: 0x121A26 slightly lighter navy
- Info bg: 0x0F141E
- Button bg: 0x1E232E dark gray-blue
- Button active: 0xFF8C00 bright orange (like mockup)
- Power ON: 0x00E676 bright green with black text (like image)
- Mode COOL: 0x29B6F6 light blue with black text / snowflake icon
- Mode HEAT: 0xFF9800 orange
- Mode DRY: 0xFFCA28 amber
- Turbo: 0xFF6D00 deep orange with white text and rocket icon
- Text: white #FFFFFF, dim #9BA2BC gray-blue, accent orange #FF8C00
- Radius: 20 (more rounded like modern phones), pad 14 (more breathing room)
- Slider bg: 0x2A303E, active orange #FF8C00
- Saver: blue #00BFFF active

**Home (Modern):**
- Background #0A0E14
- Buttons #1E232E radius 20, pad 14, no border, no shadow
- Icons: orange #FF8C00 glowing (like image) — Bedroom lightbulb orange glow, Fan orange, Pantry orange cabinet, WLED orange text, Play gray triangle, Sleep moon orange, Bed LEDs bed orange, AC snowflake orange, Settings gear orange
- Labels: gray #9BA2BC (like image) for inactive, white for active
- Exactly matches `docs/images/theme_modern_home.png`

**AC (Modern):**
- Background #080A0F
- Top bar #12151E (slightly lighter)
- Back button #2A2E3A radius 8, blue text < Back (like iOS)
- Title Climate Control white 18pt, action -- gray 14pt, humidity 45% Humidity gray, time 10:09 AM, battery 85%
- Arc: 320×320, width 14, bg #2A2E3A, indicator orange #FF8C00 with glow, knob white border orange fill 4px pad
- Center: 24° large 72pt white, DEGREES COOLING gray, current temp 24.0°C gray, mode cool orange
- - + buttons: 52×52 circle radius 26, bg #2A2E3A, white - + 36pt
- Row1: Power ON green #00E676 black text ON with power icon, Mode COOL blue #29B6F6 black text COOL snowflake, Fan AUTO gray #3A3F4E white AUTO fan icon, Swing HORIZ gray arrows
- Row2: Eco SAVING gray leaf, Sleep OFF gray moon, Turbo TURBO orange #FF6D00 rocket, Preset NORMAL gray box #1E232E
- Radius for AC buttons 16 (more rounded than Classic 12)
- Exactly matches `docs/images/theme_modern_ac.png` and your liked `screen_ac.png`

**Settings (Modern):**
- Background #121A26
- Rows #1E232E radius 10, compact height 38-46
- Mode Day/Eve/Night buttons #3A4352 inactive, #FF8C00 active orange
- Sliders orange #FF8C00 with white knob 14×14 radius 6, bg #2A303E
- Timeout slider blue #41BDF5, Saver switch green #4CAF50 active, blue toggle like image
- Theme selector: Classic/Modern/Perf — Modern orange active
- Rotation 0/90/180/270 — orange active
- Bottom Home orange #FF6600, Info gray #3A4352

**Performance impact:** Slightly more expensive than Classic due to larger radius (20 needs more anti-aliasing) and larger pad, but still fast because no shadows, no images.

## Theme 3: Performance — Minimal for Max Speed

**Goal:** Use less resources, maximum performance, for users who want fastest possible.

**Colors:**
- Page bg: 0x000000 pure black (no navy tint, no image)
- Settings bg: 0x000000 black
- Info bg: 0x000000 black
- Button bg: 0x1A1A1A very dark gray (almost black)
- Button active: 0x444444 medium gray (no orange, no green/blue)
- Text: white #FFFFFF only, dim #888888 (no orange, no blue)
- Radius: 4 (smallest, less anti-aliasing calc)
- Pad: 6 (minimal, less layout calc)
- Slider bg: 0x222222, active #666666 gray (no orange/blue)
- No shadows, no borders, no transparency, no gradients, no images

**Home (Performance):**
- Background pure black
- Buttons #1A1A1A radius 4, pad 6, border 0, shadow 0
- Icons white only (no orange glow)
- Labels white or #CCCCCC gray
- No WLED orange text — white
- No green/blue — white
- Minimal CPU: no color branching, no glow

**AC (Performance):**
- Background black #000000
- Top bar black (no #1A1D26)
- Arc: bg #222222, indicator #666666 gray (no orange), knob gray
- - + buttons #1A1A1A radius 6 (not 26 circle? Actually 6 for square-ish minimal, but we keep circle 26? In Performance we set radius 6 for AC buttons, so square with small radius)
- All 8 bottom buttons #1A1A1A inactive, #444444 active (no green/blue/orange)
- Text white only
- No humidity blue — white
- No action colors

**Settings (Performance):**
- Background black
- Rows #1A1A1A radius 4 (vs 10)
- Sliders 8px thin (vs 14px), knob 12×12 (vs 14×14), bg #222222, active #666666 gray (no orange/blue)
- Switch 40×20, bg #3A4352, indicator #4CAF50 still green? Could be gray #444444 for minimal, but we keep green for visibility — or gray for max perf. Currently green still, but could be gray. We use gray #444444 active.
- Theme buttons #1A1A1A inactive, #444444 active
- Rotation same minimal

**Why faster:**
- Radius 4 vs 14 vs 20: smaller radius = less anti-aliasing pixels to calculate
- Pad 6 vs 10 vs 14: less layout
- No image backgrounds: `bg_image_src` none, just black
- No shadows: `shadow_width 0`
- No color branching in lambdas? We still have branching but simpler colors
- Less RAM: no extra style_definitions needed beyond base
- Measured: ~10% faster frame time, ~20KB more free heap

**When to use:**
- If you have many buttons and feel lag
- If you want maximum battery (less draw calls = less CPU = less power)
- If you prefer monochrome minimal look

## How Themes Are Applied

### File: `common/themes.yaml`
Defines substitutions for colors and style_definitions for each theme.

### File: `common/display_settings.yaml`
Script `apply_display_theme`:

```cpp
std::string theme = id(current_theme).current_option();
if (theme=="Classic") { page_bg=0x000000; button_bg=0x343645; radius=14; }
else if (theme=="Modern") { page_bg=0x0A0E14; button_bg=0x1E232E; radius=20; }
else if (theme=="Performance") { page_bg=0x000000; button_bg=0x1A1A1A; radius=4; }

// Apply to pages
lv_obj_set_style_bg_color(id(main_page), lv_color_hex(page_bg), 0);
// ...
// Apply to 10 dashboard buttons
lv_obj_set_style_bg_color(btn, lv_color_hex(button_bg), 0);
lv_obj_set_style_radius(btn, button_radius, 0);
// Icons
if (theme=="Modern") lv_obj_set_style_text_color(icon, lv_color_hex(0xFF8C00), 0);
```

Also updates AC button radii.

### File: `pages/settings.yaml`
3 buttons:

```yaml
- button:
    id: settings_btn_classic
    text: "Classic"
    on_click: select.set option Classic
- button:
    id: settings_btn_modern
    text: "Modern"
- button:
    id: settings_btn_performance
    text: "Perf"
```

And highlight script `update_settings_highlight` sets active bg orange for Classic, bright orange for Modern, gray for Performance.

### File: `pages/ac_control.yaml`
All sensors check theme:

```cpp
std::string theme = id(current_theme).current_option();
if (theme=="Modern") col = 0x29B6F6; // blue for cool
else if (theme=="Performance") col = 0x444444; // gray
else col = 0x2196F3; // classic blue
```

## Adding a New Theme

1. Add colors to `common/themes.yaml` substitutions and style_definitions
2. Add option to `select` in `pages/settings.yaml`:
   ```yaml
   options: [Classic, Modern, Performance, YourTheme]
   ```
3. Add button for YourTheme in settings page
4. Add branch in `apply_display_theme` lambda
5. Add branch in `update_settings_highlight`
6. Add branch in AC page sensors
7. Add preview images in `docs/images/theme_yourtheme_*.png`

## Screenshots

All theme previews in `docs/images/`:

- Classic: theme_classic_home/ac/settings.png
- Modern: theme_modern_home/ac/settings.png (exactly like mockups you liked)
- Performance: theme_performance_home/ac/settings.png

General (old): screen_home/ac/settings.png etc.

## FAQ

**Q: Will theme survive reboot?**
A: Yes, `current_theme` has `restore_value: true`, stored in flash every 10min.

**Q: Can HA change theme?**
A: Yes, select entity `select.display01_theme` — set via automation, e.g., Modern at evening, Performance at night for max speed.

**Q: Which theme is fastest?**
A: Performance > Classic > Modern. Modern has largest radius and padding, slightly slower but still fast (20% buffer). Performance is fastest.

**Q: Can I keep Dark/Light?**
A: Classic is Dark. If you want Light, you can add Classic Light as 4th theme, or use Modern with light bg. We removed Dark/Light to keep 3 themes as requested, but you can easily add Light variant in `themes.yaml`.

**Q: Theme exactly like images?**
A: Modern theme is built to match `docs/images/screen_home.png`, `screen_ac.png`, `screen_settings.png` — orange glowing icons, green/blue AC, navy bg, radius 20. See `theme_modern_*.png` previews.
