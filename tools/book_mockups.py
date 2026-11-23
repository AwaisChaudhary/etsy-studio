"""Original mockups for our own KDP paperbacks (made from our own cover/interior renders)."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os
OUT = "/home/claude/etsy-studio/pins/books"; os.makedirs(OUT, exist_ok=True)
G = "/usr/share/fonts/truetype/google-fonts/"
def F(name, size): return ImageFont.truetype(G + name, size)
LORA = "Lora-Variable.ttf"; PB = "Poppins-Bold.ttf"; PM = "Poppins-Medium.ttf"

def lora(size, bold=True):
    f = F(LORA, size)
    try: f.set_variation_by_name("Bold" if bold else "Regular")
    except Exception: pass
    return f

def shadowed(canvas, img, xy, angle=0, blur=22, off=(14, 22), alpha=110):
    im = img.convert("RGBA")
    if angle: im = im.rotate(angle, expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", (im.width + 120, im.height + 120), (0, 0, 0, 0))
    mask = im.split()[3].point(lambda a: alpha if a > 0 else 0)
    sh.paste((20, 20, 30, 255), (60, 60), mask)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(sh, (xy[0] - 60 + off[0], xy[1] - 60 + off[1]))
    canvas.alpha_composite(im, xy)

def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur); return lines

def text_block(d, x, y, lines, font, fill, gap=1.18):
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill); y += int(font.size * gap)
    return y

knit = Image.open("/tmp/cov/knit-front.png").convert("RGB")
race = Image.open("/tmp/cov/race-front.png").convert("RGB")
p14 = Image.open("/home/claude/kdp/project-journal/int-014.png").convert("RGB")
p97 = Image.open("/home/claude/kdp/project-journal/int-097.png").convert("RGB")
CREAM, NAVY, BERRY, TEAL, GOLD = (243, 238, 228), (30, 41, 74), (184, 44, 98), (31, 138, 128), (245, 168, 38)

# 1) site thumbnail 400x400
c = Image.new("RGBA", (800, 800), CREAM + (255,))
b = knit.resize((470, int(470 * knit.height / knit.width)))
shadowed(c, b, (165, 90))
c.convert("RGB").resize((400, 400), Image.LANCZOS).save("/home/claude/etsy-studio/site/assets/shop/knit-crochet-project-journal.jpg", quality=88)

# 2) knit pin A: cover hero
c = Image.new("RGBA", (1000, 1500), (232, 243, 240, 255))
d = ImageDraw.Draw(c)
d.rectangle((0, 980, 1000, 1500), fill=TEAL)
b = knit.resize((560, int(560 * knit.height / knit.width)))
shadowed(c, b, (220, 300), angle=-4)
d = ImageDraw.Draw(c)
y = text_block(d, 70, 70, ["The knitting journal", "that remembers for you"], lora(64), NAVY)
d.text((70, y + 8), "Yarn, hook, gauge, rows and notes for 40 projects", font=F(PM, 30), fill=BERRY)
y2 = 1140
for ln in ["40 project spreads with 100-row counters", "Yarn weight + hook and needle size charts", "Stash inventory, abbreviations, graph paper"]:
    d.text((70, y2), "• " + ln, font=F(PM, 32), fill="white"); y2 += 52
d.rounded_rectangle((70, 1330, 600, 1420), radius=45, fill=GOLD)
d.text((105, 1350), "Paperback on Amazon · $9.99", font=F(PB, 32), fill=NAVY)
d.text((640, 1360), "Purl & Paper", font=F(PB, 34), fill="white")
c.convert("RGB").save(f"{OUT}/knit-journal-pin-a.jpg", quality=90)

# 3) knit pin B: inside pages fan + cover
c = Image.new("RGBA", (1000, 1500), CREAM + (255,))
d = ImageDraw.Draw(c)
y = text_block(d, 70, 80, ["“Which hook was that?”"], lora(66), NAVY)
y = text_block(d, 70, y + 10, wrap(d, "Keep every make in one place: a project journal for knitters and crocheters.", F(PM, 34), 860), F(PM, 34), BERRY)
pa = p14.resize((470, int(470 * p14.height / p14.width)))
pb = p97.resize((470, int(470 * p97.height / p97.width)))
shadowed(c, pa, (60, 420), angle=6)
shadowed(c, pb, (470, 440), angle=-5)
cv = knit.resize((380, int(380 * knit.height / knit.width)))
shadowed(c, cv, (310, 760), angle=-2)
d = ImageDraw.Draw(c)
d.rounded_rectangle((70, 1340, 930, 1430), radius=45, fill=NAVY)
d.text((120, 1360), "Knit & Crochet Project Journal · $9.99 paperback", font=F(PB, 31), fill="white")
c.convert("RGB").save(f"{OUT}/knit-journal-pin-b.jpg", quality=90)

# 4) race pin
DARK, LIME = (17, 18, 22), (214, 245, 61)
c = Image.new("RGBA", (1000, 1500), DARK + (255,))
d = ImageDraw.Draw(c)
for x in range(-1500, 1000, 46): d.line((x, 1500, x + 1500, 0), fill=(32, 34, 40), width=2)
d.text((70, 70), "TRAINING FOR A FITNESS RACE?", font=F(PB, 34), fill=LIME)
y = text_block(d, 70, 130, wrap(d, "Log 12 weeks of runs and stations in one book", F(PB, 60), 860), F(PB, 60), "white", gap=1.12)
b = race.resize((520, int(520 * race.height / race.width)))
shadowed(c, b, (240, y + 50), angle=-3, alpha=200, off=(18, 26))
d = ImageDraw.Draw(c)
d.rounded_rectangle((70, 1340, 930, 1430), radius=45, fill=LIME)
d.text((110, 1360), "Race Ready training log · $9.99 paperback", font=F(PB, 33), fill=DARK)
c.convert("RGB").save(f"{OUT}/race-ready-pin.jpg", quality=90)
print("ok")
