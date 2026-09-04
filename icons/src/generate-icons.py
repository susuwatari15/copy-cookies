#!/usr/bin/env python3
"""Sinh icon 16/48/128 cho extension tu artwork goc.

Nguon: icons/src/cookies-icon.png (splash art Hextech cookie 1254x1254).
Khung vien trang tri cua artwork bi cat bo — o kich thuoc icon no chi con
la nhieu. Chi giu phan banh, cat tron va de nen trong suot de icon noi tren
ca thanh cong cu sang lan toi.

Chay: python3 icons/src/generate-icons.py
"""
import os
from PIL import Image, ImageDraw, ImageFilter

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(SRC_DIR, os.pardir))
SRC = os.path.join(SRC_DIR, "cookies-icon.png")

CENTER = (622, 625)  # tam cua banh trong artwork goc

# size -> (ban kinh crop, unsharp mask sau khi thu nho)
# Kich thuoc cang nho cat cang sat + net hon de vien banh & loi pha le con doc duoc.
PROFILES = {
    128: (452, (0.7, 70)),
    48:  (435, (0.8, 110)),
    16:  (420, (0.8, 140)),
}


def render(size, half, sharpen):
    src = Image.open(SRC).convert("RGB")
    cx, cy = CENTER
    im = src.crop((cx - half, cy - half, cx + half, cy + half)).convert("RGBA")

    # mat na tron ve o 4x roi thu nho -> vien muot, khong rang cua
    mask = Image.new("L", (half * 8, half * 8), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, half * 8 - 1, half * 8 - 1), fill=255)
    mask = mask.resize((half * 2, half * 2), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.5))
    im.putalpha(mask)

    out = im.resize((size, size), Image.LANCZOS)
    if sharpen:
        radius, percent = sharpen
        rgb = out.convert("RGB").filter(
            ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=0))
        rgb.putalpha(out.getchannel("A"))
        out = rgb
    return out


if __name__ == "__main__":
    for size, (half, sharpen) in PROFILES.items():
        path = os.path.join(OUT_DIR, f"icon{size}.png")
        render(size, half, sharpen).save(path)
        print("wrote", path)
