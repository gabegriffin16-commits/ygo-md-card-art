# Master Duel card art

Compressed card images for the [Master Duel Companion App](https://github.com/gabegriffin16-commits/ygo-md-companion).

- `art/<card id>.avif`: every card in Master Duel, 421×614 AVIF (about 33 KB each, around a fifth of the original JPG).
- `build_art.py` makes them from YGOPRODeck's images; `.github/workflows/build-art.yml` runs it weekly and adds new cards.
- Served by GitHub Pages at `https://gabegriffin16-commits.github.io/ygo-md-card-art/art/<id>.avif`.

Card images © Konami. Images are re-hosted for personal use per YGOPRODeck's API guidance (don't hotlink their servers).
