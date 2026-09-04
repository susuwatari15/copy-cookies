import math, os, sys
SP = os.path.dirname(os.path.abspath(__file__))

def hexagon(cx, cy, r, rot=0):
    pts = []
    for i in range(6):
        a = math.radians(60*i - 90 + rot)   # pointy-top
        pts.append(f"{cx + r*math.cos(a):.2f},{cy + r*math.sin(a):.2f}")
    return " ".join(pts)

def diamond(cx, cy, s):
    return f'<rect x="{cx-s:.2f}" y="{cy-s:.2f}" width="{2*s:.2f}" height="{2*s:.2f}" transform="rotate(45 {cx:.2f} {cy:.2f})"'

def svg(size, detail):
    S = 128  # design space
    k = size / S
    cx = cy = S/2
    # chips: (x, y, radius) — layout kept from the original cookie icon
    chips = [(46,44,6.5),(80,50,5.5),(42,72,5.5),(62,84,5.0),(86,80,5.5)]
    glow = 'filter="url(#glow)"' if detail else ''
    parts = []
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {S} {S}">')
    parts.append('''<defs>
  <linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#F0E6D2"/><stop offset="45%" stop-color="#C8AA6E"/>
    <stop offset="70%" stop-color="#C89B3C"/><stop offset="100%" stop-color="#785A28"/>
  </linearGradient>
  <radialGradient id="core" cx="50%" cy="42%" r="62%">
    <stop offset="0%" stop-color="#0A323C"/><stop offset="55%" stop-color="#0A1428"/>
    <stop offset="100%" stop-color="#010A13"/>
  </radialGradient>
  <linearGradient id="teal" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#CDFAFA"/><stop offset="50%" stop-color="#0AC8B9"/>
    <stop offset="100%" stop-color="#0397AB"/>
  </linearGradient>
  <linearGradient id="gold16" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#F5EEDF"/><stop offset="55%" stop-color="#D3B375"/>
    <stop offset="100%" stop-color="#9A7433"/>
  </linearGradient>
  <radialGradient id="core16" cx="50%" cy="42%" r="65%">
    <stop offset="0%" stop-color="#12495A"/><stop offset="60%" stop-color="#0A2436"/>
    <stop offset="100%" stop-color="#04131F"/>
  </radialGradient>
  <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="2.4" result="b"/>
    <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter>
</defs>''')
    if detail:
        # outer gold hexagon frame
        parts.append(f'<polygon points="{hexagon(cx,cy,60)}" fill="url(#core)" stroke="url(#gold)" stroke-width="7" stroke-linejoin="round"/>')
        # inner hairline
        parts.append(f'<polygon points="{hexagon(cx,cy,49)}" fill="none" stroke="#C8AA6E" stroke-width="1.6" opacity="0.75" stroke-linejoin="round"/>')
        # hextech chips
        for x, y, r in chips:
            parts.append(f'{diamond(x,y,r)} fill="url(#teal)" {glow}/>')
        # centre facet spark
        parts.append(f'<polygon points="{hexagon(cx,cy,49)}" fill="none" stroke="#0AC8B9" stroke-width="0.9" opacity="0.28" stroke-linejoin="round"/>')
    else:
        # 16px: heavier strokes, single hextech crystal core (chips are illegible at this size)
        parts.append(f'<polygon points="{hexagon(cx,cy,59)}" fill="url(#core16)" stroke="url(#gold16)" stroke-width="11" stroke-linejoin="round"/>')
        parts.append(f'{diamond(cx,cy,26)} fill="url(#teal)"/>')
        parts.append(f'{diamond(cx,cy,13)} fill="#EAFFFF"/>')
    parts.append('</svg>')
    return "\n".join(parts)

for size, detail in ((128, True), (48, True), (16, False)):
    open(f"{SP}/icon{size}.svg","w").write(svg(size, detail))
    open(f"{SP}/icon{size}.html","w").write(
        "<style>html,body{margin:0;padding:0;background:transparent}</style>" + svg(size, detail))
print("ok")

# --- render PNG bang Chrome headless (khong can dependency ngoai) ---
# Chay:  python3 icons/src/generate-icons.py
import subprocess, shutil
CHROME = next((p for p in (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    shutil.which("google-chrome"), shutil.which("chromium")) if p and os.path.exists(p)), None)
OUT = os.path.abspath(os.path.join(SP, os.pardir))  # icons/
if CHROME:
    for size in (128, 48, 16):
        subprocess.run([CHROME, "--headless", "--disable-gpu", "--force-color-profile=srgb",
                        "--default-background-color=00000000", "--hide-scrollbars",
                        f"--window-size={size},{size}", f"--screenshot={OUT}/icon{size}.png",
                        "--virtual-time-budget=800", f"file://{SP}/icon{size}.html"],
                       check=True, capture_output=True)
    print("rendered ->", OUT)
else:
    print("Khong tim thay Chrome; dung file SVG trong icons/src de tu render.")
