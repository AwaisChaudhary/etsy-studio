"""Procedural paper textures (original, generated) as JPEG data URIs."""
import base64, io
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def _noise(w, h, rng, scales=((6, 0.45), (24, 0.3), (96, 0.18), (384, 0.07))):
    out = np.zeros((h, w), np.float32)
    for cells, amp in scales:
        gw, gh = max(2, int(w / (w / cells))), max(2, int(cells * h / w))
        g = rng.random((gh, gw)).astype(np.float32)
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += np.asarray(im, np.float32) / 255 * amp
    return out / sum(a for _, a in scales)

def _vignette(w, h, power=2.6):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = (x / w - 0.5) * 2, (y / h - 0.5) * 2
    return np.clip(np.maximum(np.abs(dx), np.abs(dy)) ** power, 0, 1)

def _uri(arr, q=60):
    im = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

def tea(w=1275, h=1650, seed=1, base=(238, 224, 198), dark=(170, 120, 74), rings=3, strength=1.0):
    rng = np.random.default_rng(seed)
    n = _noise(w, h, rng)
    blot = np.asarray(Image.fromarray((_noise(w, h, rng, ((3, .6), (10, .4))) * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(30)), np.float32) / 255
    a = 0.10 + 0.32 * (n - 0.35) + 0.42 * np.clip(blot - 0.48, 0, 1) * 2 + 0.38 * _vignette(w, h)
    ring = Image.new("L", (w, h), 0); d = ImageDraw.Draw(ring)
    for _ in range(rings):
        cx, cy, r = rng.integers(0, w), rng.integers(0, h), rng.integers(w // 10, w // 5)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=150, width=int(rng.integers(5, 12)))
        d.ellipse([cx - r + 8, cy - r + 6, cx + r - 6, cy + r - 8], outline=70, width=3)
    ring = np.asarray(ring.filter(ImageFilter.GaussianBlur(3)), np.float32) / 255
    a = np.clip((a + ring * 0.5) * strength, 0, 1)[..., None]
    fib = (rng.random((h, w)) * 10 - 5)[..., None]
    col = np.array(base, np.float32) * (1 - a) + np.array(dark, np.float32) * a + fib
    return _uri(col)

def night(w=1275, h=1650, seed=2, base=(24, 33, 62), light=(52, 66, 112), stars=900):
    rng = np.random.default_rng(seed)
    n = _noise(w, h, rng)
    a = np.clip(0.2 + 0.6 * (n - 0.4) + 0.1, 0, 1)
    v = _vignette(w, h, 2.0)[..., None]
    col = np.array(base, np.float32) * (1 - a[..., None]) + np.array(light, np.float32) * a[..., None]
    col = col * (1 - 0.35 * v) + (rng.random((h, w, 1)) * 6 - 3)
    im = Image.fromarray(np.clip(col, 0, 255).astype(np.uint8)); d = ImageDraw.Draw(im)
    for _ in range(stars):
        x, y = rng.integers(0, w), rng.integers(0, h); r = rng.choice([0.6, 0.9, 1.3, 2.0], p=[.5, .3, .15, .05]); g = int(rng.integers(170, 255))
        d.ellipse([x - r, y - r, x + r, y + r], fill=(g, g, int(min(255, g + 10))))
    return _uri(np.asarray(im, np.float32))

def kraft(w=1275, h=1650, seed=3):
    return tea(w, h, seed, base=(200, 164, 120), dark=(150, 108, 66), rings=0, strength=0.6)
