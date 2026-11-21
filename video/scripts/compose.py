# Dabrah 60s walkthrough — composes filmed screenshots with camera moves, cursor, spotlights,
# transitions, role chips and captions. Writes two versions per scene (clean + captioned), then concats.
import json, math, os, subprocess, sys, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
Image.MAX_IMAGE_PIXELS = None
D = '/home/claude/proto/vid/'; SH = D + 'shots/'; OUT = D + 'out/'; os.makedirs(OUT, exist_ok=True)
W, H, FPS, K = 1920, 1080, 30, 2.5
NIGHT = (14, 26, 23); TEEN = (164, 100, 60); SAND = (227, 196, 143); JES = (241, 231, 214)
FD = '/root/.fonts/'
RAQM = ImageFont.Layout.RAQM
def kufam(sz, wt=700):
    f = ImageFont.truetype(FD + 'Kufam[wght].ttf', sz, layout_engine=RAQM)
    try: f.set_variation_by_axes([wt])
    except Exception: pass
    return f
def plex(sz, w='Bold'): return ImageFont.truetype(FD + f'IBMPlexSansArabic-{w}.ttf', sz, layout_engine=RAQM)
F_CAP = plex(46, 'Bold'); F_CHIP = plex(30, 'SemiBold'); F_ROLE = kufam(128); F_ROLE2 = plex(46, 'Medium'); F_SMALL = plex(32, 'Medium')

def ease(p):
    p = max(0., min(1., p)); return 4*p*p*p if p < .5 else 1 - (-2*p+2)**3/2
def lerp(a, b, p): return a + (b - a) * p
def keyed(keys, t):
    """keys: [(t, *vals)] -> eased interpolation; holds outside range."""
    if t <= keys[0][0]: return keys[0][1:]
    for (t0, *a), (t1, *b) in zip(keys, keys[1:]):
        if t <= t1:
            p = ease((t - t0) / (t1 - t0)) if t1 > t0 else 1
            return tuple(lerp(x, y, p) for x, y in zip(a, b))
    return keys[-1][1:]

_img = {}
def shot(n):
    if n not in _img: _img[n] = Image.open(SH + n + '.jpg').convert('RGB')
    return _img[n]

def text_img(txt, font, fill, pad=(0, 0)):
    d = ImageDraw.Draw(Image.new('L', (1, 1)))
    l, t, r, b = d.textbbox((0, 0), txt, font=font, direction='rtl', language='ar')
    im = Image.new('RGBA', (r - l + 2*pad[0], b - t + 2*pad[1]), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((pad[0] - l, pad[1] - t), txt, font=font, fill=fill, direction='rtl', language='ar')
    return im

# ---------- cursor / ripple ----------
def make_cursor(h=44):
    s = 8; pts = [(0, 0), (0, 17), (4.3, 13.2), (7.3, 20), (10, 18.8), (7, 12.4), (12.6, 12.4)]
    big = Image.new('RGBA', (int(16*s*h/22), int(24*s*h/22)), (0, 0, 0, 0)); sc = s*h/22
    P = [(2*sc/2 + x*sc, 2*sc/2 + y*sc) for x, y in pts]
    sh = Image.new('RGBA', big.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).polygon([(x + 1.5*sc, y + 2*sc) for x, y in P], fill=(0, 0, 0, 110))
    sh = sh.filter(ImageFilter.GaussianBlur(1.6*sc))
    d = ImageDraw.Draw(big); big = Image.alpha_composite(sh, big); d = ImageDraw.Draw(big)
    d.polygon(P, fill=(255, 255, 255, 255)); d.line(P + [P[0]], fill=(23, 19, 15, 255), width=int(1.5*sc), joint='curve')
    return big.resize((big.width // s, big.height // s), Image.LANCZOS)
CURSOR = make_cursor()

def draw_ripple(fr, x, y, p):
    if not 0 <= p <= 1: return
    ov = Image.new('RGBA', fr.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    r = 14 + 58 * ease(p); a = int(255 * (1 - p))
    d.ellipse([x - r, y - r, x + r, y + r], fill=TEEN + (int(a * .28),), outline=TEEN + (a,), width=5)
    fr.alpha_composite(ov)

def spotlight(fr, box, a):
    if a <= 0: return
    x0, y0, x1, y1 = box; m = Image.new('L', fr.size, int(150 * a)); d = ImageDraw.Draw(m)
    d.rounded_rectangle([x0, y0, x1, y1], radius=26, fill=0)
    dark = Image.new('RGBA', fr.size, NIGHT + (0,)); dark.putalpha(m); fr.alpha_composite(dark)
    ov = Image.new('RGBA', fr.size, (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle([x0 - 4, y0 - 4, x1 + 4, y1 + 4], radius=30, outline=SAND + (int(235 * a),), width=5)
    fr.alpha_composite(ov)

def chip(label):
    t = text_img(label, F_CHIP, JES); w, h = t.width + 92, 66
    im = Image.new('RGBA', (w + 30, h + 30), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([15, 19, 15 + w, 19 + h], 33, fill=(0, 0, 0, 90))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(8))); d = ImageDraw.Draw(im)
    d.rounded_rectangle([15, 15, 15 + w, 15 + h], 33, fill=NIGHT + (235,), outline=(255, 255, 255, 30), width=2)
    d.ellipse([15 + w - 46, 15 + h//2 - 9, 15 + w - 28, 15 + h//2 + 9], fill=TEEN)
    im.alpha_composite(t, (15 + 30, 15 + (h - t.height)//2 - 2)); return im
_chips = {}

# ---------- scenes ----------
class Scene:
    def __init__(s, name, src, dur, cam, cur=None, clicks=(), spots=(), role=None, trans=None, tr=0.0, view_h=None, extra=None):
        s.name, s.src, s.dur, s.cam, s.cur, s.clicks, s.spots, s.role, s.trans, s.tr = name, src, dur, cam, cur, clicks, spots, role, trans, tr
        s.extra = extra
    def render(s, t):
        img = shot(s.src); ih = img.height / K
        cx, cy, vw = keyed(s.cam, t); vh = vw * H / W
        cx = min(max(cx, vw/2), 1280 - vw/2) if vw <= 1280 else 640
        cy = min(max(cy, vh/2), ih - vh/2) if vh <= ih else ih/2
        x0, y0 = cx - vw/2, cy - vh/2
        fr = img.resize((W, H), Image.BICUBIC, box=(x0*K, y0*K, (x0+vw)*K, (y0+vh)*K), reducing_gap=2.0).convert('RGBA')
        S = W / vw; to = lambda x, y: ((x - x0) * S, (y - y0) * S)
        if s.extra: s.extra(fr, t)
        for (t0, t1, bx) in s.spots:
            a = min(1, (t - t0)/.35, (t1 - t)/.35)
            if a > 0:
                X0, Y0 = to(bx[0], bx[1]); X1, Y1 = to(bx[0] + bx[2], bx[1] + bx[3]); spotlight(fr, (X0, Y0, X1, Y1), ease(a))
        if s.cur:
            px, py = keyed(s.cur, t); sx, sy = to(px, py)
            vis = min(1, (t - s.cur[0][0]) / .25) if t >= s.cur[0][0] else 0
            for c in s.clicks: draw_ripple(fr, sx, sy, (t - c) / .55)
            if vis > 0:
                press = any(0 <= t - c < .16 for c in s.clicks); cimg = CURSOR
                if press: cimg = CURSOR.resize((int(CURSOR.width*.86), int(CURSOR.height*.86)), Image.LANCZOS)
                if vis < 1: cimg = cimg.copy(); cimg.putalpha(cimg.getchannel('A').point(lambda v: int(v*vis)))
                fr.alpha_composite(cimg, (int(sx - 6), int(sy - 6)))
        if s.role:
            if s.role not in _chips: _chips[s.role] = chip(s.role)
            c = _chips[s.role]; a = min(1, max(0, (t - s.tr - .1) / .35))
            if a > 0:
                cc = c.copy(); cc.putalpha(cc.getchannel('A').point(lambda v: int(v * a)))
                fr.alpha_composite(cc, (W - c.width - 26, 22 + int((1 - ease(a)) * -20)))
        return fr

# ---------- transitions ----------
def tr_fade(A, B, p): return Image.blend(A, B, ease(p))
def tr_zoom(A, B, p):
    e = ease(p); za = 1 + .22 * e
    a = A.resize((int(W*za), int(H*za)), Image.BILINEAR).crop((int((W*za - W)/2), int((H*za - H)/2), int((W*za - W)/2) + W, int((H*za - H)/2) + H))
    zb = .9 + .1 * e
    b = B.resize((int(W*zb), int(H*zb)), Image.BILINEAR); bb = Image.new('RGBA', (W, H), NIGHT + (255,)); bb.paste(b, ((W - b.width)//2, (H - b.height)//2))
    return Image.blend(a, bb, e)
def _hblur(im, k):
    if k < 2: return im
    return Image.blend(im, im.resize((max(8, int(W / k)), H), Image.BILINEAR).resize((W, H), Image.BILINEAR), .85)
def tr_whip(A, B, p):
    e = ease(p); dx = int(W * e); blur = 1 + 26 * math.sin(math.pi * p)
    fr = Image.new('RGBA', (W, H), NIGHT + (255,))
    fr.paste(_hblur(A, blur), (dx, 0)); fr.paste(_hblur(B, blur), (dx - W, 0)); return fr
_wipe_txt = {}
def make_wipe(title, sub):
    def f(A, B, p):
        key = title
        if key not in _wipe_txt: _wipe_txt[key] = (text_img(title, F_ROLE, JES), text_img(sub, F_ROLE2, SAND))
        T1, T2 = _wipe_txt[key]
        base = (A if p < .5 else B).copy()
        if p < .42: L = lerp(W + 200, -120, ease(p / .42))
        elif p < .6: L = -120
        else: L = lerp(-120, -W - 420, ease((p - .6) / .4))
        R = L + W + 320; sk = 160
        ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        d.polygon([(L + sk, 0), (R + sk, 0), (R, H), (L, H)], fill=NIGHT + (255,))
        d.polygon([(L + sk - 34, 0), (L + sk, 0), (L, H), (L - 34, H)], fill=TEEN + (255,))
        d.polygon([(R + sk, 0), (R + sk + 22, 0), (R + 22, H), (R, H)], fill=SAND + (255,))
        base.alpha_composite(ov)
        tp = min(1, max(0, (p - .3) / .18)) * min(1, max(0, (.78 - p) / .14))
        if tp > 0:
            off = int((1 - ease(min(1, (p - .3) / .18))) * 60)
            for im, y in ((T1, H//2 - 120), (T2, H//2 + 60)):
                c = im.copy(); c.putalpha(c.getchannel('A').point(lambda v: int(v * tp)))
                base.alpha_composite(c, ((W - im.width)//2 + off, y))
        return base
    return f

# ---------- storyboard (CSS px of each shot) ----------
LOGO = Image.open('/home/claude/proto/brand/logo-light.png').convert('RGBA')
def closing_extra(fr, t):
    a = ease(min(1, max(0, (t - .5) / .9)))
    if a <= 0: return
    dark = Image.new('RGBA', fr.size, NIGHT + (int(35 * a),)); fr.alpha_composite(dark)
    lg = LOGO.resize((int(300 * (0.92 + .08*a)), int(141 * (0.92 + .08*a))), Image.LANCZOS)
    lg.putalpha(lg.getchannel('A').point(lambda v: int(v * a)))
    fr.alpha_composite(lg, ((W - lg.width)//2, 70))
    b = 0
    if b > 0:
        s = text_img('مهاراثون 2026 · مسيرة للمستقبل', F_SMALL, SAND); s.putalpha(s.getchannel('A').point(lambda v: int(v * b)))
        fr.alpha_composite(s, ((W - s.width)//2, H - 120))

SC = [
 Scene('land', 'land', 11.0,
   cam=[(0, 640, 760, 640), (3.8, 640, 790, 1280), (4.5, 640, 790, 1280), (5.7, 760, 1460, 1280), (7.0, 1040, 1385, 760), (8.0, 1030, 1390, 740),
        (9.0, 640, 2470, 1280), (11.0, 640, 2520, 1120)],
   cur=[(9.0, 960, 2780), (9.7, 790, 2560), (11, 790, 2560)], clicks=[9.9],
   spots=[(7.0, 8.0, (860, 1318, 385, 132))]),
 Scene('login0', 'login0', 2.1, cam=[(0, 640, 360, 1280), (2.1, 700, 380, 940)],
   cur=[(0.15, 640, 620), (1.2, 944, 400), (2.1, 944, 400)], clicks=[1.4], trans=tr_zoom, tr=.6),
 Scene('login1', 'login1', 2.1, cam=[(0, 640, 360, 1280), (2.1, 560, 340, 980)],
   cur=[(0, 944, 420), (1.0, 375, 325), (2.1, 375, 325)], clicks=[1.2], trans=tr_fade, tr=.35),
 Scene('emp-path', 'emp-path', 9.8,
   cam=[(0, 640, 360, 1280), (1.0, 640, 360, 1280), (2.4, 650, 300, 640), (3.8, 655, 305, 610), (4.8, 300, 420, 720), (6.4, 300, 410, 690),
        (7.5, 760, 1450, 1000), (9.8, 760, 1440, 900)],
   cur=[(1.6, 900, 560), (2.5, 690, 330), (4.0, 690, 330), (5.0, 430, 512), (6.6, 430, 512), (7.6, 600, 1300), (8.4, 520, 1378), (9.8, 520, 1378)],
   clicks=[5.3, 8.6], spots=[(2.5, 4.1, (553, 206, 166, 166)), (4.9, 6.6, (89, 189, 422, 455)), (7.8, 9.8, (110, 1330, 1060, 330))],
   role='عبدالله · موظف', trans=make_wipe('عبدالله', 'الموظف'), tr=1.0),
 Scene('emp-learn', 'emp-learn', 4.4, cam=[(0, 860, 600, 1000), (1.7, 860, 600, 960), (2.6, 640, 1250, 1100), (4.4, 640, 1290, 1040)],
   cur=[(0.4, 880, 760), (1.1, 1069, 611), (2.3, 600, 900), (2.9, 172, 1115), (4.4, 172, 1115)], clicks=[1.3, 3.2],
   role='عبدالله · موظف', trans=tr_whip, tr=.45),
 Scene('mgr-team', 'mgr-team', 7.6,
   cam=[(0, 640, 400, 1180), (1.0, 640, 400, 1180), (2.4, 640, 470, 900), (4.0, 660, 475, 860), (4.9, 860, 835, 800), (7.6, 860, 830, 740)],
   cur=[(2.4, 900, 640), (3.3, 1089, 470), (4.6, 1089, 470), (5.6, 1136, 718), (7.6, 1136, 718)], clicks=[3.5],
   spots=[(2.5, 4.4, (88, 342, 1103, 260)), (5.1, 7.6, (533, 622, 658, 422))],
   role='محمد · مدير مباشر', trans=make_wipe('محمد', 'المدير المباشر'), tr=1.0),
 Scene('mgr-know', 'mgr-know', 4.6, cam=[(0, 640, 380, 1280), (1.0, 700, 520, 900), (4.6, 690, 520, 860)],
   cur=[(1.1, 700, 640), (2.0, 1124, 452), (2.6, 1124, 452), (3.3, 167, 444), (4.6, 167, 444)], clicks=[3.5],
   spots=[(1.5, 3.0, (110, 395, 1060, 100))], role='محمد · مدير مباشر', trans=tr_whip, tr=.45),
 Scene('mgr-perf', 'mgr-perf', 3.4, cam=[(0, 640, 640, 1100), (1.4, 640, 800, 1000), (3.4, 620, 820, 950)],
   cur=[(1.0, 700, 900), (2.0, 173, 724), (3.4, 173, 724)], clicks=[2.3],
   spots=[(0.5, 1.6, (533, 544, 658, 723)), (1.7, 3.4, (89, 544, 422, 723))], role='محمد · مدير مباشر', trans=tr_whip, tr=.45),
 Scene('haya-dev', 'haya-dev', 5.0, cam=[(0, 900, 380, 1060), (1.0, 900, 380, 1060), (4.0, 900, 360, 860), (5.0, 900, 360, 830)],
   cur=[(2.2, 1000, 520), (3.3, 673, 679), (5.0, 673, 679)], clicks=[3.6],
   role='هيا · تطوير', trans=make_wipe('هيا', 'التدريب والتطوير'), tr=1.0),
 Scene('top-files', 'top-files', 3.3, cam=[(0, 640, 470, 1100), (1.0, 640, 470, 1100), (3.3, 720, 560, 860)],
   cur=[(1.3, 900, 760), (2.1, 1100, 530), (3.3, 1090, 532)],
   spots=[(1.5, 3.3, (700, 500, 470, 60))], role='فيصل · إدارة عليا', trans=make_wipe('فيصل', 'الإدارة العليا'), tr=1.0),
 Scene('top-champs', 'top-champs', 2.6, cam=[(0, 640, 400, 1200), (2.6, 640, 560, 1100)],
   role='فيصل · إدارة عليا', trans=tr_whip, tr=.45),
 Scene('closing', 'land', 4.1, cam=[(0, 640, 800, 1280), (4.1, 640, 780, 1120)], trans=tr_zoom, tr=.7, extra=closing_extra),
]
CAPS = [
 (0.3, 4.2, 'بكل مستودع ومصنع فيه ناس شاطرين… بس محد داري عنهم.'),
 (4.4, 7.9, 'مثل عبدالله: سنع بشغله، بس ما يدري وش يرقّيه.'),
 (8.1, 10.9, 'دبره تخلّي ترقيتك على مهارتك، مو على سنواتك.'),
 (11.2, 15.0, 'كل واحد يدخل بدوره: موظف، مدير، تطوير، أو إدارة عليا.'),
 (16.2, 18.7, 'عبدالله يشوف جاهزيته للترقية… ووش باقي عليه بالضبط.'),
 (18.8, 21.8, 'ونخلته تكبر مع كل سعفة التزام.'),
 (22.0, 24.9, 'وكل جدارة بيت نجدي… عدد مثلثاته هو مستواه.'),
 (25.1, 29.2, 'يتعلم من أهل الدبره، ويسجّل بالورش والدورات بضغطة.'),
 (30.4, 33.6, 'محمد مديره يشوف فريقه حديقة نخل… كل نخلة موظف.'),
 (33.8, 36.9, 'والاعتمادات تجي تلقائية بالأدلة، ودوره بس المقابلة.'),
 (37.1, 41.5, 'ويكشف المعرفة اللي عند شخص واحد، ويبدأ لها ظِل.'),
 (41.7, 44.9, 'ويوزّع العبء بالتدوير قبل لا ينضغط أحد.'),
 (46.0, 49.9, 'وهيا تشوف الفجوات بالأرقام، وتبني خطة تطوير بميزانيتها.'),
 (51.0, 53.2, 'وأي رفض يوصل الإدارة العليا مع سببه،'),
 (53.4, 55.8, 'ويكرّمون أبطال الأقسام وموظف الشهر.'),
 (56.2, 59.8, 'دبره… لا تسأل عن الخبرة، اسأل عن الدبره.'),
]
CAP_ON_SCREEN = CAPS[:-1]   # last line is already on screen (hero headline)
_capimg = {}
def cap_img(txt):
    if txt in _capimg: return _capimg[txt]
    t = text_img(txt, F_CAP, JES); w, h = t.width + 110, t.height + 52
    im = Image.new('RGBA', (w + 40, h + 40), (0, 0, 0, 0))
    sh = Image.new('RGBA', im.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).rounded_rectangle([20, 26, 20 + w, 26 + h], 30, fill=(0, 0, 0, 110))
    im = Image.alpha_composite(im, sh.filter(ImageFilter.GaussianBlur(10))); d = ImageDraw.Draw(im)
    d.rounded_rectangle([20, 20, 20 + w, 20 + h], 30, fill=NIGHT + (228,))
    d.rounded_rectangle([20 + w - 16, 20 + 18, 20 + w - 8, 20 + h - 18], 4, fill=TEEN)
    im.alpha_composite(t, (20 + 48, 20 + 24)); _capimg[txt] = im; return im
def add_caption(fr, T):
    for a, b, txt in CAP_ON_SCREEN:
        if a <= T <= b:
            al = min(1, (T - a) / .18, (b - T) / .18); c = cap_img(txt)
            if al < 1: c = c.copy(); c.putalpha(c.getchannel('A').point(lambda v: int(v * al)))
            fr.alpha_composite(c, ((W - c.width)//2, H - c.height - 34 + int((1 - ease(al)) * 14)))

def enc(path):
    return subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS), path], stdin=subprocess.PIPE)

def frame_at(i, t):
    s = SC[i]; fr = s.render(t)
    if s.trans and t < s.tr and i > 0:
        A = SC[i-1].render(SC[i-1].dur + t); fr = s.trans(A, fr, t / s.tr)
    return fr

def render(only=None, stills=None):
    T0 = 0; starts = []
    for s in SC: starts.append(T0); T0 += s.dur
    if stills:  # list of global times -> preview PNGs
        for T in stills:
            i = max(k for k in range(len(SC)) if starts[k] <= T); fr = frame_at(i, T - starts[i]); add_caption(fr, T)
            fr.convert('RGB').save(OUT + f'still_{T:05.2f}.jpg', quality=88)
        return
    for i, s in enumerate(SC):
        if only is not None and i not in only: continue
        n = round(s.dur * FPS); pc, pv = enc(OUT + f'c{i:02d}.tmp.mp4'), enc(OUT + f'v{i:02d}.tmp.mp4')
        for f in range(n):
            t = f / FPS; fr = frame_at(i, t)
            pc.stdin.write(fr.convert('RGB').tobytes()); add_caption(fr, starts[i] + t); pv.stdin.write(fr.convert('RGB').tobytes())
        for p_, nm in ((pc, 'c'), (pv, 'v')):
            p_.stdin.close(); assert p_.wait() == 0; os.replace(OUT + f'{nm}{i:02d}.tmp.mp4', OUT + f'{nm}{i:02d}.mp4')
        print('scene', i, s.name, 'done', flush=True)

if __name__ == '__main__':
    if sys.argv[1] == 'stills': render(stills=[float(x) for x in sys.argv[2:]])
    else: render(only=[int(x) for x in sys.argv[2:]] or None)
