#!/usr/bin/env python3
"""Render 'The World in One Day - 25 November 2026' as a 1024x1024 news collage."""
import math, os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

def font(size, bold=True):
    names = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for n in names:
        if os.path.exists(n):
            return ImageFont.truetype(n, size)
    return ImageFont.load_default()

img = Image.new("RGB", (W, H), (10, 16, 38))
d = ImageDraw.Draw(img, "RGBA")

# vertical gradient sky
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(10 + 18 * t), int(16 + 26 * t), int(38 + 52 * t)))

# stars / data dots
for i in range(140):
    x = (i * 173) % W; y = (i * 97) % 300
    r = 1 + (i % 3)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, 70))

# header banner
d.rectangle([0, 0, W, 150], fill=(178, 24, 40))
d.rectangle([0, 150, W, 160], fill=(245, 197, 66))
d.text((48, 26), "THE WORLD IN ONE DAY", font=font(58), fill=(255, 255, 255))
d.text((50, 98), "TUESDAY  -  25 NOVEMBER 2026  -  GLOBAL EDITION", font=font(24, False), fill=(255, 226, 170))

# globe
cx, cy, R = 330, 470, 235
for rr in range(R, 0, -4):
    t = rr / R
    d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(int(24 + 30 * t), int(90 + 60 * t), int(160 + 40 * t)))
d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(140, 210, 255), width=4)
# latitude / longitude arcs
for k in range(-2, 3):
    yy = cy + k * 78
    half = int(math.sqrt(max(R * R - (k * 78) ** 2, 0)))
    d.arc([cx - half, yy - 26, cx + half, yy + 26], 0, 180, fill=(160, 220, 255, 120), width=2)
    d.arc([cx - half, yy - 26, cx + half, yy + 26], 180, 360, fill=(160, 220, 255, 120), width=2)
for k in range(-2, 3):
    wdt = int(R * math.cos(k * 0.5))
    d.ellipse([cx - wdt, cy - R, cx + wdt, cy + R], outline=(160, 220, 255, 90), width=2)
# stylised continents (green landmasses)
land = (74, 178, 105)
blobs = [
    [(cx-150,cy-120),(cx-70,cy-150),(cx-40,cy-90),(cx-90,cy-55),(cx-160,cy-70)],
    [(cx-95,cy-10),(cx-45,cy-35),(cx-30,cy+40),(cx-70,cy+80),(cx-105,cy+30)],
    [(cx+10,cy-130),(cx+90,cy-140),(cx+130,cy-80),(cx+70,cy-60),(cx+15,cy-85)],
    [(cx+35,cy-30),(cx+95,cy-45),(cx+120,cy+15),(cx+70,cy+55),(cx+30,cy+10)],
    [(cx+95,cy+95),(cx+165,cy+85),(cx+185,cy+135),(cx+130,cy+160),(cx+95,cy+135)],
    [(cx-30,cy+120),(cx+25,cy+110),(cx+40,cy+155),(cx-15,cy+170),(cx-38,cy+145)],
]
for b in blobs:
    d.polygon(b, fill=land)
# orbit ring + pin markers
d.ellipse([cx - R - 42, cy - R - 42, cx + R + 42, cy + R + 42], outline=(245, 197, 66, 160), width=3)
for (px, py) in [(cx-110,cy-95),(cx+70,cy-105),(cx+120,cy+30),(cx-60,cy+55),(cx+20,cy+140)]:
    d.ellipse([px-9,py-9,px+9,py+9], fill=(245,197,66), outline=(255,255,255), width=2)

# headline panels on the right
panels = [
    ("WORLD", "One planet, one day:\nstories crossing every\nborder before midnight.", (178,24,40)),
    ("MARKETS", "Traders weigh the day's\nsignals from Asia to\nWall Street's close.", (24,110,60)),
    ("TECH", "AI tools move from lab\nto everyday life, one\nlaunch at a time.", (70,50,160)),
    ("CLIMATE", "Cities trade ideas on\ncooler streets, cleaner\nair and rising seas.", (10,120,140)),
]
y = 205
for tag, body, col in panels:
    d.rounded_rectangle([610, y, 985, y + 118], radius=14, fill=(255,255,255,235))
    d.rounded_rectangle([610, y, 700, y + 34], radius=8, fill=col)
    d.text((622, y + 6), tag, font=font(19), fill=(255,255,255))
    ty = y + 44
    for line in body.split("\n"):
        d.text((626, ty), line, font=font(19, False), fill=(24,28,44))
        ty += 24
    y += 132

# bottom ticker band
d.rectangle([0, 800, W, 1024], fill=(8, 10, 22))
d.rectangle([0, 800, W, 810], fill=(245, 197, 66))
d.text((48, 826), "24 HOURS  -  EVERY CONTINENT  -  ONE FRONT PAGE", font=font(27), fill=(245, 197, 66))
items = [
    "SPORT: finals, records and last-minute drama",
    "CULTURE: festivals light up the night sky",
    "SCIENCE: eyes on the oceans and the stars",
    "PEOPLE: small kindnesses, told worldwide",
]
ty = 872
for it in items:
    d.ellipse([52, ty + 7, 62, ty + 17], fill=(178, 24, 40))
    d.text((76, ty), it, font=font(23, False), fill=(232, 236, 248))
    ty += 34
d.text((48, 986), "25.11.2026", font=font(20), fill=(140, 160, 200))

img.save(OUT)
print("wrote", OUT, img.size)
