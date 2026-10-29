"""Game Center achievement badges (512x512, no alpha): a pixel-art medal per achievement, in the game's palette."""
import sys, os, math
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
OUT = sys.argv[1]


FONT5 = {  # 3x5 digits/letters for the badge label
 'A':['010','101','111','101','101'],'B':['110','101','110','101','110'],'C':['011','100','100','100','011'],'D':['110','101','101','101','110'],
 'E':['111','100','110','100','111'],'F':['111','100','110','100','100'],'G':['011','100','101','101','011'],'H':['101','101','111','101','101'],
 'I':['111','010','010','010','111'],'K':['101','110','100','110','101'],'L':['100','100','100','100','111'],'M':['101','111','111','101','101'],
 'N':['110','101','101','101','101'],'O':['010','101','101','101','010'],'P':['110','101','110','100','100'],'R':['110','101','110','101','101'],
 'S':['011','100','010','001','110'],'T':['111','010','010','010','010'],'U':['101','101','101','101','111'],'W':['101','101','111','111','101'],
 'Y':['101','101','010','010','010'],'0':['111','101','101','101','111'],'1':['010','110','010','010','111'],'3':['110','001','010','001','110'],
 '5':['111','100','110','001','110'],'8':['111','101','111','101','111'],' ':['000']*5,'-':['000','000','111','000','000'],
}
BADGES = [  # id, label, ribbon color, symbol
 ('first_td', 'FIRST TD', (255, 196, 40), 'ball'), ('first_pick', 'FIRST PICK', (90, 170, 255), 'hand'),
 ('first_win', 'FIRST WIN', (80, 210, 90), 'star'), ('game100', '100 YARDS', (255, 140, 40), 'num100'),
 ('hat_trick', 'HAT TRICK', (230, 70, 70), 'three'), ('pulls8', '8 PULLS', (250, 230, 40), 'flag'),
 ('shutout', 'SHUTOUT', (120, 120, 140), 'zero'), ('playoff_win', 'PLAYOFFS', (170, 90, 230), 'star'),
 ('champion', 'CHAMPION', (255, 215, 0), 'trophy'), ('td50', '50 TDS', (255, 120, 60), 'ball'),
 ('captain', 'CAPTAIN', (60, 200, 200), 'c'), ('hall_of_fame', 'HALL OF FAME', (255, 225, 74), 'trophy'),
]
def badge(label, col, sym, g=64):
    im = Image.new('RGB', (g, g), (16, 18, 40)); d = ImageDraw.Draw(im)
    for y in range(g):  # night gradient
        for x in range(g): im.putpixel((x, y), (16 + y // 4, 18 + y // 4, 40 + y // 2))
    cx, cy, r = 32, 26, 19
    d.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=(0, 0, 0))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    dark = tuple(int(c * 0.6) for c in col); light = tuple(min(255, int(c + (255 - c) * 0.5)) for c in col)
    d.ellipse([cx - r + 3, cy - r + 3, cx + r - 3, cy + r - 3], fill=dark)
    d.ellipse([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5], fill=col)
    d.arc([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5], 200, 300, fill=light, width=2)
    K, W = (0, 0, 0), (255, 255, 255)
    if sym == 'ball':
        d.ellipse([cx - 11, cy - 7, cx + 11, cy + 7], fill=K); d.ellipse([cx - 10, cy - 6, cx + 10, cy + 6], fill=(181, 100, 31))
        d.line([cx - 4, cy, cx + 4, cy], fill=W); [d.point((x, cy - 1), fill=W) for x in range(cx - 3, cx + 4, 2)]
        d.line([cx - 7, cy - 4, cx - 7, cy + 4], fill=W); d.line([cx + 7, cy - 4, cx + 7, cy + 4], fill=W)
    elif sym in ('star',):
        pts = [(cx + 12 * math.cos(math.pi / 2 + i * math.pi / 5) * (1 if i % 2 == 0 else 0.45), cy - 12 * math.sin(math.pi / 2 + i * math.pi / 5) * (1 if i % 2 == 0 else 0.45)) for i in range(10)]
        d.polygon(pts, fill=W, outline=K)
    elif sym == 'trophy':
        d.rectangle([cx - 9, cy - 10, cx + 9, cy + 1], fill=(255, 240, 150), outline=K); d.rectangle([cx - 2, cy + 1, cx + 2, cy + 7], fill=(255, 240, 150), outline=K)
        d.rectangle([cx - 7, cy + 7, cx + 7, cy + 10], fill=(255, 240, 150), outline=K); d.arc([cx - 14, cy - 9, cx - 6, cy - 1], 90, 270, fill=K); d.arc([cx + 6, cy - 9, cx + 14, cy - 1], 270, 90, fill=K)
    elif sym == 'flag':
        d.line([cx - 7, cy - 11, cx - 7, cy + 11], fill=K, width=2); d.polygon([(cx - 6, cy - 11), (cx + 10, cy - 6), (cx - 6, cy - 1)], fill=(255, 228, 0), outline=K)
    elif sym == 'hand':
        d.ellipse([cx - 11, cy - 7, cx + 11, cy + 7], fill=K); d.ellipse([cx - 10, cy - 6, cx + 10, cy + 6], fill=(181, 100, 31)); d.rectangle([cx - 3, cy - 12, cx + 3, cy - 4], fill=W, outline=K)
    else:
        txt = {'num100': '100', 'three': '3', 'zero': '0', 'c': 'C'}[sym]; s = 3 if len(txt) > 1 else 5
        w = (len(txt) * 4 - 1) * s; x0 = cx - w // 2; y0 = cy - (5 * s) // 2
        for i, ch in enumerate(txt):
            for gy, row in enumerate(FONT5[ch]):
                for gx, b in enumerate(row):
                    if b == '1': d.rectangle([x0 + (i * 4 + gx) * s, y0 + gy * s, x0 + (i * 4 + gx) * s + s - 1, y0 + gy * s + s - 1], fill=W, outline=None)
    # ribbon + label
    d.rectangle([4, 49, 59, 59], fill=K); d.rectangle([5, 50, 58, 58], fill=dark)
    s = 1; w = sum(4 for _ in label) - 1; x0 = 32 - w // 2
    for i, ch in enumerate(label):
        for gy, row in enumerate(FONT5.get(ch, FONT5[' '])):
            for gx, b in enumerate(row):
                if b == '1': im.putpixel((x0 + i * 4 + gx, 52 + gy), (255, 255, 255))
    return im.resize((512, 512), Image.NEAREST)
os.makedirs(OUT, exist_ok=True)
for bid, label, col, sym in BADGES: badge(label, col, sym).save(os.path.join(OUT, 'ach_' + bid + '.png'))
badge('LEGACY', (255, 225, 74), 'trophy').save(os.path.join(OUT, 'leaderboard_legacy.png'))
print('wrote', len(BADGES) + 1)
