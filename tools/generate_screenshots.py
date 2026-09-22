#!/usr/bin/env python3
"""
OspreyPi ESP32-S3 480x480 — docs/images screenshot generator.

Renders device-accurate 480x480 UI mockups for every theme and page straight
from the palettes / layout coordinates used by the firmware YAML
(esphome-modular-lvgl-buttons/common/themes/*.yaml + pages/*.yaml +
dashboards/home.yaml), using the real bundled fonts (Nunito, DejaVu Bold,
Noto Georgian, Material Design Icons) and real image assets
(screensaver bg, weather + connection icons, lightbulb).

Output (docs/images/):
  theme_<theme>_home.png / theme_<theme>_ac.png / theme_<theme>_settings.png
    for <theme> in classic | modern | performance | daylight   (480x480)
  screen_ac.png, screen_settings.png, screen_light.png,
  screen_screensaver.png, screen_info.png                       (480x480)
  preview_classic_v2_home.png, preview_modern_v2_home.png,
  preview_performance_v2_home.png, preview_daylight_home.png    (960x960)
  theme_preview_sheet.png                                        (1008x1008)

Usage:
  python3 tools/generate_screenshots.py [output-dir]

Requires: pip install pillow
"""

from __future__ import annotations

import math
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "esphome-modular-lvgl-buttons" / "assets"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "docs" / "images"

FONT_FILES = {
    "nunito": ASSETS / "fonts" / "Nunito-SemiBold.ttf",
    "bold": ASSETS / "fonts" / "DejaVuSans-Bold.ttf",
    "geo": ASSETS / "fonts" / "NotoSansGeorgian.ttf",
    "mdi": ASSETS / "fonts" / "materialdesignicons-webfont.ttf",
}

# Material Design Icons codepoints (from common/mdi_glyph_substitutions.yaml)
MDI = {
    "lightbulb": 0xF0335,
    "fan": 0xF0210,
    "fan_auto": 0xF171D,
    "string_lights": 0xF12BA,
    "ac": 0xF001B,
    "play_pause": 0xF040E,
    "night": 0xF0594,
    "cog": 0xF0493,
    "exit": 0xF0FC5,
    "power": 0xF0425,
    "snowflake": 0xF0717,
    "fire": 0xF0238,
    "water": 0xF058C,
    "leaf": 0xF032A,
    "moon": 0xF0F65,
    "rocket": 0xF0463,
    "swap": 0xF04E1,
    "arrow_left": 0xF004D,
    "thermometer": 0xF050F,
    "home": 0xF02DC,
    "restart": 0xF0709,
    "account": 0xF0004,
    "wind": 0xF059D,
}

def hx(v) -> tuple:
    """0xRRGGBB -> (r, g, b) (accepts tuples unchanged)"""
    if isinstance(v, tuple):
        return v
    return ((v >> 16) & 255, (v >> 8) & 255, v & 255)


# ─────────────────────────────────────────────────────────────────────────────
# Theme palettes — mirror common/themes/*.yaml + the repaint lambdas in
# dashboards/home.yaml (apply_dashboard_theme / repaint_button_*),
# pages/ac_control.yaml (ac_main_refresh) and pages/settings.yaml
# (apply_settings_theme).
# ─────────────────────────────────────────────────────────────────────────────
THEMES = {
    "classic": dict(
        page=0x000000, settings_bg=0x11151C, info_bg=0x11151C,
        ac_bg=0x0F1115, ac_top=0x1A1D26,
        # home tiles
        tile=0x343645, tile_on=0xF37320, tile_radius=14, pad=10,
        icon_off=0x9BA2BC, icon_on=0xFFFFFF, tile_label=0xFFFFFF,
        # AC page
        ac_off_bg=0x343645, ac_radius=12,
        power_on=0x4CAF50, power_text=0xFFFFFF,
        mode_cool=0x2196F3, mode_text=0xFFFFFF,
        step_bg=0x343645, step_radius=26,
        arc_track=0x2A2E3A, arc_accent=0xFF9F1C,
        back_bg=0x151B26, back_border=0x29B6F6, back_radius=10,
        # settings page
        row_bg=0x1E232E, row_radius=10, label=0xAAAAAA, value=0xCCCCCC,
        track=0x2A303E, accent=0xFF9F1C, timeout=0x41BDF5,
        sel_active=0xFF9F1C, sel_inactive=0x3A4352, knob=0xFFFFFF,
        # info page
        info_row_a=0x1E2530, info_row_b=0x151A24, info_key=0x8891A0,
        raised=False, glow_active=False,
    ),
    "modern": dict(
        page=0x0A0E14, settings_bg=0x121A26, info_bg=0x0F141E,
        ac_bg=0x080A0F, ac_top=0x12151E,
        tile=0x323B4D, tile_on=0x323B4D, tile_radius=20, pad=14,
        grad_top=0x323B4D, grad_bottom=0x1A212C, bevel=0x3D4658,
        icon_off=0xFF8C00, icon_on=0xFF8C00, tile_label=0x9BA2BC,
        ac_off_bg=0x232A38, ac_radius=18,
        power_on=0x00E676, power_text=0x000000,
        mode_cool=0x29B6F6, mode_text=0x000000,
        step_bg=0x2A3242, step_radius=16,
        arc_track=0x232A38, arc_accent=0xFF8C00,
        back_bg=0x151B26, back_border=0x29B6F6, back_radius=10,
        row_bg=0x1E2530, row_radius=10, label=0xAAAAAA, value=0xCCCCCC,
        track=0x2A303E, accent=0xFF8C00, timeout=0x41BDF5,
        sel_active=0xFF8C00, sel_inactive=0x2A3142, knob=0xFFFFFF,
        info_row_a=0x1E2530, info_row_b=0x151A24, info_key=0x8891A0,
        raised=True, glow_active=True, glow_color=0xFF8C00,
        glow_border=0xFFB74D,
    ),
    "performance": dict(
        page=0x000000, settings_bg=0x000000, info_bg=0x000000,
        ac_bg=0x000000, ac_top=0x000000,
        tile=0x1A1A1A, tile_on=0x444444, tile_radius=4, pad=6,
        icon_off=0xFFFFFF, icon_on=0xFFFFFF, tile_label=0xCCCCCC,
        ac_off_bg=0x1A1A1A, ac_radius=6,
        power_on=0x444444, power_text=0xFFFFFF,
        mode_cool=0x444444, mode_text=0xFFFFFF,
        step_bg=0x1A1A1A, step_radius=4,
        arc_track=0x1A1A1A, arc_accent=0x666666,
        back_bg=0x151B26, back_border=0x29B6F6, back_radius=10,
        row_bg=0x141414, row_radius=4, label=0x888888, value=0xCCCCCC,
        track=0x222222, accent=0x666666, timeout=0x41BDF5,
        sel_active=0x444444, sel_inactive=0x1A1A1A, knob=0xFFFFFF,
        info_row_a=0x141414, info_row_b=0x0A0A0A, info_key=0x888888,
        raised=False, glow_active=False,
    ),
    "daylight": dict(
        page=0x0B0C0D, settings_bg=0x0F1216, info_bg=0x0F1216,
        ac_bg=0x0B0C0D, ac_top=0x191D23,
        tile=0x191D23, tile_on=0xE37220, tile_radius=20, pad=14,
        grad_top=0x1F242C, grad_bottom=0x151A20, bevel=0x242A33,
        icon_off=0x8A9099, icon_on=0xF8953D, tile_label=0xFFFFFF,
        ac_off_bg=0x191D23, ac_radius=18,
        power_on=0x4CAF50, power_text=0xFFFFFF,
        mode_cool=0x29B6F6, mode_text=0xFFFFFF,
        step_bg=0x191D23, step_radius=18,
        arc_track=0x232932, arc_accent=0xE37220,
        back_bg=0x191D23, back_border=0xF8953D, back_radius=18,
        row_bg=0x171A1F, row_radius=12, row_border=0x2E3542,
        label=0xB4B8BC, value=0xFFFFFF,
        track=0x2A303E, accent=0xE37220, timeout=0xE37220,
        sel_active=0xFF9F1C, sel_inactive=0x3A4352, knob=0xF8953D,
        info_row_a=0x191D23, info_row_b=0x14181E, info_key=0xB4B8BC,
        raised=True, glow_active=True, glow_color=0xE37220,
        glow_border=0xF8953D,
    ),
}

# Raised "3D" tile parameters per theme (depth_dark / depth_light styles)
DEPTH = {
    "modern": dict(shadow_w=14, shadow_opa=0.55, border=0x3D4658),
    "daylight": dict(shadow_w=16, shadow_opa=0.60, border=0x242A33),
}


class Screen:
    """480x480 (or scaled) canvas with supersampled drawing helpers."""

    def __init__(self, out_px: int = 480, k: int = 3, bg: int = 0x000000):
        self.k = k
        self.px = out_px
        self.size = out_px * k
        self.img = Image.new("RGB", (self.size, self.size), hx(bg))
        self.draw = ImageDraw.Draw(self.img, "RGBA")
        self._fonts: dict = {}

    # ── fonts / text ────────────────────────────────────────────────────
    def font(self, key: str, size: int):
        cache_key = (key, size)
        if cache_key not in self._fonts:
            self._fonts[cache_key] = ImageFont.truetype(
                str(FONT_FILES[key]), size * self.k
            )
        return self._fonts[cache_key]

    def text(self, x, y, s, fkey, fsize, color, anchor="la"):
        self.draw.text(
            (x * self.k, y * self.k), s, font=self.font(fkey, fsize),
            fill=hx(color), anchor=anchor,
        )

    def glyph(self, x, y, name, size, color, anchor="la"):
        self.text(x, y, chr(MDI[name]), "mdi", size, color, anchor)

    # ── primitives ──────────────────────────────────────────────────────
    def rrect(self, box, radius, fill=None, outline=None, width=1):
        if fill is None and outline is None:
            return
        self.draw.rounded_rectangle(
            [c * self.k for c in box], radius * self.k,
            fill=hx(fill) if fill is not None else None,
            outline=hx(outline) if outline is not None else None,
            width=width * self.k,
        )

    def rect(self, box, fill):
        self.draw.rectangle([c * self.k for c in box], fill=hx(fill))

    def circle(self, cx, cy, r, fill=None, outline=None, width=1):
        box = [(cx - r) * self.k, (cy - r) * self.k, (cx + r) * self.k, (cy + r) * self.k]
        self.draw.ellipse(
            box,
            fill=hx(fill) if fill is not None else None,
            outline=hx(outline) if outline is not None else None,
            width=width * self.k,
        )

    def arc(self, box, start, end, color, width, rounded=False):
        """LVGL-style arc: angles 0..360 clockwise from 3 o'clock."""
        # draw wide arc as a pieslice difference for clean anti-aliasing
        cx = (box[0] + box[2]) / 2
        cy = (box[1] + box[3]) / 2
        r_out = (box[2] - box[0]) / 2
        r_in = r_out - width
        layer = Image.new("L", self.img.size, 0)
        d = ImageDraw.Draw(layer)
        end_n = end if end > start else end + 360
        # outer minus inner pie
        d.pieslice(
            [(cx - r_out) * self.k, (cy - r_out) * self.k,
             (cx + r_out) * self.k, (cy + r_out) * self.k],
            start, end_n, fill=255,
        )
        d.pieslice(
            [(cx - r_in) * self.k, (cy - r_in) * self.k,
             (cx + r_in) * self.k, (cy + r_in) * self.k],
            start, end_n, fill=0,
        )
        solid = Image.new("RGB", self.img.size, hx(color))
        self.img.paste(solid, (0, 0), layer)

    def vgrad(self, box, radius, top, bottom):
        """Vertical gradient rounded-rect (LVGL bg_grad ver)."""
        x0, y0, x1, y1 = [c * self.k for c in box]
        h = max(1, y1 - y0)
        grad = Image.new("RGB", (1, h))
        for i in range(h):
            f = i / (h - 1) if h > 1 else 0
            grad.putpixel(
                (0, i),
                tuple(int(a + (b - a) * f) for a, b in zip(hx(top), hx(bottom))),
            )
        grad = grad.resize((x1 - x0, h))
        mask = Image.new("L", (x1 - x0, h), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            [0, 0, x1 - x0 - 1, h - 1], radius * self.k, fill=255
        )
        self.img.paste(grad, (x0, y0), mask)

    def _blurred_rrect(self, box, radius, color, alpha, blur, offset_y=0):
        layer = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        b = [box[0] * self.k, (box[1] + offset_y) * self.k,
             box[2] * self.k, (box[3] + offset_y) * self.k]
        d.rounded_rectangle(b, radius * self.k, fill=hx(color) + (int(255 * alpha),))
        layer = layer.filter(ImageFilter.GaussianBlur(blur * self.k))
        self.img.paste(layer, (0, 0), layer)

    def glow(self, box, radius, color, strength=0.75, blur=7):
        self._blurred_rrect(box, radius, color, strength, blur, 0)

    def shadow(self, box, radius, strength=0.55, blur=7, offset_y=5):
        self._blurred_rrect(box, radius, 0x000000, strength, blur, offset_y)

    def paste_image(self, img, cx, cy, w, h, darken=None):
        im = img.resize((int(w * self.k), int(h * self.k)), Image.LANCZOS)
        if darken is not None:
            im = Image.eval(im, lambda p: int(p * darken))
        self.img.paste(im, (int((cx - w / 2) * self.k), int((cy - h / 2) * self.k)))

    def save(self, path: Path):
        OUT.mkdir(parents=True, exist_ok=True)
        self.img.resize((self.px, self.px), Image.LANCZOS).save(path)
        print(f"wrote {path.relative_to(ROOT)}  ({self.px}x{self.px})")


# ─────────────────────────────────────────────────────────────────────────────
# Shared widgets
# ─────────────────────────────────────────────────────────────────────────────
def tile(s: Screen, box, theme: str, active=False, radius=None, glow=None):
    """Home-dashboard tile / AC button container per theme.

    glow: None = no colored glow; or (border_color, glow_color) for active
    filled states (Modern glow_green/glow_blue/glow_orange, Daylight warm).
    """
    t = THEMES[theme]
    r = radius if radius is not None else t["tile_radius"]

    if t["raised"]:
        d = DEPTH[theme]
        if glow is not None:
            s.glow(box, r, glow[1], 0.75, 9)
        else:
            s.shadow(box, r, d["shadow_opa"], 6, 5)
        if active and glow is None:
            # Daylight active tile: solid accent fill + warm glow
            s.glow(box, r, t["glow_color"], 0.7, 8)
            s.rrect(box, r, fill=t["tile_on"])
            s.rrect(box, r, outline=t["glow_border"], width=2)
        else:
            s.vgrad(box, r, t["grad_top"], t["grad_bottom"])
            s.rrect(box, r, outline=d["border"], width=1)
            if glow is not None:
                s.rrect(box, r, outline=glow[0], width=2)
    else:
        fill = t["tile_on"] if active else t["tile"]
        s.rrect(box, r, fill=fill)
    return box


def entity_tile(
    s: Screen, box, theme: str, icon: str, label, active: bool,
    icon_size=40, label_size=24,
):
    """Home dashboard entity button (buttons/entity_button.yaml + repaint skin)."""
    t = THEMES[theme]
    tile(s, box, theme, active)
    pad = t["pad"]
    icon_color = t["icon_on"] if active or theme in ("modern", "performance") else t["icon_off"]
    if theme == "performance":
        icon_color = 0xFFFFFF
    if theme == "daylight":
        icon_color = t["icon_on"] if active else t["icon_off"]
    s.glyph(box[0] + pad, box[1] + pad - 2, icon, icon_size, icon_color)
    if label:
        s.text(box[0] + pad, box[3] - pad - label_size, label, "nunito",
               label_size, t["tile_label"])


# ─────────────────────────────────────────────────────────────────────────────
# Page renderers
# ─────────────────────────────────────────────────────────────────────────────
def home_screen(theme: str, out_px=480, k=3) -> Screen:
    t = THEMES[theme]
    s = Screen(out_px, k, bg=t["page"])

    # flex column_wrap: 3 columns of 150px, pad_column 8, page pad 4 (6 modern)
    pad = 6 if theme == "modern" else 4
    col_x = [pad, pad + 158, pad + 316]
    row_y = [pad, pad + 236, pad + 353]  # 228 + 8, +109 + 8

    # Column 1 — Bedroom (tall, ON), Fan, Pantry
    entity_tile(s, (col_x[0], row_y[0], col_x[0] + 150, row_y[0] + 228), theme,
                "lightbulb", "Bedroom", True)
    entity_tile(s, (col_x[0], row_y[1], col_x[0] + 150, row_y[1] + 109), theme,
                "fan", "Fan", False)
    entity_tile(s, (col_x[0], row_y[2], col_x[0] + 150, row_y[2] + 109), theme,
                "lightbulb", "Pantry", False)

    # Column 2 — WLED (ON), AC nav, play/pause (fullscreen 80px icon), Sleep
    entity_tile(s, (col_x[1], row_y[0], col_x[1] + 150, row_y[0] + 109), theme,
                "string_lights", "WLED", True)
    entity_tile(s, (col_x[1], row_y[1], col_x[1] + 150, row_y[1] + 109), theme,
                "ac", "AC", False)
    b5 = (col_x[1], row_y[2], col_x[1] + 150, row_y[2] + 109)
    tile(s, b5, theme, False)
    icon5 = 0xFFFFFF if theme != "modern" else 0xFF8C00
    s.glyph((b5[0] + b5[2]) / 2, (b5[1] + b5[3]) / 2, "play_pause", 80,
            icon5, anchor="mm")

    # Column 3 — Bed LEDs (tall dimmer, ON), Settings card, Leave
    b7 = (col_x[2], row_y[0], col_x[2] + 150, row_y[0] + 228)
    entity_tile(s, b7, theme, "string_lights", "Bed LEDs", True)
    # dimmer slider: 18x172 top_right x-8 y18, dark_gray 80% track, mint fill
    sl_x, sl_y, sl_w, sl_h = b7[2] - 8 - 18, b7[1] + 18, 18, 172
    s.rrect((sl_x, sl_y, sl_x + sl_w, sl_y + sl_h), 9, fill=0x313131)
    val = 0.65
    s.rrect((sl_x, sl_y + sl_h * (1 - val), sl_x + sl_w, sl_y + sl_h), 9,
            fill=0x7ACF38)
    knob_y = sl_y + sl_h * (1 - val)
    s.circle(sl_x + sl_w / 2, knob_y, 9, fill=0xFFFFFF)

    # Settings card: cog top-left, status halo + connected icon, hint label
    bset = (col_x[2], row_y[1], col_x[2] + 150, row_y[1] + 109)
    tile(s, bset, theme, False)
    s.glyph(bset[0] + t["pad"], bset[1] + t["pad"] - 2, "cog", 22, 0xFFFFFF)
    halo_c = ((bset[0] + bset[2]) / 2, (bset[1] + bset[3]) / 2 - 4)
    halo = Image.new("RGBA", s.img.size, (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse(
        [(halo_c[0] - 34) * s.k, (halo_c[1] - 34) * s.k,
         (halo_c[0] + 34) * s.k, (halo_c[1] + 34) * s.k],
        fill=(0x39, 0xD1, 0x9C, int(255 * 0.22)),
    )
    s.img.paste(halo, (0, 0), halo)
    conn = Image.open(ASSETS / "images" / "connection" / "connected.png").convert("RGBA")
    s.paste_image(conn, halo_c[0], halo_c[1], 60, 60)
    s.text(bset[0] + t["pad"], bset[3] - t["pad"] - 14, "Tap · hold for info",
           "nunito", 14, 0x9BA2BC)

    entity_tile(s, (col_x[2], row_y[2], col_x[2] + 150, row_y[2] + 109), theme,
                "exit", "Leave", False)
    return s


def ac_screen(theme: str, out_px=480, k=3) -> Screen:
    t = THEMES[theme]
    s = Screen(out_px, k, bg=t["ac_bg"])

    # top bar tint
    s.rrect((0, 0, 480, 52), 0, fill=t["ac_top"])

    # header: back chip / title / humidity + room temp
    s.rrect((8, 7, 86, 43), t["back_radius"], fill=t["back_bg"],
            outline=t["back_border"], width=1)
    s.text(47, 25, "< Back", "nunito", 18, t["back_border"], anchor="mm")
    s.text(240, 26, "Climate Control", "nunito", 24, 0xFFFFFF, anchor="mm")
    s.text(472, 17, "47% Humidity", "nunito", 18,
           0xB4B8BC if theme == "daylight" else 0x9BA2BC, anchor="ra")
    s.text(472, 38, "Room 24.5°C", "nunito", 14, 0x6C7382, anchor="ra")

    # temperature gauge: 224x224 arc at y52, 135° → 45° (270° sweep), 16..31°C
    gx0, gy0, gx1, gy1 = 128, 52, 352, 276
    s.arc((gx0, gy0, gx1, gy1), 135, 45, t["arc_track"], 13)
    target = 24.0
    frac = (target - 16) / (31 - 16)
    s.arc((gx0, gy0, gx1, gy1), 135, 135 + 270 * frac, t["arc_accent"], 13)
    # knob at the arc end
    ang = math.radians(135 + 270 * frac)
    cx, cy, r = 240, 164, 112 - 6.5
    kx, ky = cx + r * math.cos(ang), cy + r * math.sin(ang)
    s.circle(kx, ky, 9, fill=t["arc_accent"], outline=0xFFFFFF, width=2)

    s.text(240, 150, f"{target:.0f}°", "nunito", 72, 0xFFFFFF, anchor="mm")
    s.glyph(240 - 46, 218, "thermometer", 22, 0x9BA2BC, anchor="rm")
    s.text(240 - 34, 218, "COOLING", "nunito", 18, 0x9BA2BC, anchor="rm")

    # −/+ steppers (62x62 at top_mid x∓150, y132)
    for x_center, sym in ((90, "−"), (390, "+")):
        box = (x_center - 31, 132, x_center + 31, 194)
        if theme in ("modern", "daylight"):
            tile(s, box, theme, False, radius=t["step_radius"],
                 glow=(0x4A5468, 0x9BA2BC) if theme == "modern" else None)
            if theme == "daylight":
                s.rrect(box, t["step_radius"], outline=0x4A5468, width=1)
        else:
            s.rrect(box, t["step_radius"], fill=t["step_bg"])
        s.text(x_center, 163, sym, "nunito", 36, 0xFFFFFF, anchor="mm")

    # two rows of 4 state buttons (108x86, row y 294 and 388)
    titles = [("Power", "power", "ON"), ("Mode", "snowflake", "COOL"),
              ("Fan", "fan", "AUTO"), ("Swing", "swap", "OFF"),
              ("Eco", "leaf", "OFF"), ("Sleep", "moon", "OFF"),
              ("Turbo", "rocket", "OFF"), ("Preset", "account", "NORMAL")]
    for i, (title, icon, label) in enumerate(titles):
        row, col = divmod(i, 4)
        x = 12 + col * 116
        y = 294 + row * 94
        box = (x, y, x + 108, y + 86)
        active_fill = None
        if title == "Power":
            active_fill = (t["power_on"], t["power_text"])
        elif title == "Mode":
            active_fill = (t["mode_cool"], t["mode_text"])
        title_c = 0xB4B8BC if theme == "daylight" else 0xBBBBBB
        if active_fill:
            if theme in ("modern",):
                glow_map = {"Power": (0x69F0AE, 0x00E676),
                            "Mode": (0x81D4FA, 0x29B6F6)}
                gb, gc = glow_map[title]
                tile(s, box, theme, False, radius=t["ac_radius"], glow=(gb, gc))
                s.rrect(box, t["ac_radius"], fill=active_fill[0])
                s.rrect(box, t["ac_radius"], outline=gb, width=2)
            elif theme == "daylight":
                s.shadow(box, t["ac_radius"], 0.5, 5, 4)
                s.rrect(box, t["ac_radius"], fill=active_fill[0])
                s.rrect(box, t["ac_radius"], outline=0x242A33, width=1)
            else:
                s.rrect(box, t["ac_radius"], fill=active_fill[0])
            icon_c = label_c = active_fill[1]
        else:
            tile(s, box, theme, False, radius=t["ac_radius"])
            if theme == "daylight":
                s.rrect(box, t["ac_radius"], outline=0x242A33, width=1)
            icon_c = label_c = 0xFFFFFF
        cx = (box[0] + box[2]) / 2
        s.text(cx, box[1] + 8, title, "nunito", 14, title_c, anchor="ma")
        s.glyph(cx, box[1] + 36, icon, 22, icon_c, anchor="mm")
        s.text(cx, box[1] + 60, label, "nunito", 18, label_c, anchor="ma")
    return s


def settings_screen(theme: str, out_px=480, k=3, active_theme=None) -> Screen:
    t = THEMES[theme]
    s = Screen(out_px, k, bg=t["settings_bg"])
    active_theme = active_theme or theme

    def row_bg(box):
        if theme == "daylight":
            s.shadow(box, t["row_radius"], 0.20, 3, 2)
            s.rrect(box, t["row_radius"], fill=t["row_bg"],
                    outline=t.get("row_border", 0x2E3542), width=1)
        else:
            s.rrect(box, t["row_radius"], fill=t["row_bg"])

    def hslider(x, y, w, h, frac, indicator, knob=0xFFFFFF):
        s.rrect((x, y, x + w, y + h), h / 2, fill=t["track"])
        s.rrect((x, y, x + w * frac, y + h), h / 2, fill=indicator)
        s.circle(x + w * frac, y + h / 2, h / 2 + 1, fill=knob)

    def sel_button(x, y, w, h, label, active):
        box = (x, y, x + w, y + h)
        if active:
            if theme == "modern":
                s.glow(box, 10, 0xFF8C00, 0.6, 7)
                s.rrect(box, 10, fill=t["sel_active"], outline=0xFFB74D, width=2)
            else:
                s.rrect(box, 10 if theme != "performance" else 4,
                        fill=t["sel_active"])
        else:
            r = 10 if theme != "performance" else 4
            if theme == "modern":
                s.shadow(box, r, 0.4, 4, 3)
                s.vgrad(box, r, t["grad_top"], t["grad_bottom"])
                s.rrect(box, r, outline=t["bevel"], width=1)
            else:
                s.rrect(box, r, fill=t["sel_inactive"])
        s.text(x + w / 2, y + h / 2, label, "nunito", 14,
               0xFFFFFF if active else 0xCCCCCC, anchor="mm")

    # header bar 460x44 at y6 (row_bg colour after apply_settings_theme)
    row_bg((10, 6, 470, 50))
    s.rrect((16, 10, 72, 46), 10 if theme != "performance" else 4,
            fill=t["sel_inactive"] if theme != "daylight" else 0x22262E)
    if theme == "daylight":
        s.rrect((16, 10, 72, 46), 10, outline=0x2E3542, width=1)
    s.glyph(44, 28, "arrow_left", 22, 0xFFFFFF, anchor="mm")
    s.text(240, 28, "Settings", "nunito", 24, 0xFFFFFF, anchor="mm")

    # Row: Brightness mode
    row_bg((10, 56, 470, 98))
    s.text(22, 77, "Mode", "nunito", 14, t["label"], anchor="lm")
    for i, (lbl, act) in enumerate([("Day", True), ("Eve", False), ("Night", False)]):
        sel_button(170 + i * 98, 62, 90, 30, lbl, act)

    # Rows: brightness sliders
    for i, (lbl, frac) in enumerate([("Day · 100%", 1.0), ("Eve · 50%", 0.5),
                                     ("Night · 35%", 0.35)]):
        y = 103 + i * 43
        row_bg((10, y, 470, y + 38))
        s.text(22, y + 19, lbl, "nunito", 14, t["value"], anchor="lm")
        hslider(170, y + 13, 296, 12, frac, t["accent"], t["knob"])
        s.text(462, y + 19, lbl.split("·")[1].strip(), "nunito", 14,
               t["value"], anchor="rm")

    # Row: timeout + saver
    y = 232
    row_bg((10, y, 470, y + 42))
    s.text(22, y + 21, "Timeout · 30s", "nunito", 14, t["value"], anchor="lm")
    hslider(170, y + 16, 160, 10, 0.1, t["timeout"], t["knob"])
    s.text(318, y + 21, "Saver", "nunito", 14, 0x888888, anchor="lm")
    sw_x, sw_y = 380, y + 11
    s.rrect((sw_x, sw_y, sw_x + 40, sw_y + 20), 10, fill=t["sel_inactive"])
    s.rrect((sw_x + 20, sw_y, sw_x + 40, sw_y + 20), 10, fill=0x4CAF50)
    s.circle(sw_x + 30, sw_y + 10, 8, fill=0xFFFFFF)

    # Row: theme selector (4 buttons)
    y = 279
    row_bg((10, y, 470, y + 46))
    s.text(22, y + 23, "Theme", "nunito", 14, t["label"], anchor="lm")
    themes = [("Classic", "classic"), ("Modern", "modern"),
              ("Perf", "performance"), ("Day", "daylight")]
    for i, (lbl, key) in enumerate(themes):
        sel_button(83 + i * 96, y + 7, 91, 32, lbl, key == active_theme)

    # Row: rotation
    y = 330
    row_bg((10, y, 470, y + 46))
    s.text(22, y + 23, "Rotate", "nunito", 14, t["label"], anchor="lm")
    for i, lbl in enumerate(["0°", "90°", "180°", "270°"]):
        sel_button(170 + i * 75, y + 7, 70, 32, lbl, i == 0)

    # Row: screensaver language (pages/settings.yaml settings_row_lang)
    y = 381
    row_bg((10, y, 470, y + 42))
    s.text(22, y + 21, "Saver lang", "nunito", 14, t["label"], anchor="lm")
    sel_button(131, y + 5, 165, 32, "Georgian", True)
    sel_button(300, y + 5, 165, 32, "English", False)

    # bottom buttons
    s.rrect((10, 438, 110, 474), 10 if theme != "performance" else 4, fill=0xFF6600)
    s.text(60, 456, "Home", "nunito", 18, 0xFFFFFF, anchor="mm")
    info_bg = 0x22262E if theme == "daylight" else (
        0x1A1A1A if theme == "performance" else 0x3A4352)
    s.rrect((370, 438, 470, 474), 10 if theme != "performance" else 4, fill=info_bg)
    if theme == "daylight":
        s.rrect((370, 438, 470, 474), 10, outline=0x2E3542, width=1)
    s.text(420, 456, "Info", "nunito", 18, 0xFFFFFF, anchor="mm")
    return s


def light_screen(out_px=480, k=3) -> Screen:
    """WLED / Bed LEDs light page (pages/light_color.yaml, Modern palette)."""
    s = Screen(out_px, k, bg=0x0F141E)
    s.text(240, 29, "Bed LEDs", "nunito", 24, 0xFFFFFF, anchor="mm")

    def vslider(cx, cy_top, frac, indicator, value_label):
        x0, x1 = cx - 17, cx + 17
        y0, y1 = cy_top, cy_top + 218
        s.rrect((x0, y0, x1, y1), 17, fill=0x0F141E,
                outline=0x242A33, width=1)
        s.shadow((x0, y0, x1, y1), 17, 0.35, 4, 3)
        s.rrect((x0, y0, x1, y1), 17, fill=0x0F141E)
        # indicator grows from bottom
        fy = y0 + 218 * (1 - frac)
        s.rrect((x0 + 1, fy, x1 - 1, y1 - 1), 15, fill=indicator)
        s.circle(cx, fy, 12, fill=0xFFB74D, outline=0xFFFFFF, width=2)
        return fy

    # left column: Brightness (panel 66x300 centered at x54, y258)
    s.text(54, 120, "Brightness", "nunito", 14, 0x9BA2BC, anchor="mm")
    vslider(54, 145, 0.5, 0xFF8C00, None)
    s.text(54, 392, "50%", "nunito", 14, 0xCCCCCC, anchor="mm")

    # second column: Saturation
    s.text(136, 120, "Saturation", "nunito", 14, 0x9BA2BC, anchor="mm")
    vslider(136, 145, 0.4, 0xFF1744, None)
    s.text(136, 392, "40%", "nunito", 14, 0xCCCCCC, anchor="mm")

    # hue ring: 12 segments, 250x250 centered (320, 226), width 32
    segs = [
        (227, 245, 0xFF4000), (250, 268, 0xFF8000), (272, 290, 0xBFFF00),
        (295, 313, 0x40FF00), (317, 335, 0x00FFBF), (340, 358, 0x00FF40),
        (2, 20, 0x00BFFF), (25, 43, 0x0040FF), (47, 65, 0xBF00FF),
        (70, 88, 0x4000FF), (92, 110, 0xFF00BF), (115, 133, 0xFF0040),
    ]
    for a0, a1, color in segs:
        s.arc((195, 101, 445, 351), a0, a1, color, 32)

    # bulb: glowing disc (recolored live) + bulb image, concentric with ring
    s.glow((278, 184, 362, 268), 42, 0xFF8C00, 0.55, 8)
    s.circle(320, 226, 42, fill=0xFF8C00)
    bulb = Image.open(ASSETS / "images" / "light" / "lightbulb.png").convert("RGBA")
    s.paste_image(bulb, 320, 226, 80, 80)
    return s


def screensaver_screen(out_px=480, k=3) -> Screen:
    s = Screen(out_px, k, bg=0x000000)
    bg = Image.open(ASSETS / "bg" / "bg1.jpg").convert("RGB")
    bg = bg.resize((s.size, s.size), Image.LANCZOS)
    s.img.paste(bg, (0, 0))
    # readability scrim (device shows the photo directly; slight dim keeps
    # the white clock legible in the mockup)
    scrim = Image.new("RGBA", s.img.size, (0, 0, 0, int(255 * 0.45)))
    s.img.paste(scrim, (0, 0), scrim)
    s.draw = ImageDraw.Draw(s.img, "RGBA")

    s.text(240, 24, "21:47", "bold", 148, 0xFFFFFF, anchor="ma")
    s.text(240, 214, "ორშაბათი, 21 სექტემბერი", "geo", 32, 0xFFFFFF, anchor="ma")

    s.text(28, 330, "24°", "bold", 96, 0xFFFFFF, anchor="lm")
    sunny = Image.open(ASSETS / "weather" / "sunny.png").convert("RGBA")
    s.paste_image(sunny, 240, 371, 110, 110)
    s.text(452, 344, "48%", "bold", 28, 0xFFFFFF, anchor="ra")
    s.text(452, 380, "8 km/h", "bold", 24, 0xCCCCCC, anchor="ra")
    return s


def info_screen(out_px=480, k=3) -> Screen:
    s = Screen(out_px, k, bg=0x0F141E)

    s.rrect((12, 10, 468, 50), 10, fill=0x1E2530)
    s.text(26, 30, "Device display01", "nunito", 24, 0xFFFFFF, anchor="lm")
    s.text(454, 30, "ESPHome 2.3", "nunito", 24, 0x9BA2BC, anchor="rm")

    rows = [
        ("Build", "2026.9.0"),
        ("Uptime", "1d 04h 23m"),
        ("WiFi", "OspreyNet"),
        ("IP", "192.168.1.84"),
        ("MAC", "7C:DF:A1:E2:3B:94"),
        ("Signal", "-48 dBm"),
        ("CPU", "34%"),
        ("Heap", "148 KB"),
        ("PSRAM", "7.6 MB"),
        ("HA Connection", "● Connected"),
    ]
    y = 58
    for i, (key, value) in enumerate(rows):
        bg = 0x1E2530 if i % 2 == 0 else 0x151A24
        s.rrect((12, y, 468, y + 32), 8, fill=bg)
        s.text(26, y + 16, key, "nunito", 20, 0x8891A0, anchor="lm")
        color = 0x4CAF50 if key == "HA Connection" else 0xFFFFFF
        s.text(454, y + 16, value, "nunito", 20, color, anchor="rm")
        y += 35

    # bottom actions: Restart + Home (224x44, space_between, y426)
    s.rrect((12, 426, 236, 470), 10, fill=0x2A3142)
    s.glyph(88, 448, "restart", 22, 0xFFFFFF, anchor="rm")
    s.text(98, 448, "Restart", "nunito", 20, 0xFFFFFF, anchor="lm")
    s.rrect((244, 426, 468, 470), 10, fill=0xFF6600)
    s.glyph(320, 448, "home", 22, 0xFFFFFF, anchor="rm")
    s.text(330, 448, "Home", "nunito", 20, 0xFFFFFF, anchor="lm")
    return s


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    for theme in ("classic", "modern", "performance", "daylight"):
        home_screen(theme).save(OUT / f"theme_{theme}_home.png")
        ac_screen(theme).save(OUT / f"theme_{theme}_ac.png")
        settings_screen(theme).save(OUT / f"theme_{theme}_settings.png")

    # general screens (Modern is the default showcase)
    ac_screen("modern").save(OUT / "screen_ac.png")
    settings_screen("modern").save(OUT / "screen_settings.png")
    light_screen().save(OUT / "screen_light.png")
    screensaver_screen().save(OUT / "screen_screensaver.png")
    info_screen().save(OUT / "screen_info.png")

    # hi-res home previews (960x960)
    for theme, name in (("classic", "preview_classic_v2_home"),
                        ("modern", "preview_modern_v2_home"),
                        ("performance", "preview_performance_v2_home"),
                        ("daylight", "preview_daylight_home")):
        home_screen(theme, out_px=960, k=2).save(OUT / f"{name}.png")

    # theme preview sheet: 2x2 grid (1008x1008)
    sheet = Image.new("RGB", (1008, 1008), hx(0x0A0A0C))
    cells = [("classic", 0, 0), ("modern", 1, 0),
             ("performance", 0, 1), ("daylight", 1, 1)]
    for theme, cx, cy in cells:
        img = home_screen(theme, out_px=480, k=3).img.resize(
            (480, 480), Image.LANCZOS)
        sheet.paste(img, (12 + cx * 504, 12 + cy * 504))
    OUT.mkdir(parents=True, exist_ok=True)
    sheet.save(OUT / "theme_preview_sheet.png")
    print(f"wrote docs/images/theme_preview_sheet.png  (1008x1008)")
    print("\nDone — all screenshots regenerated in", OUT)


if __name__ == "__main__":
    main()
