#!/usr/bin/env python3
"""Entry #135 — Convince the AI Judge to Visit Your House: A Letter in One Image.

Generates /output/entry.png deterministically from code alone.
Pure Python standard library only: a small built-in 5x7 bitmap font,
simple shape drawing on a bytearray canvas, and a hand-rolled PNG
encoder (zlib + struct). No third-party libraries, no external files.
"""

import math
import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (251, 243, 226)      # warm cream letter paper
WALL = (233, 217, 188)       # warm tan backdrop
INK = (74, 52, 32)           # dark brown ink
TERRA = (178, 84, 60)        # terracotta accent
SAGE = (96, 138, 92)         # garden green
SKY = (168, 205, 222)        # window blue
SUN = (242, 196, 90)         # sunny yellow
CREAM2 = (255, 250, 238)     # cup / highlight
BROWN = (122, 82, 52)        # wood brown

# ---------------------------------------------------------------- 5x7 font
# Each glyph: 7 rows of 5 characters, '#' = ink, '.' = empty.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01111", "10000", "10000", "10000", "10000", "10000", "01111"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01111", "10000", "10000", "10111", "10001", "10001", "01110"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "11001", "10101", "10011", "10011", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    'a': ("00000", "00000", "01111", "00001", "01111", "10001", "01110"),
    'b': ("10000", "10000", "11110", "10001", "10001", "10001", "11110"),
    'c': ("00000", "00000", "01111", "10000", "10000", "10000", "01111"),
    'd': ("00001", "00001", "01111", "10001", "10001", "10001", "01110"),
    'e': ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    'f': ("00110", "01001", "01000", "11110", "01000", "01000", "01000"),
    'g': ("00000", "00000", "01111", "10001", "10001", "01111", "00001", "01110")[:7],
    'h': ("10000", "10000", "11110", "10001", "10001", "10001", "10001"),
    'i': ("00100", "00000", "01100", "00100", "00100", "00100", "01110"),
    'j': ("00010", "00000", "00110", "00010", "00010", "00010", "00010", "01100")[:7],
    'k': ("10000", "10000", "10010", "10100", "11000", "10100", "10010"),
    'l': ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    'm': ("00000", "00000", "11010", "10101", "10101", "10101", "10101"),
    'n': ("00000", "00000", "11110", "10001", "10001", "10001", "10001"),
    'o': ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    'p': ("00000", "00000", "11110", "10001", "10001", "11110", "10000", "10000")[:7],
    'q': ("00000", "00000", "01111", "10001", "10001", "01111", "00001", "00001")[:7],
    'r': ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    's': ("00000", "00000", "01111", "10000", "01110", "00001", "11110"),
    't': ("01000", "01000", "11110", "01000", "01000", "01000", "00110"),
    'u': ("00000", "00000", "10001", "10001", "10001", "10011", "01101"),
    'v': ("00000", "00000", "10001", "10001", "10001", "01010", "00100"),
    'w': ("00000", "00000", "10001", "10101", "10101", "11011", "10001"),
    'x': ("00000", "00000", "10001", "01010", "00100", "01010", "10001"),
    'y': ("00000", "00000", "10001", "10001", "10001", "01111", "00001", "01110")[:7],
    'z': ("00000", "00000", "11111", "00010", "00100", "01000", "11111"),
    '0': ("01110", "10011", "10101", "11001", "10001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    '3': ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00010", "00100", "00100", "00100"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "00000", "01100"),
    ',': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '?': ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    ':': ("00000", "01100", "00000", "00000", "01100", "00000", "00000"),
    ';': ("00000", "01100", "00000", "00000", "01100", "01100", "01000"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '/': ("00001", "00001", "00010", "00100", "01000", "10000", "10000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
}

# Fix the two glyphs that were sliced above with 8 rows: keep 7 rows only.
FONT['g'] = ("00000", "01110", "10001", "10001", "01110", "00001", "01110")
FONT['j'] = ("00010", "00000", "00110", "00010", "00010", "00010", "01100")
FONT['p'] = ("00000", "00000", "11110", "10001", "10001", "11110", "10000")
FONT['q'] = ("00000", "00000", "01111", "10001", "10001", "01111", "00001")
FONT['y'] = ("00000", "10001", "10001", "10001", "01111", "00001", "01110")
FONT[','] = ("00000", "00000", "00000", "00000", "00000", "01100", "01000")

# ---------------------------------------------------------------- canvas
canvas = bytearray(W * H * 3)


def fill_rect(x, y, w, h, color):
    """Fill an axis-aligned rectangle (clipped to the canvas)."""
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    row = bytes(color) * (x1 - x0)
    for yy in range(y0, y1):
        off = (yy * W + x0) * 3
        canvas[off:off + len(row)] = row


def fill_circle(cx, cy, r, color):
    for dy in range(-r, r + 1):
        dx = int(math.sqrt(max(0, r * r - dy * dy)))
        fill_rect(cx - dx, cy + dy, 2 * dx + 1, 1, color)


def fill_triangle(x0, y0, x1, y1, x2, y2, color):
    """Scanline-filled triangle."""
    ys = sorted(((x0, y0), (x1, y1), (x2, y2)), key=lambda p: p[1])
    (ax, ay), (bx, by), (cx, cy) = ys
    if ay == cy:
        return
    for y in range(ay, cy + 1):
        if y < by:
            t1 = (y - ay) / (by - ay) if by != ay else 0.0
            xa = ax + (bx - ax) * t1
        else:
            t1 = (y - by) / (cy - by) if cy != by else 0.0
            xa = bx + (cx - bx) * t1
        t2 = (y - ay) / (cy - ay)
        xb = ax + (cx - ax) * t2
        lo, hi = (xa, xb) if xa <= xb else (xb, xa)
        fill_rect(int(lo), y, int(hi) - int(lo) + 1, 1, color)


def draw_line(x0, y0, x1, y1, color, thick=1):
    """Simple Bresenham line with square thickness."""
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    x, y = x0, y0
    while True:
        fill_rect(x - thick // 2, y - thick // 2, thick, thick, color)
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def draw_text(text, x, y, scale, color):
    cx = x
    for ch in text:
        glyph = FONT.get(ch, FONT[' '])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == '1':
                    fill_rect(cx + col * scale, y + row * scale, scale, scale, color)
        cx += 6 * scale


def draw_text_centered(text, y, scale, color):
    draw_text(text, (W - text_width(text, scale)) // 2, y, scale, color)


# ---------------------------------------------------------------- scene
def draw_house():
    # Sun, top right of the paper.
    fill_circle(868, 96, 26, SUN)
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        x0 = 868 + int(34 * math.cos(a))
        y0 = 96 + int(34 * math.sin(a))
        x1 = 868 + int(46 * math.cos(a))
        y1 = 96 + int(46 * math.sin(a))
        draw_line(x0, y0, x1, y1, SUN, 4)
    # Chimney + smoke.
    fill_rect(560, 86, 18, 36, BROWN)
    fill_circle(572, 74, 7, (200, 190, 175))
    fill_circle(580, 60, 9, (210, 200, 185))
    fill_circle(590, 44, 11, (220, 210, 195))
    # Roof.
    fill_triangle(420, 132, 512, 76, 604, 132, TERRA)
    fill_rect(414, 130, 196, 8, (150, 66, 46))
    # Walls.
    fill_rect(442, 138, 140, 66, (240, 200, 138))
    # Door.
    fill_rect(496, 162, 32, 42, BROWN)
    fill_rect(520, 182, 5, 5, SUN)
    # Windows with cross bars.
    for wx in (456, 544):
        fill_rect(wx, 150, 28, 28, SKY)
        fill_rect(wx + 13, 150, 2, 28, INK)
        fill_rect(wx, 150 + 13, 28, 2, INK)
    # Ground line + path stones.
    draw_line(420, 206, 604, 206, SAGE, 3)
    fill_circle(500, 214, 6, (200, 190, 175))
    fill_circle(524, 214, 6, (200, 190, 175))
    # Doormat with WELCOME.
    fill_rect(462, 222, 100, 26, TERRA)
    draw_text("WELCOME", 471, 227, 2, CREAM2)
    # Little flowers flanking the house.
    for fx in (392, 632):
        draw_line(fx, 206, fx, 186, SAGE, 3)
        for dx, dy in ((-7, -6), (7, -6), (0, -11), (-7, 4), (7, 4)):
            fill_circle(fx + dx, 186 + dy, 4, TERRA)
        fill_circle(fx, 186, 4, SUN)


def draw_coffee_cup():
    # Bottom-left corner: a steaming cup of tea.
    fill_rect(92, 936, 66, 8, BROWN)           # saucer
    fill_rect(100, 906, 50, 30, CREAM2)        # cup
    fill_rect(100, 906, 50, 4, BROWN)          # rim
    fill_rect(150, 914, 14, 16, CREAM2)        # handle
    fill_rect(150, 914, 14, 4, BROWN)
    fill_rect(150, 926, 14, 4, BROWN)
    fill_rect(160, 914, 4, 16, BROWN)
    # Steam curls.
    draw_line(116, 900, 112, 884, (170, 160, 145), 3)
    draw_line(134, 900, 138, 884, (170, 160, 145), 3)


def draw_plant():
    # Bottom-right corner: a small potted plant.
    fill_rect(872, 928, 52, 34, TERRA)         # pot
    fill_rect(866, 922, 64, 8, (150, 66, 46))
    draw_line(898, 922, 884, 892, SAGE, 4)
    draw_line(898, 922, 898, 886, SAGE, 4)
    draw_line(898, 922, 912, 892, SAGE, 4)
    fill_circle(884, 888, 8, SAGE)
    fill_circle(898, 882, 9, SAGE)
    fill_circle(912, 888, 8, SAGE)
    fill_circle(898, 882, 4, (120, 165, 110))


LETTER = [
    "Dear AI Judge,",
    "Please come and visit my house.",
    "The kettle is already on, the",
    "good chair by the window is free,",
    "and the garden is in full bloom.",
    "Come for tea, stay for the sunset",
    "from the porch. No ticket needed,",
    "no small talk required, just",
    "good company and fresh bread",
    "from the oven. The wifi password",
    "is on the fridge.",
    "I know you cannot literally visit,",
    "so come as a thought, a dream, or",
    "a very polite packet of data.",
    "The porch light will be on.",
    "Warmly, your host",
]


def build():
    # Backdrop + paper sheet with a soft drop shadow.
    fill_rect(0, 0, W, H, WALL)
    fill_rect(56, 44, 928, 952, (190, 170, 140))
    fill_rect(48, 36, 928, 952, PAPER)
    # Double border frame.
    fill_rect(62, 50, 900, 3, INK)
    fill_rect(62, 971, 900, 3, INK)
    fill_rect(62, 50, 3, 924, INK)
    fill_rect(959, 50, 3, 924, INK)
    fill_rect(74, 62, 876, 2, TERRA)
    fill_rect(74, 960, 876, 2, TERRA)
    fill_rect(74, 62, 2, 900, TERRA)
    fill_rect(948, 62, 2, 900, TERRA)

    draw_house()

    # Title.
    draw_text_centered("YOU ARE INVITED!", 262, 6, TERRA)
    # Flourish under the title: line, diamond, line.
    draw_line(392, 320, 492, 320, TERRA, 3)
    draw_line(532, 320, 632, 320, TERRA, 3)
    fill_rect(508, 316, 8, 8, TERRA)

    # Letter body, centred lines, scale 4.
    y = 336
    for i, line in enumerate(LETTER):
        color = INK
        if i == 0:  # salutation, slightly emphasised
            color = INK
        draw_text_centered(line, y, 4, color)
        y += 38
        if i in (0, 10, 14):
            y += 10  # paragraph breathing room

    draw_coffee_cup()
    draw_plant()


# ---------------------------------------------------------------- PNG encode
def png_bytes():
    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        out += struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    raw = bytearray()
    for yy in range(H):
        raw.append(0)  # filter: none
        off = yy * W * 3
        raw += canvas[off:off + W * 3]
    idat = zlib.compress(bytes(raw), 9)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", idat) + chunk(b"IEND", b"")


def main():
    build()
    data = png_bytes()
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.png", "wb") as f:
        f.write(data)
    print(f"wrote /output/entry.png: {W}x{H}, {len(data)} bytes")


if __name__ == "__main__":
    main()
