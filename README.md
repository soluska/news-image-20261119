[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

# The World in One Day — 19 November 2026

A newspaper front page that sums up Thursday 19 November 2026's world
news in a single image — for the make.fun `news-image-20261119` bounty
($250).

Lead story: Trump, Xi and Putin hold their first-ever three-way summit
in Shenzhen, on the sidelines of APEC, with Ukraine topping the agenda.
Also inside: Ukraine strikes the Crimea Bridge for the third time in a
week; Iran hits Gulf states in answer to the US strike on Qeshm island
as the IEA calls the Hormuz crisis energy's biggest-ever threat; GTA VI
finally launches to a 99 Metacritic score; the World Court delivers its
genocide judgment on Myanmar; Cyclone Akvan drives over 100,000 people
from their homes in Odisha; and COP31 deadlocks in Antalya — plus an
"Also Today" strip with six more stories, from Anthropic's record
$81.3bn IPO to a record $190.4m Van Gogh sale.

Everything is drawn entirely in code with Pillow: vector shapes, three
hand-drawn flags, a Shenzhen dusk skyline, per-story icons and real
typography (DejaVu fonts, bundled under `fonts/`). No photographs, no
AI images, no network. Fully deterministic: two runs produce
byte-identical output.

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` (1024x1024, well under the 1 MiB limit).
`MAKEFUN_OUTPUT_DIR` is optional; without it the poster is written to
`/output/entry.png`.
