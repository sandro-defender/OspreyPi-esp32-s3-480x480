# Custom Dashboard

## Default Dashboard

File: `esphome-modular-lvgl-buttons/dashboards/home.yaml`

9 buttons + AC + Settings:

- Button 1 tall 228px Bedroom light
- Button 2 109px Fan switch
- Button 3 109px Pantry
- Button 4 109px WLED script + light state
- AC nav 109px → ac_main_page
- Button 5 109px play/pause fullscreen icon
- Button 6 109px Sleep script
- Button 7 tall 228px Bed LEDs dimmer + long press color page
- Settings 109px + connection status
- Button 9 109px Leave script

## Override Per Display

In Display01.yaml substitutions:

```yaml
substitutions:
  dashboard_button_1_text: "office"
  dashboard_button_1_entity: "light.office_lights"
  dashboard_button_1_action: "light.toggle"
  dashboard_button_1_icon: "\U000F0335" # mdi-lightbulb
  dashboard_button_1_height: "228px"
```

Pattern: `dashboard_button_<n>_<text|entity|action|icon|height>`

Button 4 also has `dashboard_button_4_state_entity` because action is script but state is light.

Button 5 uses `entity`, `action`, `icon`, `height` only (fullscreen).

Button 7 uses `text`, `entity`, `icon`, `height` (dimmer).

## Actions

Any HA action:

```yaml
light.toggle
switch.toggle
script.turn_on
scene.turn_on
button.press
automation.trigger
media_player.media_play_pause
```

Must match domain.

## Icons

Material Design Icons — add glyph to `common/assets.yaml`:

```yaml
font:
  - file: .../materialdesignicons-webfont.ttf
    id: mdi_icons_40
    glyphs:
      - $mdi_lightbulb
      - $mdi_your_new_icon
```

Find code: https://pictogrammers.com/library/mdi/ — use \U000Fxxxx

## Create New Profile

1. Copy `dashboards/home.yaml` → `dashboards/upstairs.yaml`
2. Edit cards order
3. Point display:

```yaml
packages:
  display: !include esphome-modular-lvgl-buttons/common/display.yaml
  dashboard: !include esphome-modular-lvgl-buttons/dashboards/upstairs.yaml
```

Hardware, settings, OTA, weather remain.

**Important:** keep the `script:` block from home.yaml
(`apply_display_theme`, `update_settings_highlight`, `apply_dashboard_theme`
and the `repaint_button_*` calls) in the new profile — that is the 4-theme
repaint engine. Without it the device boots Classic-colored and on/off skins
stop updating. (`update_settings_highlight` is also called by the
`screensaver_language` select in `pages/screensaver.yaml`, so a custom
dashboard that keeps the screensaver page needs it too.)

## Button Templates

In `buttons/`:

- `entity_button.yaml` — generic with icon top_left, text bottom_left, state color
- `dimmer_light_button.yaml` — shows brightness bar, long press → color page
- `page_button.yaml` — opens LVGL page
- `fullscreen_entity_button.yaml` — large icon centered
- `color_picker.yaml` etc.

## State Listeners

In `sensors/`:

- `switch_or_light_button_state.yaml` — subscribes to HA entity, updates button bg
- `dimmer_light_state.yaml` — also brightness
- `play_pause_button_state.yaml`

They are included with vars `uid` and `entity_id`.

## Performance Tips for Custom Dashboard

- Keep 9-10 buttons max — more = slower flex wrap
- Use 109px and 228px heights — preserves 3-column layout
- Avoid images >100×100
- Use bpp 4 fonts
- No scrollable main_page — flex wrap is fast
