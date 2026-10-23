#!/usr/bin/env python3
"""Prepare a photo for a post.

    python3 tools/prep_image.py ~/Desktop/IMG_1234.jpg workshop-sept-2026

Writes static/posts/workshop-sept-2026.jpg: rotated the right way up, at most 1600px wide,
JPEG quality 85, with all camera metadata (including GPS location) removed.
Then put `image: workshop-sept-2026.jpg` and an `image_alt:` line in the post's front matter.
"""
import sys, pathlib
from PIL import Image, ImageOps

if len(sys.argv) < 2:
    sys.exit(__doc__)
src = pathlib.Path(sys.argv[1]).expanduser()
name = sys.argv[2] if len(sys.argv) > 2 else src.stem.lower().replace(" ", "-")
out = pathlib.Path(__file__).resolve().parents[1] / "static" / "posts" / f"{name}.jpg"
out.parent.mkdir(parents=True, exist_ok=True)
im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
w, h = im.size
if w > 1600:
    im = im.resize((1600, round(h * 1600 / w)), Image.LANCZOS)
im.save(out, "JPEG", quality=85, optimize=True, progressive=True)
print(f"{out}  {im.size[0]}x{im.size[1]}  {out.stat().st_size // 1024} KB")
print(f"front matter:\n  image: {name}.jpg\n  image_alt: \"...\"")
