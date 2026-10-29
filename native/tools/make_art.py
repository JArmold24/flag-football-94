"""App Store icon (1024x1024, full bleed, no alpha) and launch screen art for Flag Football '94.
Pixel art drawn on a small grid and scaled up crisp, in the game's own palette."""
import math, sys, os
from PIL import Image
OUT = sys.argv[1] if len(sys.argv) > 1 else 'assets'
FONT = {  # 5x7 pixel glyphs
 'F': ['11111','10000','10000','11110','10000','10000','10000'], 'L': ['10000','10000','10000','10000','10000','10000','11111'],
 'A': ['01110','10001','10001','11111','10001','10001','10001'], 'G': ['01111','10000','10000','10011','10001','10001','01111'],
 'O': ['01110','10001','10001','10001','10001','10001','01110'], 'T': ['11111','00100','00100','00100','00100','00100','00100'],
 'B': ['11110','10001','10001','11110','10001','10001','11110'], "'": ['00100','00100','01000','00000','00000','00000','00000'],
 '9': ['01110','10001','10001','01111','00001','00010','01100'], '4': ['00010','00110','01010','10010','11111','00010','00010'], ' ': ['00000']*7,
}
def text(cells, s, x0, y0, scale, col, shadow=None, outline=None):
    x = x0
    for ch in s:
        g = FONT[ch]
        for gy, row in enumerate(g):
            for gx, b in enumerate(row):
                if b == '1':
                    for sy in range(scale):
                        for sx in range(scale):
                            px, py = x + gx * scale + sx, y0 + gy * scale + sy
                            if outline:
                                for ox, oy in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)):
                                    q = (px + ox, py + oy)
                                    if q not in cells or cells[q][1] < 2: cells[q] = (outline, 1)
                            if shadow: 
                                q = (px + scale, py + scale)
                                if q not in cells or cells[q][1] < 1: cells[q] = (shadow, 0)
                            cells[(px, py)] = (col, 2)
        x += (len(g[0]) + 1) * scale
def width(s, scale): return sum((len(FONT[c][0]) + 1) * scale for c in s) - scale
def ball(put, cx, cy, a, b, tilt):
    th = math.radians(tilt); c, s_ = math.cos(th), math.sin(th)
    B, D, H, W, K = (181, 100, 31), (110, 58, 18), (222, 150, 96), (250, 250, 250), (0, 0, 0)
    mask = {}
    for y in range(int(cy - a - 2), int(cy + a + 3)):
        for x in range(int(cx - a - 2), int(cx + a + 3)):
            dx, dy = x + 0.5 - cx, y + 0.5 - cy
            u, v = dx * c + dy * s_, -dx * s_ + dy * c
            if (u / a) ** 2 + (v / b) ** 2 <= 1:
                col = B
                if v > b * 0.38: col = D
                elif v < -b * 0.3 and abs(u) < a * 0.55: col = H
                if a * 0.58 < abs(u) < a * 0.58 + max(1.2, a * 0.13): col = W
                if abs(v + b * 0.3) < max(0.7, b * 0.12) and abs(u) < a * 0.3: col = W
                if abs(v + b * 0.3) < b * 0.3 and abs(u) < a * 0.3 and int(u * 1.5 + 100) % 3 == 0: col = W
                mask[(x, y)] = col
    for k, col in mask.items(): put(k[0], k[1], col)
    for (x, y) in list(mask):
        for q in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if q not in mask: put(q[0], q[1], K)

def icon(size=1024, g=64):
    img = Image.new('RGB', (g, g)); px = img.load()
    G1, G2, LINE = (52, 150, 52), (44, 128, 44), (236, 236, 236)
    for y in range(g):
        for x in range(g): px[x, y] = G2 if (y // 8) % 2 else G1
    # night sky band at the top with stadium lights, so the icon reads as a game, not a sports ball
    for y in range(0, 14):
        for x in range(g): px[x, y] = (14 + y, 18 + y, 44 + y * 2)
    for lx in (8, 22, 42, 56):
        for yy in range(3, 6):
            for xx in range(lx - 3, lx + 4): px[xx, yy] = (255, 246, 196) if yy < 5 else (230, 220, 160)
    for x in range(g): px[x, 14] = (30, 30, 40); px[x, 15] = (60, 60, 70)
    for x in range(g): px[x, 34] = LINE
    for x in range(4, 60, 6): px[x, 46] = LINE; px[x + 1, 46] = LINE
    put = lambda x, y, c: (0 <= x < g and 0 <= y < g) and px.__setitem__((x, y), c)
    ball(put, 32, 30, 17, 10, -24)
    cells = {}; s = "'94"
    text(cells, s, (g - width(s, 2)) // 2 + 1, 46, 2, (255, 225, 74), shadow=(120, 60, 0), outline=(0, 0, 0))
    for (x, y), (c, _) in cells.items(): put(x, y, c)
    return img.resize((size, size), Image.NEAREST)

def splash(size=2732, g=136):
    img = Image.new('RGB', (g, g), (11, 11, 20)); px = img.load()
    put = lambda x, y, c: (0 <= x < g and 0 <= y < g) and px.__setitem__((x, y), c)
    ball(put, 68, 56, 16, 9.5, -24)
    cells = {}
    t1 = 'FLAG FOOTBALL'; text(cells, t1, (g - width(t1, 1)) // 2, 74, 1, (255, 225, 74), outline=(0, 0, 0))
    t2 = "'94"; text(cells, t2, (g - width(t2, 2)) // 2, 84, 2, (255, 255, 255), outline=(0, 0, 0))
    for (x, y), (c, _) in cells.items(): put(x, y, c)
    return img.resize((size, size), Image.NEAREST)

os.makedirs(OUT, exist_ok=True)
ic = icon(); ic.save(os.path.join(OUT, 'icon-only.png')); ic.save(os.path.join(OUT, 'icon-foreground.png'))
Image.new('RGB', (1024, 1024), (52, 150, 52)).save(os.path.join(OUT, 'icon-background.png'))
sp = splash(); sp.save(os.path.join(OUT, 'splash.png')); sp.save(os.path.join(OUT, 'splash-dark.png'))
print('wrote', OUT, ic.mode, ic.size, sp.size)
