[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/hiduplahzomb/news-image-20261124-ka-r3/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/hiduplahzomb/news-image-20261124-ka-r3/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

# World news of Tuesday 24 November 2026 — in one image

A newspaper front page summing up Tuesday 24 November 2026: the ICJ ruling
that Myanmar committed genocide against the Rohingya (backed by fourteen
states) leads, followed by Shenzhou-24 reaching Tiangong, Ukraine's strike
on a Russian ship in the Gulf of Finland, the UN chief's call to rein in AI
risks within a year, the Solomon Islands naming Australia its top security
partner, the Houthi strike on Riyadh's tallest tower, and Nvidia's CEO
return — plus a three-item in-brief band (measles, Gaza, Iran) and a markets
strip (S&P, Nasdaq, Nikkei, gold, Brent). Every pictogram is drawn from
scratch in code; all labels are short and factual.

## How to run

Re-render the image (requires Pillow and the DejaVu fonts):

```sh
python3 draw.py        # writes entry.png
```

Run the entry (standard library only, no network):

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` copies the repository's `entry.png` to the output directory and
verifies the copy is byte-identical to the source, exiting non-zero on any
mismatch. Running it twice produces identical bytes.

## License

MIT — see [LICENSE](LICENSE).
