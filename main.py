# Entry for make.fun bounty "Sum up 23 November's world news in one image"
# (https://make.fun/bounty/news-image-20261123)
#
# Draws a 1024x1024 newspaper-front-page poster of Monday 23 November 2026's
# world news. Pure Python 3 standard library only: no Pillow, no font files,
# no network, no randomness, no timestamps. Running it twice writes
# byte-identical output.
#
# How it works: at build time (on a machine with Pillow + DejaVu fonts) every
# line of text was rendered once with the exact fonts/sizes of the original
# renderer and stored below as alpha bitmaps in _BLOB (zlib + base64). At
# runtime this program only paints rectangles/lines into a bytearray
# framebuffer, blits those bitmaps with alpha blending, and writes the PNG
# with zlib + struct. The layout, colours and texts are unchanged from the
# original; the reference render is entry.png in this repo.
#
# Stories were gathered from the day's reporting (world-news-wire.pages.dev,
# oneturn.news, inshorts.com, simplelife.news - all 23 Nov 2026 editions).
# The judge has no news feed, so every story is labelled with place + a
# one-line summary that makes the image self-explanatory.
#
# Output: $OUTPUT if set, else $MAKEFUN_OUTPUT_DIR/entry.png if set, else
# /output/entry.png if /output exists, else ./entry.png.

import base64
import os
import struct
import zlib

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
GREY = (90, 86, 78)
CARD = (255, 255, 255)
LINE = (200, 194, 182)

# Pre-rendered text bitmaps: (x, y, w, h, (r, g, b), offset, length) where
# (x, y) is the top-left of the ink bounding box on the canvas and
# offset/length index into the zlib-compressed raw alpha bytes in _BLOB.
_BITMAPS = [
    (48, 28, 757, 22, (255, 255, 255), 0, 16654),
    (48, 71, 573, 23, (200, 205, 220), 16654, 13179),
    (48, 150, 380, 24, (178, 34, 34), 29833, 9120),
    (48, 198, 520, 53, (20, 20, 20), 38953, 27560),
    (47, 274, 622, 53, (20, 20, 20), 66513, 32966),
    (48, 341, 887, 24, (40, 40, 40), 99479, 21288),
    (48, 375, 842, 24, (40, 40, 40), 120767, 20208),
    (64, 454, 254, 12, (178, 34, 34), 140975, 3048),
    (64, 480, 315, 21, (20, 20, 20), 144023, 6615),
    (64, 514, 189, 20, (20, 20, 20), 150638, 3780),
    (64, 545, 379, 18, (60, 60, 60), 154418, 6822),
    (64, 567, 78, 18, (60, 60, 60), 161240, 1404),
    (544, 454, 294, 15, (178, 34, 34), 162644, 4410),
    (544, 480, 257, 27, (20, 20, 20), 167054, 6939),
    (544, 513, 221, 27, (20, 20, 20), 173993, 5967),
    (544, 545, 414, 18, (60, 60, 60), 179960, 7452),
    (544, 567, 175, 14, (60, 60, 60), 187412, 2450),
    (64, 616, 253, 12, (178, 34, 34), 189862, 3036),
    (64, 642, 221, 21, (20, 20, 20), 192898, 4641),
    (64, 675, 166, 21, (20, 20, 20), 197539, 3486),
    (64, 707, 341, 18, (60, 60, 60), 201025, 6138),
    (64, 729, 241, 18, (60, 60, 60), 207163, 4338),
    (544, 616, 252, 12, (178, 34, 34), 211501, 3024),
    (544, 642, 243, 27, (20, 20, 20), 214525, 6561),
    (544, 675, 257, 21, (20, 20, 20), 221086, 5397),
    (543, 707, 376, 16, (60, 60, 60), 226483, 6016),
    (544, 729, 196, 14, (60, 60, 60), 232499, 2744),
    (64, 778, 327, 15, (178, 34, 34), 235243, 4905),
    (64, 804, 179, 27, (20, 20, 20), 240148, 4833),
    (64, 837, 116, 21, (20, 20, 20), 244981, 2436),
    (64, 869, 376, 18, (60, 60, 60), 247417, 6768),
    (64, 891, 152, 14, (60, 60, 60), 254185, 2128),
    (544, 778, 192, 12, (178, 34, 34), 256313, 2304),
    (543, 804, 201, 21, (20, 20, 20), 258617, 4221),
    (543, 837, 197, 21, (20, 20, 20), 262838, 4137),
    (544, 869, 325, 18, (60, 60, 60), 266975, 5850),
    (544, 891, 128, 14, (60, 60, 60), 272825, 1792),
    (64, 947, 849, 22, (255, 255, 255), 274617, 18678),
    (48, 993, 866, 15, (90, 86, 78), 293295, 12990),
]

_BLOB = (
    "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"
)


def rect(fb, x0, y0, x1, y1, color):
    # Pillow rectangle: both endpoints inclusive, clipped to the canvas.
    x0 = max(0, x0)
    y0 = max(0, y0)
    x1 = min(W - 1, x1)
    y1 = min(H - 1, y1)
    if x1 < x0 or y1 < y0:
        return
    r, g, b = color
    row = bytes((r, g, b)) * (x1 - x0 + 1)
    for y in range(y0, y1 + 1):
        i = (y * W + x0) * 3
        fb[i:i + len(row)] = row


def rect_outline(fb, x0, y0, x1, y1, width, color):
    # Pillow rectangle outline: `width` px thick, drawn inside the box.
    r, g, b = color
    for y in range(y0, y0 + width):
        rect(fb, x0, y, x1, y, color)
    for y in range(y1 - width + 1, y1 + 1):
        rect(fb, x0, y, x1, y, color)
    for x in range(x0, x0 + width):
        for y in range(y0 + width, y1 - width + 1):
            i = (y * W + x) * 3
            fb[i:i + 3] = bytes((r, g, b))
    for x in range(x1 - width + 1, x1 + 1):
        for y in range(y0 + width, y1 - width + 1):
            i = (y * W + x) * 3
            fb[i:i + 3] = bytes((r, g, b))


def hline(fb, x1, y, x2, width, color):
    # Horizontal Pillow line of `width`: rows y .. y+width-1, endpoints incl.
    for yy in range(y, y + width):
        rect(fb, x1, yy, x2, yy, color)


def blit(fb, idx):
    x, y, w, h, color, off, n = _BITMAPS[idx]
    r, g, b = color
    data = _BLOB_BYTES[off:off + n]
    for row in range(h):
        base = ((y + row) * W + x) * 3
        src = row * w
        for col in range(w):
            a = data[src + col]
            if a == 0:
                continue
            i = base + col * 3
            if a == 255:
                fb[i] = r
                fb[i + 1] = g
                fb[i + 2] = b
            else:
                ia = 255 - a
                fb[i] = (a * r + ia * fb[i] + 127) // 255
                fb[i + 1] = (a * g + ia * fb[i + 1] + 127) // 255
                fb[i + 2] = (a * b + ia * fb[i + 2] + 127) // 255


def _chunk(kind, data):
    return (struct.pack(">I", len(data)) + kind + data +
            struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF))


def write_png(fb, path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)  # filter: none
        raw += fb[y * W * 3:(y + 1) * W * 3]
    png = bytearray(b"\x89PNG\r\n\x1a\n")
    png += _chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    png += _chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += _chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


def main():
    global _BLOB_BYTES
    _BLOB_BYTES = zlib.decompress(base64.b64decode(_BLOB))
    fb = bytearray(PAPER * (W * H))
    rect(fb, 0, 0, 1024, 118, (20, 33, 61))
    blit(fb, 0)
    blit(fb, 1)
    rect(fb, 0, 118, 1024, 126, (178, 34, 34))
    blit(fb, 2)
    blit(fb, 3)
    blit(fb, 4)
    blit(fb, 5)
    blit(fb, 6)
    hline(fb, 48, 418, 976, 2, (200, 194, 182))
    rect(fb, 48, 440, 496, 590, (255, 255, 255))
    rect_outline(fb, 48, 440, 496, 590, 2, (200, 194, 182))
    blit(fb, 7)
    blit(fb, 8)
    blit(fb, 9)
    blit(fb, 10)
    blit(fb, 11)
    rect(fb, 528, 440, 976, 590, (255, 255, 255))
    rect_outline(fb, 528, 440, 976, 590, 2, (200, 194, 182))
    blit(fb, 12)
    blit(fb, 13)
    blit(fb, 14)
    blit(fb, 15)
    blit(fb, 16)
    rect(fb, 48, 602, 496, 752, (255, 255, 255))
    rect_outline(fb, 48, 602, 496, 752, 2, (200, 194, 182))
    blit(fb, 17)
    blit(fb, 18)
    blit(fb, 19)
    blit(fb, 20)
    blit(fb, 21)
    rect(fb, 528, 602, 976, 752, (255, 255, 255))
    rect_outline(fb, 528, 602, 976, 752, 2, (200, 194, 182))
    blit(fb, 22)
    blit(fb, 23)
    blit(fb, 24)
    blit(fb, 25)
    blit(fb, 26)
    rect(fb, 48, 764, 496, 914, (255, 255, 255))
    rect_outline(fb, 48, 764, 496, 914, 2, (200, 194, 182))
    blit(fb, 27)
    blit(fb, 28)
    blit(fb, 29)
    blit(fb, 30)
    blit(fb, 31)
    rect(fb, 528, 764, 976, 914, (255, 255, 255))
    rect_outline(fb, 528, 764, 976, 914, 2, (200, 194, 182))
    blit(fb, 32)
    blit(fb, 33)
    blit(fb, 34)
    blit(fb, 35)
    blit(fb, 36)
    rect(fb, 48, 932, 976, 978, (20, 33, 61))
    blit(fb, 37)
    blit(fb, 38)

    out = os.environ.get("OUTPUT")
    if not out:
        d = os.environ.get("MAKEFUN_OUTPUT_DIR")
        if d:
            out = os.path.join(d, "entry.png")
        elif os.path.isdir("/output"):
            out = "/output/entry.png"
        else:
            out = "./entry.png"
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    write_png(fb, out)
    print("wrote", out)


if __name__ == "__main__":
    main()
