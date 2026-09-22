#!/usr/bin/env python3
"""Generate hardware/PINOUT.xlsx — ESP32-S3 used-vs-free pinout as a real Excel sheet.

Columns: GPIO | Used? | Where connected | For what | My mapping (OspreyPi
firmware) | Official docs (vendor) | Notes. Plus a Connectors sheet (P1, U9,
USB-C, FPC1, BAT) and a Readme sheet with sources.

Regenerate after any pinout change:
    pip install openpyxl
    python3 tools/generate_pinout_xlsx.py
"""
from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

OUT = Path(__file__).resolve().parent.parent / "hardware" / "PINOUT.xlsx"

HEADER_FILL = PatternFill("solid", fgColor="1F4E79")
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11)
TITLE_FONT = Font(bold=True, size=14, color="1F4E79")
SUB_FONT = Font(size=11, color="404040")
LINK_FONT = Font(size=11, color="0563C1", underline="single")
THIN = Side(style="thin", color="B0B0B0")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
WRAP = Alignment(vertical="center", wrap_text=True)
WRAP_TOP = Alignment(vertical="top", wrap_text=True)
CENTER = Alignment(vertical="center", horizontal="center", wrap_text=True)

# Status -> cell fill
STATUS_FILL = {
    "Used": PatternFill("solid", fgColor="FCE4E4"),      # light red
    "Shared": PatternFill("solid", fgColor="FFF2CC"),    # light yellow
    "Free": PatternFill("solid", fgColor="D9EAD3"),      # light green
    "Reserved": PatternFill("solid", fgColor="D9D9D9"),  # grey
}

# (GPIO, Used?, Where connected, For what, My mapping, Official docs, Notes)
ROWS = [
    ("0", "Used", "LCD FPC pin 17 (DB1) + BOOT circuit (CH340K auto-download)",
     "LCD blue B0 + boot strapping", "display.data_pins.blue[0]",
     "IO0/DB1 · EXAMPLE_LCD_IO_RGB_DATA0 (Box_rev2 main.c)",
     "Strapping: must be HIGH/floating at reset (panel is input-only, safe). Do not add pulls/loads."),
    ("1", "Shared", "SP3485 DE + #RE via SN74HC14 inverter (R21 470\u03a9 pull-up)",
     "RS485 TX", "Unused (no uart: enabled)",
     "IO1/485_TX (MCU sheet)",
     "TX-low-drive scheme: reusing as GPIO output makes the 485 bus chatter on A/B."),
    ("2", "Shared", "SP3485 RO via SN74HC14 double-inverter (non-inverting buffer)",
     "RS485 RX", "Unused (no uart: enabled)",
     "IO2/485_RX (MCU sheet)",
     "INPUT ONLY - driven by a buffer output. Never configure as output."),
    ("3", "Used", "LCD FPC pin 23 (DB7)", "LCD green G1",
     "display.data_pins.green[1]", "IO3/DB7 · DATA6",
     "Strapping: must float at reset (panel is input-only, safe)."),
    ("4", "Shared", "FT6336U SCL + U9 sensor header pin 4 (R35 4.7k\u03a9 pull-up)",
     "Touch clock + I2C sensor bus", "i2c.scl (bus_a, 400 kHz)",
     "IO4/I2C-SCL · EXAMPLE_TOUCH_I2C_SCL",
     "Shared bus: touch addr 0x38. Hang extra 3.3 V I2C devices on U9."),
    ("5", "Shared", "FT6336U SDA + U9 sensor header pin 3 (R34 4.7k\u03a9 pull-up)",
     "Touch data + I2C sensor bus", "i2c.sda (bus_a)",
     "IO5/I2C-SDA · EXAMPLE_TOUCH_I2C_SDA",
     "Same as GPIO4."),
    ("6", "Used", "LCD FPC pin 33 (DB17)", "LCD red R4",
     "display.data_pins.red[4]", "IO6/DB17 · DATA15", ""),
    ("7", "Used", "LCD FPC pin 32 (DB16)", "LCD red R3",
     "display.data_pins.red[3]", "IO7/DB16 · DATA14", ""),
    ("8", "Used", "LCD FPC pin 26 (DB10)", "LCD green G4",
     "display.data_pins.green[4]", "IO8/DB10 · DATA9", ""),
    ("9", "Used", "LCD FPC pin 21 (DB5)", "LCD blue B4",
     "display.data_pins.blue[4]", "IO9/DB5 · DATA4", ""),
    ("10", "Used", "LCD FPC pin 20 (DB4)", "LCD blue B3",
     "display.data_pins.blue[3]", "IO10/DB4 · DATA3", ""),
    ("11", "Used", "LCD FPC pin 19 (DB3)", "LCD blue B2",
     "display.data_pins.blue[2]", "IO11/DB3 · DATA2", ""),
    ("12", "Used", "LCD FPC pin 18 (DB2)", "LCD blue B1",
     "display.data_pins.blue[1]", "IO12/DB2 · DATA1", ""),
    ("13", "Used", "SY7200 boost EN/PWM (R13 10k\u03a9 pull-down)",
     "Backlight brightness PWM", "ledc gpio_backlight_pwm 1 kHz \u2192 light.display_backlight",
     "IO13/LCD_BK · EXAMPLE_PIN_NUM_BK_LIGHT",
     "Active HIGH. Backlight is OFF at boot until firmware drives it."),
    ("14", "Used", "LCD FPC pin 15", "HSYNC (horizontal sync)",
     "display.hsync_pin", "IO14/HSYNC", ""),
    ("15", "Used", "LCD FPC pin 31 (DB15)", "LCD red R2",
     "display.data_pins.red[2]", "IO15/DB15 · DATA13", ""),
    ("16", "Used", "LCD FPC pin 30 (DB14)", "LCD red R1",
     "display.data_pins.red[1]", "IO16/DB14 · DATA12", ""),
    ("17", "Used", "LCD FPC pin 29 (DB13)", "LCD red R0",
     "display.data_pins.red[0]", "IO17/DB13 · DATA11", ""),
    ("18", "Used", "LCD FPC pin 27 (DB11)", "LCD green G5",
     "display.data_pins.green[5]", "IO18/DB11 · DATA10", ""),
    ("19", "Used", "LCD FPC pin 25 (DB9)", "LCD green G3",
     "display.data_pins.green[3]", "IO19/DB9 · DATA8",
     "Native USB D- unavailable (pin used by LCD) - USB works via CH340K only."),
    ("20", "Used", "LCD FPC pin 24 (DB8)", "LCD green G2",
     "display.data_pins.green[2]", "IO20/DB8 · DATA7",
     "Native USB D+ unavailable (same reason)."),
    ("21", "Used", "LCD FPC pin 14", "VSYNC (vertical sync)",
     "display.vsync_pin", "IO21/VSYNC", ""),
    ("22-25", "Reserved", "- (these GPIOs do not exist on ESP32-S3)", "-",
     "-", "- (absent from schematic)", "Do not use."),
    ("26-32", "Reserved", "In-package SPI Flash/PSRAM bus - no module pads", "-",
     "-", "-", "NEVER touch."),
    ("33, 34", "Reserved", "Octal SPIIO4/5 - exist on bare chip, no WROOM-1 pads", "-",
     "-", "-", "Unusable on this module."),
    ("35-37", "Reserved", "Octal SPIIO6/7 + SPIDQS \u2192 module 16 MB Flash / 8 MB PSRAM", "-",
     "-", "-", "RESERVED on all N16R8 (R8 = octal) modules."),
    ("38", "Used", "LCD FPC pin 10", "3-wire SPI clock (ST7701S init)",
     "spi.clk_pin (lcd_spi)", "IO38/SCLK · EXAMPLE_LCD_IO_SPI_SCL", ""),
    ("39", "Used", "LCD FPC pin 9", "3-wire SPI data",
     "spi.mosi_pin (lcd_spi)", "IO39/MOSI · EXAMPLE_LCD_IO_SPI_SDA", ""),
    ("40", "Free", "NOT CONNECTED (module pad exists, no PCB net)", "- free for user -",
     "-", "IO40 (no net on MCU sheet)",
     "Solder a wire to the module pad. Digital I/O, ADC2, LEDC PWM, PCNT. Sits near the antenna - keep wires short."),
    ("41", "Free", "NOT CONNECTED (module pad exists, no PCB net)", "- free for user -",
     "-", "IO41 (no net on MCU sheet)", "Same as GPIO40."),
    ("42", "Used", "AO3400 MOSFET gate (R29 100\u03a9, R30 10k\u03a9 pull-down) \u2192 buzzer 2700 Hz",
     "Buzzer drive", "ledc buzzer_output 1 kHz",
     "IO42/BUZZER (MCU sheet)", "Active HIGH, passive element."),
    ("43", "Used", "CH340K RXD (R9 470\u03a9)", "USB serial TX (flashing + logs)",
     "UART0 TX (logger baud_rate: 0)", "MCU_TXD / TXD0",
     "Keep for flashing. Do not reuse."),
    ("44", "Used", "CH340K TXD", "USB serial RX",
     "UART0 RX", "MCU_RXD / RXD0",
     "INPUT ONLY - CH340K output drives this pin. Never drive as output."),
    ("45", "Used", "LCD FPC pin 11", "3-wire SPI chip-select",
     "display.cs_pin (ignore_strapping_warning: true)",
     "IO45/CS · EXAMPLE_LCD_IO_SPI_CS",
     "Strapping (VDD_SPI 3.3 V select): floats as input at reset, driven after boot."),
    ("46", "Used", "LCD FPC pin 22 (DB6)", "LCD green G0",
     "display.data_pins.green[0]", "IO46/DB6 · DATA5",
     "Strapping (ROM boot messages): floats at reset, driven after boot."),
    ("47", "Used", "LCD FPC pin 13", "DE (data enable)",
     "display.de_pin", "IO47/DE", ""),
    ("48", "Used", "LCD FPC pin 12", "Pixel clock 16 MHz",
     "display.pclk_pin", "IO48/PCLK", ""),
]

CONNECTORS = [
    ("P1 - 5.08 mm 4-pin terminal (power + RS485)", [
        ("Pin", "Net", "Description"),
        ("1", "VCC", "12-24 VDC in (abs. max 28.5 V) \u2192 SGM6132 DCDC \u2192 5 V / 3 A"),
        ("2", "GND", "Ground"),
        ("3", "RS485_A", "RS485 bus A (non-inverting)"),
        ("4", "RS485_B", "RS485 bus B (inverting)"),
        ("-", "Protection", "120 \u03a9 termination R23, 10 k\u03a9 fail-safe bias (R20\u2192GND on B, R27\u21923V3 on A), TVS D5/D6, 10 \u03a9 series R22/R24"),
    ]),
    ("U9 - MX1.25 4-pin wafer (I2C sensor header)", [
        ("Pin", "Net", "Description"),
        ("1", "+3.3V", "Sensor power (AMS1117 1 A rail)"),
        ("2", "GND", "Ground"),
        ("3", "IO5 / I2C-SDA", "Shared with FT6336 touch (4.7 k\u03a9 pull-up), addr 0x38"),
        ("4", "IO4 / I2C-SCL", "Shared with FT6336 touch (4.7 k\u03a9 pull-up)"),
        ("-", "Note", "Verify pin order against PCB silkscreen before connecting"),
    ]),
    ("USB-C (TYPEC-302) - flashing + serial logs via CH340K", [
        ("Signal", "Net", "Description"),
        ("DP/DM", "SERIAL_DP/DM", "USB 2.0 \u2192 CH340K (USBLC6 ESD protection), up to ~2 Mbaud"),
        ("VBUS", "5 V", "Main power input"),
        ("CC", "5.1 k\u03a9", "CC pull-downs R31/R32"),
        ("DTR/RTS", "EN + IO0", "Auto-download circuit (L8050 transistors) - no boot buttons needed"),
        ("-", "Note", "ESP32-S3 native USB unusable (GPIO19/20 are LCD data) - serial bridge is the only USB function"),
    ]),
    ("FPC1 - 0.5 mm 40-pin LCD connector (FPC-05FB-40PH20)", [
        ("FPC pin", "Net", "Description"),
        ("1", "GND", "Shield"),
        ("2", "LEDA", "Backlight anode (SY7200 boost)"),
        ("3", "LEDK", "Backlight cathode"),
        ("4", "GND", ""),
        ("5", "+3.3V", ""),
        ("6", "CHIP_PU", "System EN - panel reset follows system reset, no GPIO needed"),
        ("7, 8", "NC", ""),
        ("9", "IO39/MOSI", "SPI init data"),
        ("10", "IO38/SCLK", "SPI init clock"),
        ("11", "IO45/CS", "SPI chip-select"),
        ("12", "IO48/PCLK", "Pixel clock"),
        ("13", "IO47/DE", "Data enable"),
        ("14", "IO21/VSYNC", ""),
        ("15", "IO14/HSYNC", ""),
        ("16", "NC", ""),
        ("17", "IO0/DB1 (B0)", "Blue 0"),
        ("18", "IO12/DB2 (B1)", ""),
        ("19", "IO11/DB3 (B2)", ""),
        ("20", "IO10/DB4 (B3)", ""),
        ("21", "IO9/DB5 (B4)", ""),
        ("22", "IO46/DB6 (G0)", "Green 0"),
        ("23", "IO3/DB7 (G1)", ""),
        ("24", "IO20/DB8 (G2)", ""),
        ("25", "IO19/DB9 (G3)", ""),
        ("26", "IO8/DB10 (G4)", ""),
        ("27", "IO18/DB11 (G5)", ""),
        ("28", "NC", "DB12 skipped \u2192 16-bit mode"),
        ("29", "IO17/DB13 (R0)", "Red 0"),
        ("30", "IO16/DB14 (R1)", ""),
        ("31", "IO15/DB15 (R2)", ""),
        ("32", "IO7/DB16 (R3)", ""),
        ("33", "IO6/DB17 (R4)", ""),
        ("34", "GND", ""),
        ("35", "TP-INT", "Touch interrupt - 2 k\u03a9 pull-up only, NOT routed to MCU"),
        ("36", "IO5/I2C-SDA", "Touch data"),
        ("37", "IO4/I2C-SCL", "Touch clock"),
        ("38", "CHIP_PU", "System EN"),
        ("39", "+3.3V", ""),
        ("40", "GND", ""),
        ("41, 42", "GND", "Shield"),
    ]),
    ("BAT+ / BAT- - Li-ion pads (no connector fitted)", [
        ("Pad", "Net", "Description"),
        ("BAT+", "BAT+", "Single-cell Li-ion \u2192 IP5306 charge 2.1 A / boost-discharge 2.4 A"),
        ("BAT-", "GND", "Ground"),
    ]),
]


def style_header(ws, row: int, ncols: int) -> None:
    for col in range(1, ncols + 1):
        c = ws.cell(row=row, column=col)
        c.fill = HEADER_FILL
        c.font = HEADER_FONT
        c.alignment = CENTER
        c.border = BORDER


def main() -> None:
    wb = Workbook()

    # ---- Sheet 1: Readme ----
    ws = wb.active
    ws.title = "Readme"
    ws.sheet_properties.tabColor = "1F4E79"
    ws["A1"] = "ESP32-S3 Pinout - OspreyPi / Osptek ESP32-S3-Touch-LCD-4 (ESP32-TPCB4)"
    ws["A1"].font = TITLE_FONT
    lines = [
        "Module: ESP32-S3-WROOM-1-N16R8 (16 MB Flash + 8 MB octal PSRAM) - "
        "3.95\" 480x480 ST7701S + FT6336U touch.",
        "",
        "Sheets: Pinout = every GPIO (used vs free) - Columns = pin, status,",
        "where it is connected, what it is for, MY mapping (this OspreyPi firmware),",
        "OFFICIAL docs (vendor schematic + IDF example). Connectors = P1 / U9 /",
        "USB-C / FPC1 / BAT pinouts.",
        "",
        "Bottom line: the only truly FREE pins are GPIO40 + GPIO41 (solder-only).",
        "Best expansion: I2C sensor header GPIO4/5 (shared with touch).",
        "GPIO1/2 are RS485-wired but unused by this firmware.",
        "",
        "Sources: vendor schematic R2 2025-02-05, MCU-sheet excerpt, vendor IDF",
        "example ESP32S3_3.95In_Box_rev2, this repo hardware/PINOUT.md.",
        "Official vendor repo: https://github.com/osptek/esp32-s3-touch-lcd-4",
        "(board folder versions/ESP32-S3-Touch-LCD-4).",
        "",
        "Regenerate: python3 tools/generate_pinout_xlsx.py  (needs: pip install openpyxl)",
    ]
    for i, line in enumerate(lines, start=3):
        cell = ws.cell(row=i, column=1, value=line)
        cell.font = SUB_FONT
        if line.startswith("Official vendor repo:"):
            cell.hyperlink = "https://github.com/osptek/esp32-s3-touch-lcd-4"
            cell.font = LINK_FONT
    ws.column_dimensions["A"].width = 95
    for i in range(3, 3 + len(lines)):
        ws.row_dimensions[i].height = 16

    # ---- Sheet 2: Pinout ----
    ws = wb.create_sheet("Pinout")
    ws.sheet_properties.tabColor = "70AD47"
    headers = ["GPIO", "Used?", "Where connected", "For what",
               "My mapping (OspreyPi firmware)", "Official docs (vendor)", "Notes"]
    widths = [10, 12, 52, 36, 44, 44, 62]
    for col, (h, w) in enumerate(zip(headers, widths), start=1):
        ws.cell(row=1, column=col, value=h)
        ws.column_dimensions[get_column_letter(col)].width = w
    style_header(ws, 1, len(headers))
    for r, row in enumerate(ROWS, start=2):
        for col, val in enumerate(row, start=1):
            cell = ws.cell(row=r, column=col, value=val)
            cell.border = BORDER
            cell.alignment = CENTER if col <= 2 else WRAP_TOP
            cell.font = Font(bold=True, size=12) if col == 1 else Font(size=11)
            if col == 2 and val in STATUS_FILL:
                cell.fill = STATUS_FILL[val]
                cell.font = Font(bold=True, size=11)
        ws.row_dimensions[r].height = 30 if len(row[2] + row[6]) < 120 else 45
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}{len(ROWS) + 1}"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    # ---- Sheet 3: Connectors ----
    ws = wb.create_sheet("Connectors")
    ws.sheet_properties.tabColor = "ED7D31"
    for col, w in zip("ABC", (16, 30, 90)):
        ws.column_dimensions[col].width = w
    r = 1
    for title, table in CONNECTORS:
        ws.cell(row=r, column=1, value=title).font = Font(bold=True, size=12, color="1F4E79")
        r += 1
        for i, trow in enumerate(table):
            for col, val in enumerate(trow, start=1):
                cell = ws.cell(row=r, column=col, value=val)
                cell.border = BORDER
                if i == 0:
                    cell.fill = HEADER_FILL
                    cell.font = HEADER_FONT
                    cell.alignment = CENTER
                else:
                    cell.font = Font(size=11)
                    cell.alignment = CENTER if col == 1 else WRAP
            ws.row_dimensions[r].height = 18
            r += 1
        r += 1  # blank row between tables
    ws.freeze_panes = "A1"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    print(f"Wrote {OUT} ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
