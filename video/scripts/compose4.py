# Dabrah walkthrough v4 — feels like using the live site: fixed frame, the page itself scrolls under the sticky
# header, tabs switch in place, drawers/modals/celebrations use the site's own motion (captured frame by frame).
# Focus = light blur + soft tint around a region. 80 s.
import json, math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compose2 import fade_a, soft, keyed, CURSOR, CUR_P, ripple, cap_img, Closing, W, H, FPS, enc
SH = '/home/claude/proto/vid/s4/'; OUT = '/home/claude/proto/vid/out4/'; os.makedirs(OUT, exist_ok=True)
K = 3; S = W / 1280; META = json.load(open(SH + 'meta.json')); BAR = META['bar']['h']   # 76 css

_c = {}
def load(path, box=None, size=(W, H)):
    key = (path, box, size)
    if key in _c: return _c[key]
    im = Image.open(SH + path)
    im = im.resize(size, Image.BICUBIC, box=box, reducing_gap=2.0) if box else im.resize(size, Image.LANCZOS)
    im = im.convert('RGBA'); _c[key] = im
    if len(_c) > 40: _c.pop(next(iter(_c)))
    return im
_pg = {}
def pg(name):
    if name not in _pg:
        _pg[name] = Image.open(SH + f'pg_{name}.jpg').convert('RGB')
        if len(_pg) > 4: _pg.pop(next(iter(_pg)))
    return _pg[name]
_hdr = {}
def hdr(name):
    if name not in _hdr: _hdr[name] = Image.open(SH + f'hdr_{name}.jpg').crop((0, 0, 1280*K, BAR*K)).resize((W, round(BAR*S)), Image.LANCZOS).convert('RGBA')
    return _hdr[name]
def page(name, y):
    im = pg(name); hmax = META['pages'][name]['h'] - 720; y = max(0, min(y, hmax))
    fr = im.resize((W, H), Image.BICUBIC, box=(0, y*K, 1280*K, (y + 720)*K), reducing_gap=2.0).convert('RGBA')
    fr.alpha_composite(hdr(name), (0, 0)); return fr, y
def shot(n): return load(f'v_{n}.jpg')
def seqf(n, i):
    i = max(0, min(i, META['seqs'][n] - 1)); return load(f'q_{n}_{i:03d}.jpg')

def rr_mask(box, r, feather=0, inside=255):
    x, y, w, h = [v * S for v in box]; m = Image.new('L', (W, H), 255 - inside)
    ImageDraw.Draw(m).rounded_rectangle([x, y, x + w, y + h], radius=r * S, fill=inside)
    return m.filter(ImageFilter.GaussianBlur(feather)) if feather else m
_fm = {}
def focus_mask(box):
    k = tuple(round(v) for v in box)
    if k not in _fm:
        x, y, w, h = k; _fm[k] = rr_mask((x - 8, y - 8, w + 16, h + 16), 26, feather=9, inside=0)
        if len(_fm) > 60: _fm.pop(next(iter(_fm)))
    return _fm[k]
def soften(fr):   # the focus "fog": light blur + gentle tint, not black
    b = fr.filter(ImageFilter.GaussianBlur(3.2)); return Image.blend(b, Image.new('RGBA', (W, H), (16, 24, 21, 255)), .2)

# ---------------- storyboard: steps with durations; times inside a step are relative ----------------
DR = (720, 0, 560, 720)          # challenge / certificate drawer
STEPS = [
 dict(d=3.6, v=('page', 'E_path', [(0, 0)]), fadein=.9, focus=[(.6, 3.4, 'p', (533, 186, 658, 456))],
      cur=[(2.6, 760, 620), (3.35, 1084, 547)], clicks=[3.5], caps=[(.4, 3.5, 'حياك عبدالله… هذي صفحته في دبره.')]),
 dict(d=.55, v=('seq', 'caseOpen'), caps=[(0, 2.35, 'عنده مهارة يبي يثبتها، بس ما عنده شهادة؟ يبدأ تحدي من شغله.')]),
 dict(d=1.9, v=('shot', 'case0'), tr=('dis', .12), cur=[(.9, 1000, 560), (1.6, 785, 679)], clicks=[1.8]),
 dict(d=1.5, v=('shot', 'case1'), tr=('reg', .3, DR), cur=[(1.2, 785, 679)], clicks=[1.4],
      caps=[(.05, 3.85, 'يقرأ الموقف، ويستخدم الأداة المعتمدة، ويسلّم حلّه…')]),
 dict(d=1.0, v=('shot', 'case2'), tr=('reg', .3, DR), cur=[(.6, 991, 652)], clicks=[.8]),
 dict(d=1.4, v=('shot', 'caseS'), tr=('reg', .3, DR), cur=[(1.0, 831, 679)], clicks=[1.3]),
 dict(d=2.7, v=('seq', 'celebA'), cur=[(1.6, 700, 560), (2.25, 640, 498)], clicks=[2.6],
      caps=[(.1, 2.75, 'والنظام يعتمده تلقائيًا… كفو!')]),
 dict(d=.35, v=('seq', 'celebAclose')),
 dict(d=2.0, v=('page', 'E_path1', [(0, 0)]), tr=('dis', .15), focus=[(.2, 1.8, 'p', (561, 382, 295, 183))],
      cur=[(1.1, 740, 470), (1.6, 773, 525)], clicks=[1.9], caps=[(.1, 3.0, 'ولو عنده شهادة خارجية؟ يقدر يرفقها هنا…')]),
 dict(d=.55, v=('seq', 'certOpen')),
 dict(d=1.0, v=('shot', 'certE'), tr=('dis', .12), cur=[(.6, 846, 319)], clicks=[.85]),
 dict(d=1.1, v=('shot', 'cert0'), tr=('reg', .3, DR), cur=[(.8, 813, 679)], clicks=[1.0]),
 dict(d=2.0, v=('shot', 'cert1'), tr=('reg', .3, DR), cur=[(1.0, 900, 520), (1.6, 784, 679)], clicks=[1.9],
      caps=[(0, 1.95, 'ويختبر عليها بمواقف من شغله… عشان نتأكد إنه يطبّقها.')]),
 dict(d=2.3, v=('seq', 'celebB'), cur=[(1.4, 700, 560), (1.9, 640, 498)], clicks=[2.2], caps=[(.1, 2.5, 'نجح… وانضافت لملفه.')]),
 dict(d=.35, v=('seq', 'celebBclose')),
 dict(d=2.6, v=('page', 'E_path2', [(0, 0)]), tr=('dis', .15), focus=[(.1, 2.5, 'p', (88, 186, 425, 417))],
      palm=[(.2, 'palm2'), (.8, 'palm8'), (1.4, 'palm17'), (2.0, None)], cur=[(1.0, 520, 560)],
      caps=[(.1, 2.6, 'ونخلته تكبر مع التزامه… وتقيس استمراريته.')]),
 dict(d=4.0, v=('page', 'E_path2', [(0, 0), (1.4, 927)]), focus=[(1.5, 3.9, 'p', (88, 1023, 1103, 640))],
      cur=[(1.6, 640, 560)], caps=[(.1, 4.0, 'وجداراته وطريقه للترقية: كل جدارة بيت، ومستواه بعدد مثلثاته.')]),
 dict(d=.8, v=('page', 'E_path2', [(0, 927), (.8, 0)]), cur=[(.7, 1066, 139)], clicks=[.78]),
 dict(d=4.6, v=('page', 'E_perf', [(.4, 0), (1.6, 737)]), tr=('dis', .15), focus=[(1.7, 4.4, 'p', (88, 1056, 1103, 310))],
      cur=[(1.0, 900, 300), (2.2, 760, 470)], caps=[(.1, 4.5, 'وفي «أدائي»: تقييم 360 يقيس سلوكه بعيون اللي حوله.')]),
 dict(d=.8, v=('page', 'E_perf', [(0, 737), (.8, 0)]), cur=[(.7, 992, 139)], clicks=[.78]),
 dict(d=4.4, v=('page', 'E_learn', [(1.5, 0), (2.5, 882)]), tr=('dis', .15),
      focus=[(.2, 1.5, 'p', (533, 459, 658, 261)), (2.6, 4.3, 'p', (88, 982, 1103, 599))],
      cur=[(.6, 1100, 610), (2.0, 900, 400), (3.4, 180, 260)],
      caps=[(.1, 2.4, 'ويتعلّم من أهل الدبره: مرشد مباشر، ومحتوى من شركته،'), (2.5, 4.4, 'وورش ودورات مجانية… يسجّل فيها بضغطة.')]),
 dict(d=.8, v=('page', 'E_learn', [(0, 882), (.8, 0)]), cur=[(.7, 894, 139)], clicks=[.78]),
 dict(d=2.8, v=('page', 'E_jobs', [(0, 0)]), tr=('dis', .15), focus=[(.2, 2.6, 'p', (88, 300, 1103, 410))],
      cur=[(.8, 252, 430), (2.5, 228, 38)], clicks=[2.78],
      caps=[(.1, 2.8, 'وفرص داخلية تطابق مسماه ومهاراته… بتحليل الذكاء الاصطناعي.')]),
 # ---- Haya ----
 dict(d=1.6, v=('page', 'H_talent', [(0, 0)]), tr=('dis', .3), focus=[(.2, 1.4, 'p', (368, 186, 264, 195))],
      cur=[(1.2, 500, 330)], clicks=[1.55], caps=[(.1, 3.6, 'وهيا من تطوير المواهب: تعرف بضغطة مين الجاهز للترقية.')]),
 dict(d=.47, v=('seq', 'readyOpen')),
 dict(d=1.6, v=('shot', 'hready'), tr=('dis', .1), cur=[(1.2, 800, 614)], clicks=[1.55]),
 dict(d=.35, v=('seq', 'readyClose')),
 dict(d=.5, v=('page', 'H_talent', [(0, 0)]), tr=('dis', .1), cur=[(.4, 1018, 139)], clicks=[.48]),
 dict(d=7.4, v=('page', 'H_needs', [(.2, 0), (1.2, 438)]), tr=('dis', .15),
      focus=[(1.3, 2.8, 'p', (116, 583, 1047, 120)), (2.8, 4.3, 'p', (116, 703, 1047, 120)), (4.3, 5.8, 'p', (116, 823, 1047, 120)), (5.8, 7.3, 'p', (116, 943, 1047, 120))],
      cur=[(1.2, 600, 300), (1.9, 278, 205), (3.4, 278, 325), (4.9, 278, 445), (6.4, 278, 565)],
      caps=[(.2, 3.6, 'النظام يقرأ العبء والمهارات، ويقترح لكل وظيفة قرارها:'), (3.7, 7.4, 'توظيف داخلي، أو إيقاف الوظيفة، أو توظيف خارجي.')]),
 dict(d=.8, v=('page', 'H_needs', [(0, 438), (.8, 0)]), cur=[(.7, 876, 139)], clicks=[.78]),
 dict(d=1.4, v=('page', 'H_dev', [(.2, 0), (1.0, 440)]), tr=('dis', .15), cur=[(1.1, 180, 442)], clicks=[1.35],
      caps=[(.1, 4.6, 'وتبني خطة تطوير بميزانيتها… والسعوديين أولًا.')]),
 dict(d=.5, v=('drawerIn', 'H_dev', 440, 'hplan0', (560, 0, 720, 720))),
 dict(d=1.6, v=('shot', 'hplan0'), focus=[(.1, 1.5, 'v', (584, 261, 672, 99))], cur=[(.9, 1099, 328)], clicks=[1.2]),
 dict(d=1.0, v=('shot', 'hplan1'), tr=('reg', .3, (560, 0, 720, 720)), cur=[(.6, 674, 679)], clicks=[.9]),
 dict(d=3.9, v=('page', 'H_gov', [(1.5, 0), (2.4, 632)]), tr=('dis', .35),
      focus=[(.3, 1.5, 'p', (88, 186, 1103, 520)), (2.5, 3.8, 'p', (88, 892, 425, 300))],
      cur=[(.8, 700, 420), (2.6, 520, 420), (3.6, 350, 38)], clicks=[3.88],
      caps=[(.2, 1.5, 'وتتحكم بنسبة كل جدارة،'), (1.6, 3.9, 'والنظام يرصد أي تحيّز في التقييم.')]),
 # ---- Mohammed (manager) ----
 dict(d=1.5, v=('page', 'M_team', [(0, 0)]), tr=('dis', .3), focus=[(.2, 1.2, 'p', (88, 342, 1103, 260))],
      cur=[(1.1, 1091, 480)], clicks=[1.45], caps=[(.1, 2.9, 'ومحمد المدير المباشر يشوف حديقة فريقه، وكل نخلة تفتح ملف موظف،')]),
 dict(d=.73, v=('seq', 'palOpen')),
 dict(d=.8, v=('shot', 'mpal'), tr=('dis', .1), cur=[(.5, 640, 441)], clicks=[.75]),
 dict(d=2.9, v=('tall', [(.4, 0), (2.6, 1286)]), tr=('dis', .3), cur=[(1.0, 900, 400), (2.6, 797, 633)], clicks=[2.85],
      caps=[(0, 3.0, 'بكل جداراته… وكل بيت يوضّح مستواه.')]),
 # ---- Faisal (top management) ----
 dict(d=.5, v=('page', 'M_team', [(0, 0)]), tr=('dis', .2), cur=[(.4, 110, 38)], clicks=[.48]),
 dict(d=1.0, v=('page', 'T_files', [(0, 0)]), tr=('dis', .2), cur=[(.8, 880, 139)], clicks=[.98],
      caps=[(.1, 3.1, 'وفيصل يعتمد الترقيات والخطط، ويشوف أبطال الشركة وأداءها.')]),
 dict(d=1.0, v=('page', 'T_champs', [(0, 0)]), tr=('dis', .15), cur=[(.8, 783, 139)], clicks=[.98]),
 dict(d=1.1, v=('page', 'T_over', [(0, 0)]), tr=('dis', .15), cur=[(.9, 700, 300)]),
]
CLOSE = Closing(0)
t = 0
for s in STEPS: s['t0'] = t; t += s['d']
END = t; CLOSE.dur = 80.0 - END; TOTAL = 80.0
CUR, CLICKS, CAPS, FOCUS = [], [], [], []
for s in STEPS:
    for (a, x, y) in s.get('cur', []): CUR.append((s['t0'] + a, x, y))
    CLICKS += [s['t0'] + c for c in s.get('clicks', [])]
    CAPS += [(s['t0'] + a, s['t0'] + b, txt) for a, b, txt in s.get('caps', [])]
    for (a, b, sp, box) in s.get('focus', []): FOCUS.append((s['t0'] + a, s['t0'] + b, sp, box, s))
CUR.sort()
SCRIPT_END = (END + 2.8, TOTAL - .4, 'دبره… لا تسأل عن الخبرة، اسأل عن الدبره.')

MX = META['mboxX']; TALL_H = META['mboxTallH']
_tall = None
def tall_view(y):
    global _tall
    if _tall is None: _tall = Image.open(SH + 'mbox_tall.jpg').convert('RGB')
    base = shot('mpalX').copy(); x0, y0, w, h = MX; y = max(0, min(y, _tall.height / K - h - .01))
    crop = _tall.resize((round(w*S), round(h*S)), Image.BICUBIC, box=(0, y*K, w*K, (y + h)*K), reducing_gap=2.0).convert('RGBA')
    m = Image.new('L', crop.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, crop.width - 1, crop.height - 1], radius=26*S, fill=255)
    base.paste(crop, (round(x0*S), round(y0*S)), m); return base

def render_view(s, T):
    lt = T - s['t0']; v = s['v']; scroll = 0
    if v[0] == 'page':
        y = keyed(v[2], lt)[0]; fr, scroll = page(v[1], y)
    elif v[0] == 'shot': fr = shot(v[1])
    elif v[0] == 'seq': fr = seqf(v[1], int(lt * 30))
    elif v[0] == 'tall': fr = tall_view(keyed(v[1], lt)[0])
    elif v[0] == 'drawerIn':
        _, pname, py, target, box = v; p = soft(lt / s['d'])
        base, _ = page(pname, py); scrim = Image.blend(base, soften(base).filter(ImageFilter.GaussianBlur(4)), p)
        scrim = Image.blend(scrim, Image.new('RGBA', (W, H), (14, 26, 23, 255)), .35 * p)
        x, y, w, h = [round(c * S) for c in box]; dr = shot(target).crop((x, y, x + w, y + h))
        scrim.alpha_composite(dr, (round(x + (W - x) * (1 - p)), y)); fr = scrim
    if 'palm' in s:
        box = (88, 186, 425, 417); x, y, w, h = [round(c * S) for c in box]; fr = fr.copy()
        seq = s['palm']; cur = None; prev = None; ts = 0
        for (a, n) in seq:
            if lt >= a: prev, cur, ts = cur, n, a
        def crop(n): return (shot(n) if n else fr).crop((x, y, x + w, y + h))
        if cur is not None or prev is not None:
            A = crop(prev) if lt - ts < .3 else None; B = crop(cur)
            img = Image.blend(A, B, soft((lt - ts) / .3)) if A is not None else B
            fr.paste(img, (x, y))
    return fr, scroll

def frame(T):
    if T >= END:
        c = CLOSE.render(T - END)
        if T - END < .9: c = Image.blend(frame(END - 1e-3), c, soft((T - END) / .9))
        return c
    i = max(k for k in range(len(STEPS)) if STEPS[k]['t0'] <= T); s = STEPS[i]; lt = T - s['t0']
    fr, scroll = render_view(s, T)
    # focus fog (box in page coords follows the scroll)
    for (a, b, sp, box, fs) in FOCUS:
        al = min(1, (T - a) / .5, (b - T) / .5)
        if al > 0:
            bx = box if sp == 'v' else (box[0], box[1] - (scroll if fs is s else 0), box[2], box[3])
            m = focus_mask(bx).point(lambda v, al=soft(al): int(v * al)); fr = Image.composite(soften(fr), fr, m); break
    tr = s.get('tr')
    if tr and lt < tr[1] and i > 0:
        pf, _ = render_view(STEPS[i - 1], T); p = soft(lt / tr[1])
        if tr[0] == 'reg':
            m = rr_mask(tr[2], 0, inside=int(255 * (1 - p))); fr = Image.composite(pf, fr, m)
        else: fr = Image.blend(pf, fr, p)
    if s.get('fadein') and lt < s['fadein']: fr = Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 255)), fr, soft(lt / s['fadein']))
    fr = fr.copy()
    if CUR and CUR[0][0] <= T:
        x, y = keyed(CUR, T); sx, sy = x * S, y * S
        for c in CLICKS: ripple(fr, sx, sy, (T - c) / .6)
        press = any(0 <= T - c < .14 for c in CLICKS)
        fr.alpha_composite(fade_a(CUR_P if press else CURSOR, min(1, (T - CUR[0][0]) / .3)), (int(sx - 5), int(sy - 5)))
    return fr
def add_caption(fr, T):
    for a, b, txt in CAPS:
        if a <= T <= b:
            al = min(1, (T - a) / .25, (b - T) / .25); c = fade_a(cap_img(txt), soft(al))
            fr.alpha_composite(c, ((W - c.width) // 2, H - c.height - 26))

ONLY = []
def render(stills=None):
    if stills:
        for T in stills:
            fr = frame(T); add_caption(fr, T); fr.convert('RGB').save(OUT + f'still_{T:05.2f}.jpg', quality=88)
        return
    segs = [0, 15.0, 30.0, 43.1, 58.0, END, TOTAL]
    for k in range(len(segs) - 1):
        if ONLY and k not in ONLY: continue
        f0, f1 = round(segs[k] * FPS), round(segs[k + 1] * FPS)
        pc, pv = enc(OUT + f'c{k:02d}.tmp.mp4'), enc(OUT + f'v{k:02d}.tmp.mp4')
        for f in range(f0, f1):
            T = f / FPS; fr = frame(T); pc.stdin.write(fr.convert('RGB').tobytes()); add_caption(fr, T); pv.stdin.write(fr.convert('RGB').tobytes())
        for p_, nm in ((pc, 'c'), (pv, 'v')):
            p_.stdin.close(); assert p_.wait() == 0; os.replace(OUT + f'{nm}{k:02d}.tmp.mp4', OUT + f'{nm}{k:02d}.mp4')
        print('seg', k, flush=True)
if __name__ == '__main__':
    if sys.argv[1] == 'times':
        print('END', END); [print(f"{s['t0']:6.2f} {s['v'][0]} {s['v'][1] if len(s['v'])>1 else ''}") for s in STEPS]
    elif sys.argv[1] == 'stills': render([float(x) for x in sys.argv[2:]])
    else:
        ONLY = [int(x) for x in sys.argv[2:]]; render()
