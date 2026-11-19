# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/soluska/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/soluska/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A code-only newspaper front page that sums up the world news of Thursday 19 November 2026 in one image. The program draws the entire front page with Python + Pillow — masthead, lead story, six story cards and an "Also Today" strip — and writes it to /output/entry.png. No photographs, no AI-generated images: every visual is drawn in code.

## Run it

```sh
python3 main.py
```

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` (1024x1024, well under the 1 MiB limit).
`MAKEFUN_OUTPUT_DIR` is optional; without it the poster is written to
`/output/entry.png`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=esagh3na&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
