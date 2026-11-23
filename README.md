[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/heraltmosses54-pixel/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/heraltmosses54-pixel/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# THE WORLD — Monday 23 November 2026

A single-file program that sums up one day of world news in one
image: a 1024×1024 newspaper front page covering 23 stories from
six continents. The lead story reports COP31 closing in Antalya
without a climate deal, joined by a twelve-story grid (the US
House result, the Kyiv strikes, the Banten factory fire, the
Nikkei slide and more), a dotted world map with a red marker for
every story, a "By the Numbers" rail, a nine-item briefs band and
a sport footer.

## How to run

```sh
python3 main.py
```

The PNG is written to the first of these locations that applies:

1. `$OUTPUT`, if that environment variable is set;
2. `$MAKEFUN_OUTPUT_DIR/entry.png`, if that variable is set;
3. `/output/entry.png`, if `/output` exists;
4. `entry.png` next to the script.

## How it works

Everything is done with the Python 3 standard library alone — no
third-party packages, no font files, no network. The text is
typeset from a glyph atlas embedded in `main.py` as base64 data:
the atlas bitmap (alpha quantised to 4 bits, zlib-compressed)
plus a JSON table of per-glyph metrics for seven styles
(masthead, lead headline, section heads, kickers, deck, body and
tiny). At run time the atlas is decoded, the glyphs are
alpha-blended into an RGB framebuffer, the dotted map is plotted
from a run-length land grid, and the finished page is encoded as
a PNG with `struct` and `zlib`.

The output is fully deterministic: the same bytes come out on
every run, on any machine.
