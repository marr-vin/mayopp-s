"""Run after adding new product photos: python optimize-images.py"""
import os

try:
    from PIL import Image
except ImportError:
    print("Install Pillow first: pip install Pillow")
    raise

images_dir = os.path.join(os.path.dirname(__file__), "images")

limits = {
    "hero-raw.jpg": 640,
    "hero-processed-premium.jpg": 640,
    "hero-processed-premium.png": 640,
    "mabel-maker.jpg": 720,
    "mabel-maker.png": 720,
    "weanimix.png": 800,
    "fukonte.png": 800,
    "natural-spices.png": 800,
    "fish-powder.png": 800,
    "shrimp-powder.png": 800,
    "groundnut.png": 800,
}

for name, max_w in limits.items():
    path = os.path.join(images_dir, name)
    if not os.path.isfile(path):
        continue
    before = os.path.getsize(path)
    im = Image.open(path)
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")
    w, h = im.size
    if w > max_w:
        im = im.resize((max_w, int(h * max_w / w)), Image.Resampling.LANCZOS)
    out = path if path.endswith(".jpg") else path.replace(".png", ".jpg")
    im.save(out, "JPEG", quality=82, optimize=True, progressive=True)
    if out != path and os.path.isfile(path):
        os.remove(path)
    after = os.path.getsize(out)
    print(f"{os.path.basename(out)}: {before/1024:.0f}KB -> {after/1024:.0f}KB")

print("done")
