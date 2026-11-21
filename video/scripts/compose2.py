# Dabrah 80s walkthrough, calm cut. Clips of filmed states (s2/), gentle camera, soft crossfades,
# smooth cursor, captions. Writes clean + captioned scene files, then concat.
import json, math, os, subprocess, sys, random
from collections import OrderedDict
from PIL import Image, ImageDraw, ImageFont, ImageFilter
Image.MAX_IMAGE_PIXELS = None
D = '/home/claude/proto/vid/'; SH = D + 's2/'; OUT = D + 'out2/'; os.makedirs(OUT, exist_ok=True)
W, H, FPS, K = 1920, 1080, 30, 3
NIGHT = (14, 26, 23); DEEP = (9, 17, 15); TEEN = (164, 100, 60); SAND = (227, 196, 143); JES = (241, 231, 214)
FD = '/root/.fonts/'; RAQM = ImageFont.Layout.RAQM
def kufam(sz, wt=700):
    f = ImageFont.truetype(FD + 'Kufam[wght].ttf', sz, layout_engine=RAQM)
    try: f.set_variation_by_axes([wt])
    except Exception: pass
    return f
def plex(sz, w='Bold'): return ImageFont.truetype(FD + f'IBMPlexSansArabic-{w}.ttf', sz, layout_engine=RAQM)
F_CAP = plex(44, 'Bold'); F_CHIP = plex(28, 'SemiBold'); F_TAG = kufam(76); F_SUB = plex(34, 'Medium')

def ease(p):
    p = max(0., min(1., p)); return 4*p*p*p if p < .5 else 1 - (-2*p+2)**3/2
def soft(p):  # sine in-out: calmer than cubic
    p = max(0., min(1., p)); return .5 - .5*math.cos(math.pi*p)
def lerp(a, b, p): return a + (b - a) * p
def keyed(keys, t, f=soft):
    if t <= keys[0][0]: return keys[0][1:]
    for (t0, *a), (t1, *b) in zip(keys, keys[1:]):
        if t <= t1:
            p = f((t - t0) / (t1 - t0)) if t1 > t0 else 1
            return tuple(lerp(x, y, p) for x, y in zip(a, b))
    return keys[-1][1:]

META = json.load(open(SH + 'meta.json'))
CROP = {'land': (0, 3000)}            # css y-range kept in memory for tall shots
for n in ['lv1', 'lv2', 'lv3', 'lv4', 'lv5', 'age0', 'age5', 'age9', 'age14']: CROP[n] = (3300, 4300)
_cache = OrderedDict()
def shot(n):
    if n in _cache: _cache.move_to_end(n); return _cache[n]
    im = Image.open(SH + n + '.jpg'); y0, y1 = CROP.get(n, (0, im.height / K))
    if n in CROP: im = im.crop((0, int(y0*K), im.width, int(min(y1*K, im.height))))
    im = im.convert('RGB'); _cache[n] = (im, y0)
    while len(_cache) > 6: _cache.popitem(last=False)
    return _cache[n]

def text_img(txt, font, fill):
    d = ImageDraw.Draw(Image.new('L', (1, 1)))
    l, t, r, b = d.textbbox((0, 0), txt, font=font, direction='rtl', language='ar')
    im = Image.new('RGBA', (r - l + 4, b - t + 4), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((2 - l, 2 - t), txt, font=font, fill=fill, direction='rtl', language='ar'); return im
def fade_a(im, a):
    if a >= 1: return im
    c = im.copy(); c.putalpha(c.getchannel('A').point(lambda v: int(v * max(0, a)))); return c

def make_cursor(h=40):
    s = 8; pts = [(0, 0), (0, 17), (4.3, 13.2), (7.3, 20), (10, 18.8), (7, 12.4), (12.6, 12.4)]; sc = s*h/22
    big = Image.new('RGBA', (int(16*sc), int(24*sc)), (0, 0, 0, 0)); P = [(sc + x*sc, sc + y*sc) for x, y in pts]
    sh = Image.new('RGBA', big.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).polygon([(x + 1.2*sc, y + 1.8*sc) for x, y in P], fill=(0, 0, 0, 90))
    big = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(1.8*sc)), big); d = ImageDraw.Draw(big)
    d.polygon(P, fill=(255, 255, 255, 255)); d.line(P + [P[0]], fill=(23, 19, 15, 255), width=int(1.4*sc), joint='curve')
    return big.resize((big.width // s, big.height // s), Image.LANCZOS)
CURSOR = make_cursor(); CUR_P = CURSOR.resize((int(CURSOR.width*.88), int(CURSOR.height*.88)), Image.LANCZOS)
def ripple(fr, x, y, p):
    if not 0 <= p <= 1: return
    ov = Image.new('RGBA', fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov); r = 12 + 40 * soft(p); a = int(200 * (1 - p))
    d.ellipse([x - r, y - r, x + r, y + r], fill=TEEN + (int(a * .25),), outline=TEEN + (a,), width=4); fr.alpha_composite(ov)
def spotlight(fr, box, a):
    x0, y0, x1, y1 = box; m = Image.new('L', fr.size, int(110 * a)); ImageDraw.Draw(m).rounded_rectangle([x0, y0, x1, y1], radius=28, fill=0)
    dark = Image.new('RGBA', fr.size, NIGHT + (0,)); dark.putalpha(m); fr.alpha_composite(dark)
    ov = Image.new('RGBA', fr.size, (0, 0, 0, 0)); ImageDraw.Draw(ov).rounded_rectangle([x0 - 3, y0 - 3, x1 + 3, y1 + 3], radius=30, outline=SAND + (int(200 * a),), width=4)
    fr.alpha_composite(ov)
_chips = {}
def chip(label):
    if label in _chips: return _chips[label]
    t = text_img(label, F_CHIP, JES); w, h = t.width + 86, 60
    im = Image.new('RGBA', (w + 30, h + 30), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([15, 19, 15 + w, 19 + h], 30, fill=(0, 0, 0, 70))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(8))); d = ImageDraw.Draw(im)
    d.rounded_rectangle([15, 15, 15 + w, 15 + h], 30, fill=NIGHT + (238,), outline=(255, 255, 255, 26), width=2)
    d.ellipse([15 + w - 44, 15 + h//2 - 8, 15 + w - 28, 15 + h//2 + 8], fill=TEEN)
    im.alpha_composite(t, (15 + 28, 15 + (h - t.height)//2 - 1)); _chips[label] = im; return im

def view(n, cx, cy, vw):
    im, oy = shot(n); ih = META[n]['h']; vh = vw * H / W
    cx = min(max(cx, vw/2), 1280 - vw/2) if vw <= 1280 else 640
    lo, hi = max(vh/2, oy + vh/2), min(ih, oy + im.height / K) - vh/2
    cy = min(max(cy, lo), hi) if hi >= lo else (lo + hi) / 2
    x0, y0 = cx - vw/2, cy - vh/2
    fr = im.resize((W, H), Image.BICUBIC, box=(x0*K, (y0 - oy)*K, (x0+vw)*K, (y0 - oy + vh)*K), reducing_gap=2.0).convert('RGBA')
    return fr, x0, y0, W / vw

class Clip:
    def __init__(s, name, dur, states, cam, cur=None, clicks=(), spots=(), role=None, trans='fade', tr=.45, caps=(), xf=.3):
        s.__dict__.update(locals()); del s.__dict__['s']
    def state_at(s, t):
        cur, prev, ts = s.states[0][1], None, -9
        for (t0, n) in s.states:
            if t >= t0: prev, cur, ts = cur, n, t0
        return cur, prev, ts
    def render(s, t):
        cx, cy, vw = keyed(s.cam, t)
        n, prev, ts = s.state_at(t)
        fr, x0, y0, S = view(n, cx, cy, vw)
        if prev and prev != n and t - ts < s.xf:
            pf = view(prev, cx, cy, vw)[0]; fr = Image.blend(pf, fr, soft((t - ts) / s.xf))
        to = lambda x, y: ((x - x0) * S, (y - y0) * S)
        for (t0, t1, bx) in s.spots:
            a = min(1, (t - t0) / .5, (t1 - t) / .5)
            if a > 0:
                X0, Y0 = to(bx[0], bx[1]); X1, Y1 = to(bx[0] + bx[2], bx[1] + bx[3]); spotlight(fr, (X0, Y0, X1, Y1), soft(a))
        if s.cur:
            px, py = keyed(s.cur, t); sx, sy = to(px, py)
            vis = min(1, (t - s.cur[0][0]) / .3, (s.cur[-1][0] + .4 - t) / .3) if t >= s.cur[0][0] else 0
            for c in s.clicks: ripple(fr, sx, sy, (t - c) / .6)
            if vis > 0:
                press = any(0 <= t - c < .14 for c in s.clicks)
                fr.alpha_composite(fade_a(CUR_P if press else CURSOR, vis), (int(sx - 5), int(sy - 5)))
        if s.role:
            c = chip(s.role); fr.alpha_composite(c, (14, H - c.height - 22))
        return fr

# ---------- transitions ----------
def tr_fade(A, B, p): return Image.blend(A, B, soft(p))
def tr_dip(A, B, p):  # through night: role changes / chapter breaks
    night = Image.new('RGBA', (W, H), NIGHT + (255,))
    return Image.blend(A, night, soft(p / .5)) if p < .5 else Image.blend(night, B, soft((p - .5) / .5))
def tr_black_in(A, B, p): return Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 255)), B, soft(p))
TR = {'fade': tr_fade, 'dip': tr_dip, 'black': tr_black_in}

# ---------- closing: fade to black, logo writes itself on, tagline ----------
LOGO = Image.open('/home/claude/proto/brand/logo-light.png').convert('RGBA')
random.seed(7); STARS = [(random.uniform(0, W), random.uniform(0, H*.75), random.uniform(.8, 2.2), random.uniform(0, 6.28)) for _ in range(90)]
class Closing:
    name = 'closing'; role = None; caps = ()
    def __init__(s, dur, trans='fade', tr=.9): s.dur, s.trans, s.tr = dur, trans, tr
    def render(s, t):
        fr = Image.new('RGBA', (W, H), (6, 11, 10, 255)); d = ImageDraw.Draw(fr)
        sa = soft((t - .6) / 1.2)
        for x, y, r, ph in STARS:
            a = int(sa * (90 + 70 * math.sin(t * 1.1 + ph))); d.ellipse([x - r, y - r, x + r, y + r], fill=JES + (a,))
        lw = 620; lg = LOGO.resize((lw, int(LOGO.height * lw / LOGO.width)), Image.LANCZOS)
        lx, ly = (W - lw) // 2, 250
        p = (t - .9) / 1.7                            # write-on from right to left (Arabic stroke direction)
        if p > 0:
            q = soft(min(1, p)); edge = lw * (1 - q)
            m = Image.new('L', lg.size, 0); md = ImageDraw.Draw(m)
            md.rectangle([min(edge + 40, lw), 0, lw, lg.height], fill=255) if edge + 40 < lw else None
            for i in range(40): md.line([(edge + i, 0), (edge + i, lg.height)], fill=int(255 * i / 40))
            a = Image.composite(lg.getchannel('A'), Image.new('L', lg.size, 0), m); g = lg.copy(); g.putalpha(a)
            glow = g.filter(ImageFilter.GaussianBlur(18)); glow = fade_a(glow, .55 * (1 - soft((p - 1) / .8)) if p > 1 else .55)
            fr.alpha_composite(glow, (lx, ly)); fr.alpha_composite(g, (lx, ly))
            if q < 1:                                   # pen light at the writing edge
                gx, gy = lx + edge + 20, ly + lg.height * (.45 + .18 * math.sin(p * 9))
                ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
                for rr, aa in ((26, 40), (14, 90), (6, 230)): od.ellipse([gx - rr, gy - rr, gx + rr, gy + rr], fill=SAND + (aa,))
                fr.alpha_composite(ov.filter(ImageFilter.GaussianBlur(3)))
        b = soft((t - 2.7) / .9)
        if b > 0:
            tg = text_img('لا تسأل عن الخبرة… اسأل عن الدبره', F_TAG, SAND)
            fr.alpha_composite(fade_a(tg, b), ((W - tg.width) // 2, 650 + int((1 - b) * 18)))
        c = soft((t - 3.5) / .8)
        if c > 0:
            sb = text_img('ترقيتك على مهارتك، مو على سنينك', F_SUB, JES)
            fr.alpha_composite(fade_a(sb, c * .85), ((W - sb.width) // 2, 790))
        e = soft((t - (s.dur - .7)) / .7)
        if e > 0: fr = Image.blend(fr, Image.new('RGBA', (W, H), (0, 0, 0, 255)), e)
        return fr

# ---------- storyboard (all coordinates are CSS px of the filmed page) ----------
E, M, HY, T = 'عبدالله · موظف', 'محمد · مدير مباشر', 'هيا · تطوير المواهب', 'فيصل · إدارة عليا'
def lvx(v): return 600 - 511 * v / 14     # RTL range slider: thumb x for value v
CL = [
 Clip('hero', 4.0, [(0, 'land')], [(0, 640, 790, 1280), (4.0, 640, 780, 1180)], trans='black', tr=.8,
      caps=[(.6, 3.9, 'هذي دبره… الترقية فيها بالمهارة، مو بالسنين.')]),
 Clip('problem', 3.5, [(0, 'land')], [(0, 640, 1500, 1280), (3.5, 660, 1480, 1200)],
      caps=[(.3, 3.4, 'عبدالله سنع بشغله… بس محد داري عنه.')]),
 Clip('meaning', 3.0, [(0, 'land')], [(0, 640, 2380, 1280), (3.0, 640, 2390, 1160)],
      caps=[(.3, 2.9, '«دبره» بلهجتنا: الشخص اللي يُعتمد عليه.')]),
 Clip('levels', 5.5, [(0, 'lv1'), (1.0, 'lv2'), (1.7, 'lv3'), (2.4, 'lv4'), (3.1, 'lv5'), (4.0, 'age5'), (4.45, 'age9'), (4.9, 'age14')],
      [(0, 640, 3800, 1280), (5.5, 640, 3810, 1220)],
      cur=[(.2, 900, 4120), (.75, 803, 4046), (3.2, 803, 4046), (3.65, lvx(2), 3831), (3.8, lvx(2), 3831), (5.0, lvx(14), 3831), (5.4, lvx(14), 3831)],
      clicks=[.85, 1.55, 2.25, 2.95],
      caps=[(.2, 3.4, 'كل مهارة لها خمس درجات… من مبتدئ إلى دبره.'), (3.5, 5.4, 'ولها عمر: اللي ما تستخدمها تذبل.')]),
 Clip('login', 3.0, [(0, 'login0'), (.9, 'login1')], [(0, 640, 360, 1280), (.9, 640, 360, 1280), (1.0, 640, 440, 1180), (3.0, 640, 450, 1160)],
      cur=[(.1, 700, 560), (.65, 944, 400), (1.15, 600, 380), (1.6, 375, 327), (2.2, 330, 700), (2.55, 318, 760), (2.9, 318, 760)],
      clicks=[.75, 1.7, 2.65], caps=[(.2, 2.9, 'يختار دوره… ويدخل بثواني.')]),
 # ---- employee ----
 Clip('palm', 3.0, [(0, 'palm2'), (.7, 'palm8'), (1.4, 'palm17'), (2.1, 'palm26')], [(0, 640, 410, 1180), (3.0, 600, 410, 1080)],
      spots=[(.2, 3.0, (88, 186, 425, 456))], role=E, trans='dip', tr=.7, xf=.4,
      caps=[(.3, 2.9, 'نخلته تكبر مع التزامه، وتقيس استمراريته.')]),
 Clip('challenge', 6.0, [(0, 'path0'), (.8, 'case0'), (2.0, 'case1'), (3.0, 'case2'), (3.85, 'caseS'), (4.6, 'celeb')],
      [(0, 640, 410, 1180), (.8, 640, 360, 1280), (6.0, 640, 360, 1260)],
      cur=[(.1, 900, 600), (.55, 1084, 547), (1.3, 1084, 600), (1.7, 785, 679), (2.6, 785, 679), (3.4, 991, 652), (4.1, 831, 679), (5.0, 700, 560)],
      clicks=[.65, 1.8, 2.75, 3.6, 4.4], role=E,
      caps=[(.2, 3.0, 'عنده مهارة بلا شهادة؟ يثبتها بتحدي من شغله.'), (3.1, 5.9, 'يحلّه… وتطلع له التهنئة ويرتفع مستواه.')]),
 Clip('cert', 4.0, [(0, 'cert0'), (1.2, 'cert1b'), (2.6, 'cert2')], [(0, 640, 360, 1280), (4.0, 640, 360, 1260)],
      cur=[(.2, 700, 560), (.85, 813, 679), (1.6, 900, 500), (2.2, 784, 679), (3.6, 760, 600)], clicks=[.95, 2.35], role=E,
      caps=[(.2, 3.9, 'وعنده شهادة خارجية؟ يختبر عليها وتنضاف.')]),
 Clip('glance', 2.5, [(0, 'path1')], [(0, 640, 820, 1180), (2.5, 640, 1420, 1180)], role=E,
      caps=[(.1, 2.4, 'دورته، وجداراته، وطريقه للترقية.')]),
 Clip('perf', 3.0, [(0, 'perf')], [(0, 640, 400, 1180), (1.0, 640, 1160, 1060), (3.0, 640, 1180, 1000)],
      spots=[(1.0, 3.0, (88, 1060, 1103, 320))], role=E, caps=[(.5, 2.9, 'وتقييم 360 يقيس سلوكه بشهادة اللي حوله.')]),
 Clip('learn', 3.0, [(0, 'learn')], [(0, 640, 680, 1180), (3.0, 640, 1080, 1180)], role=E,
      caps=[(.1, 2.9, 'ويتعلّم مجانًا: مرشد، ومحتوى شركته، وورش ودورات.')]),
 Clip('jobs', 3.0, [(0, 'jobs')], [(0, 640, 430, 1180), (3.0, 640, 440, 1080)], role=E,
      caps=[(.1, 2.9, 'وفرص داخلية تطابق مهاراته بتحليل الذكاء الاصطناعي.')]),
 # ---- manager ----
 Clip('garden', 4.7, [(0, 'mteam'), (1.25, 'mpal'), (3.0, 'mteam')], [(0, 640, 420, 1180), (3.2, 640, 420, 1180), (4.4, 640, 1600, 1180), (4.7, 640, 1610, 1180)],
      cur=[(.4, 800, 560), (1.0, 1088, 450), (2.9, 1088, 450)], clicks=[1.1], role=M, trans='dip', tr=.7,
      caps=[(.2, 1.6, 'محمد، المدير المباشر، يشوف حديقة قسمه،'), (1.7, 3.3, 'وكل نخلة تعرض عبء الموظف وجاهزيته وجداراته.'), (3.4, 4.6, 'وأبطال الأقسام والمهارات.')]),
 Clip('load', 4.0, [(0, 'mperf0'), (2.3, 'mperf1')], [(0, 640, 880, 1180), (4.0, 640, 890, 1140)],
      cur=[(.3, 400, 900), (.8, 175, 727), (1.3, 175, 936), (1.8, 175, 1146), (2.4, 600, 1000), (3.6, 760, 860)], clicks=[.9, 1.4, 1.9], role=M, xf=.5,
      caps=[(.2, 1.9, 'يحلّل عبء العمل ويقترح تدوير وظيفي،'), (2.0, 3.9, 'ولو اعتمد الاقتراحات… يتوازن العبء.')]),
 Clip('know', 1.4, [(0, 'mknow')], [(0, 640, 470, 1180), (1.4, 640, 470, 1140)], role=M),
 Clip('budget', 1.4, [(0, 'mbudget')], [(0, 640, 380, 1180), (1.4, 640, 380, 1140)], role=M),
 # ---- haya ----
 Clip('ready', 4.0, [(0, 'htalent0'), (.9, 'hready'), (2.5, 'htalent0')], [(0, 640, 380, 1180), (2.6, 640, 380, 1180), (3.8, 640, 1010, 1180), (4.0, 640, 1015, 1180)],
      cur=[(.15, 760, 420), (.7, 560, 300), (2.3, 560, 300)], clicks=[.8], role=HY, trans='dip', tr=.7,
      caps=[(.2, 2.5, 'هيا من التطوير: تعرف مين الجاهز للترقية.')]),
 Clip('needs', 2.5, [(0, 'hneeds')], [(0, 640, 690, 1180), (2.5, 640, 700, 1120)], role=HY,
      caps=[(.1, 2.4, 'والنظام يقترح: توظيف داخلي، أو إيقاف، أو خارجي.')]),
 Clip('plan', 2.5, [(0, 'hplan0'), (1.1, 'hplan1')], [(0, 880, 330, 1000), (2.5, 880, 330, 960)],
      cur=[(.2, 900, 480), (.85, 1099, 328), (2.3, 1099, 328)], clicks=[.95], role=HY,
      caps=[(.1, 2.4, 'وتبني خطة تطوير… والسعوديين أولًا.')]),
 Clip('gov', 2.5, [(0, 'hgov')], [(0, 640, 560, 1180), (2.5, 640, 980, 1180)], role=HY,
      caps=[(.1, 2.4, 'وتتحكم بأوزان الجدارات، ويرصد النظام أي تحيّز بالتقييم.')]),
 # ---- top management ----
 Clip('exc', 2.0, [(0, 'tfiles0'), (1.0, 'tfiles1')], [(0, 640, 520, 1180), (2.0, 660, 560, 1100)],
      cur=[(.15, 900, 600), (.75, 1121, 731), (1.9, 1121, 731)], clicks=[.85], role=T, trans='dip', tr=.7,
      caps=[(.2, 1.9, 'فيصل يعتمد الترقية الاستثنائية،')]),
 Clip('plans', 2.0, [(0, 'tplans0'), (1.0, 'tplans1')], [(0, 640, 380, 1180), (2.0, 640, 380, 1120)],
      cur=[(.1, 500, 600), (.7, 259, 496), (1.9, 259, 496)], clicks=[.8], role=T,
      caps=[(.1, 1.9, 'ويعتمد خطط التطوير،')]),
 Clip('champs', 2.0, [(0, 'tchamps')], [(0, 640, 480, 1180), (2.0, 640, 470, 1100)], role=T,
      caps=[(.1, 1.9, 'ويشوف أبطال كل قسم وكل مهارة،')]),
 Clip('board', 2.0, [(0, 'tover')], [(0, 640, 420, 1180), (2.0, 640, 420, 1100)], role=T,
      caps=[(.1, 1.9, 'ولوحة أداء الشركة كاملة.')]),
 Closing(5.5, trans='fade', tr=.9),
]
SCRIPT_END = (74.9, 79.5, 'دبره… لا تسأل عن الخبرة، اسأل عن الدبره.')

_capimg = {}
def cap_img(txt):
    if txt in _capimg: return _capimg[txt]
    t = text_img(txt, F_CAP, JES); w, h = t.width + 104, t.height + 48
    im = Image.new('RGBA', (w + 40, h + 40), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([20, 26, 20 + w, 26 + h], 28, fill=(0, 0, 0, 100))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(10))); d = ImageDraw.Draw(im)
    d.rounded_rectangle([20, 20, 20 + w, 20 + h], 28, fill=NIGHT + (232,))
    d.rounded_rectangle([20 + w - 15, 20 + 16, 20 + w - 8, 20 + h - 16], 4, fill=TEEN)
    im.alpha_composite(t, (20 + 46, 20 + 22)); _capimg[txt] = im; return im

def starts():
    T0, out = 0, []
    for c in CL: out.append(T0); T0 += c.dur
    return out, T0
def all_caps():
    st, _ = starts(); return [(st[i] + a, st[i] + b, txt) for i, c in enumerate(CL) for (a, b, txt) in c.caps]
CAPS = all_caps()
def add_caption(fr, T):
    for a, b, txt in CAPS:
        if a <= T <= b:
            al = min(1, (T - a) / .2, (b - T) / .2); c = fade_a(cap_img(txt), soft(al))
            fr.alpha_composite(c, ((W - c.width)//2, H - c.height - 30))

def frame_at(i, t):
    c = CL[i]; fr = c.render(t)
    if c.trans and t < c.tr:
        A = CL[i-1].render(CL[i-1].dur + t) if i > 0 else None; fr = TR[c.trans](A, fr, t / c.tr)
    return fr

def enc(path):
    return subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '17', '-pix_fmt', 'yuv420p', '-r', str(FPS), path], stdin=subprocess.PIPE)

def render(only=None, stills=None):
    st, total = starts()
    if stills:
        for T in stills:
            i = max(k for k in range(len(CL)) if st[k] <= T); fr = frame_at(i, T - st[i]); add_caption(fr, T)
            fr.convert('RGB').save(OUT + f'still_{T:05.2f}.jpg', quality=88)
        return
    for i, c in enumerate(CL):
        if only is not None and i not in only: continue
        n = round((st[i] + c.dur) * FPS) - round(st[i] * FPS)
        pc, pv = enc(OUT + f'c{i:02d}.tmp.mp4'), enc(OUT + f'v{i:02d}.tmp.mp4')
        for f in range(n):
            t = f / FPS; fr = frame_at(i, t); pc.stdin.write(fr.convert('RGB').tobytes())
            add_caption(fr, st[i] + t); pv.stdin.write(fr.convert('RGB').tobytes())
        for p_, nm in ((pc, 'c'), (pv, 'v')):
            p_.stdin.close(); assert p_.wait() == 0; os.replace(OUT + f'{nm}{i:02d}.tmp.mp4', OUT + f'{nm}{i:02d}.mp4')
        print('clip', i, c.name, flush=True)

if __name__ == '__main__':
    if sys.argv[1] == 'stills': render(stills=[float(x) for x in sys.argv[2:]])
    elif sys.argv[1] == 'times':
        st, tot = starts(); print(tot); [print(f'{s:6.2f} {c.name}') for s, c in zip(st, CL)]
    else: render(only=[int(x) for x in sys.argv[2:]] or None)
