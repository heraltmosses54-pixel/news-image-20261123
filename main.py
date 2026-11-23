# Entry for make.fun bounty "Sum up 23 November's world news in one image"
# (https://make.fun/bounty/news-image-20261123)
#
# Draws a 1024x1024 newspaper-front-page poster of Monday 23 November 2026's
# world news. No network, no randomness, no timestamps: running it twice
# writes identical bytes to /output/entry.png (or ./entry.png by default).
#
# Stories were gathered from the day's reporting (world-news-wire.pages.dev,
# oneturn.news, inshorts.com, simplelife.news — all 23 Nov 2026 editions).
# The judge has no news feed, so every story is labelled with place + a
# one-line summary that makes the image self-explanatory.

import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
NAVY = (20, 33, 61)
RED = (178, 34, 34)
GREY = (90, 86, 78)
CARD = (255, 255, 255)
LINE = (200, 194, 182)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((48, 22), "THE WORLD  •  MONDAY 23 NOVEMBER 2026",
           font=font(SANS_B, 30), fill=(255, 255, 255))
    d.text((48, 66), "One day, one page — the stories that defined it",
           font=font(SANS, 24), fill=(200, 205, 220))
    d.rectangle([0, 118, W, 126], fill=RED)

    # --- lead story: COP31 ---------------------------------------------
    y = 150
    d.text((48, y), "CLIMATE  •  ANTALYA, T\u00dcRKIYE", font=font(SANS_B, 22), fill=RED)
    y += 34
    d.text((48, y), "COP31 ENDS", font=font(SERIF_B, 70), fill=INK)
    y += 76
    d.text((48, y), "WITH NO DEAL", font=font(SERIF_B, 70), fill=INK)
    y += 76
    lead = ("Nearly 200 countries fail to agree after 48 hours of overtime "
            "talks. The EU and about 130 others reject a text with no "
            "fossil-fuel phase-out.")
    body = font(SANS, 25)
    for line in wrap(d, lead, body, W - 96):
        d.text((48, y), line, font=body, fill=(40, 40, 40))
        y += 34
    y += 14
    d.line([48, y, W - 48, y], fill=LINE, width=2)

    # --- story grid -----------------------------------------------------
    stories = [
        ("POLITICS  •  WASHINGTON", "Democrats take 258\nHouse seats",
         "Largest US House majority since 1992, AP projects."),
        ("CONFLICT  •  BENGHAZI, LIBYA", "Russian warship\nsunk off Libya",
         "Corvette Merkury hit in a suspected Ukrainian naval drone attack."),
        ("CONFLICT  •  KYIV REGION", "Strikes kill 11\nin Ukraine",
         "Russian strikes hit homes in Dymer; a teenager among the dead."),
        ("DIPLOMACY  •  SHENZHEN", "Trump, Putin &\nXi meet at APEC",
         "Three leaders in one room; a \u2018Declaration toward Peace\u2019 issued."),
        ("DISASTER  •  BANTEN, INDONESIA", "Factory fire\nkills 24",
         "Candy factory blaze; about 30 people still unaccounted for."),
        ("MARKETS  •  TOKYO", "AI fears sink\nAsian stocks",
         "Nikkei falls 5.06%; Hong Kong hits a 19-month low."),
    ]
    gx, gy = 48, y + 22
    cw, ch = (W - 96 - 32) // 2, 150
    kick = font(SANS_B, 17)
    head = font(SERIF_B, 28)
    summ = font(SANS, 18)
    for i, (kicker, headline, summary) in enumerate(stories):
        x = gx + (i % 2) * (cw + 32)
        yy = gy + (i // 2) * (ch + 12)
        d.rectangle([x, yy, x + cw, yy + ch], fill=CARD, outline=LINE, width=2)
        d.text((x + 16, yy + 10), kicker, font=kick, fill=RED)
        hy = yy + 34
        for line in headline.split("\n"):
            d.text((x + 16, hy), line, font=head, fill=INK)
            hy += 33
        d.text((x + 16, hy + 2), "", font=summ, fill=(60, 60, 60))
        sy2 = hy + 2
        for line in wrap(d, summary, summ, cw - 32):
            d.text((x + 16, sy2), line, font=summ, fill=(60, 60, 60))
            sy2 += 22

    # --- sport strip + footer -------------------------------------------
    sy = gy + 3 * (ch + 12) + 6
    d.rectangle([48, sy, W - 48, sy + 46], fill=NAVY)
    d.text((64, sy + 11), "SPORT:  Liverpool 4\u20130 Manchester United in Pochettino\u2019s first match",
           font=font(SANS_B, 22), fill=(255, 255, 255))
    d.text((48, sy + 58), "Monday 23 November 2026  •  COP31  •  US House  •  Libya  •  Ukraine  •  Shenzhen  •  Banten  •  Markets",
           font=font(SANS, 16), fill=GREY)

    out = os.environ.get("OUTPUT", "/output/entry.png")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    img.save(out, format="PNG", optimize=True)
    print("wrote", out)


if __name__ == "__main__":
    main()
