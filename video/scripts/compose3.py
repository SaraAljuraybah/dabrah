# Dabrah walkthrough v3: fixed camera (whole platform on screen, never zooms or pans).
# Only the cursor moves; focus = temporary dark blur around a region; screens change by soft crossfade.
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(__file__))
from compose2 import (text_img, fade_a, soft, keyed, CURSOR, CUR_P, ripple, cap_img, Closing, W, H, FPS, NIGHT, enc)
SH = '/home/claude/proto/vid/s3/'; OUT = '/home/claude/proto/vid/out3/'; os.makedirs(OUT, exist_ok=True)
S = W / 1280                                    # css px -> output px (fixed)

_img, _blur = {}, {}
def img(n):
    if n not in _img:
        _img[n] = Image.open(SH + n + '.jpg').convert('RGB').resize((W, H), Image.LANCZOS).convert('RGBA')
        if len(_img) > 12: _img.pop(next(iter(_img)));
    return _img[n]
def blur(n):
    if n not in _blur:
        b = img(n).filter(ImageFilter.GaussianBlur(9)); dark = Image.new('RGBA', (W, H), (8, 14, 12, 255))
        _blur[n] = Image.blend(b, dark, .55)
        if len(_blur) > 12: _blur.pop(next(iter(_blur)))
    return _blur[n]
_mask = {}
def mask(box):
    k = tuple(box)
    if k not in _mask:
        x, y, w, h = [v * S for v in box]; m = Image.new('L', (W, H), 255)
        ImageDraw.Draw(m).rounded_rectangle([x - 10, y - 10, x + w + 10, y + h + 10], radius=30, fill=0)
        _mask[k] = m.filter(ImageFilter.GaussianBlur(10))
    return _mask[k]

# ---------------- timeline (seconds, css viewport coords) ----------------
STATES = [  # (start, shot, crossfade seconds)
 (0, 'palm2', 0), (1.6, 'palm8', .5), (2.6, 'palm17', .5), (3.6, 'palm26', .5),
 (5.3, 'path0', .45), (7.0, 'case0', .35), (8.5, 'case1', .35), (9.6, 'case2', .35), (10.5, 'caseS', .35), (11.8, 'celeb', .4),
 (13.4, 'path1', .4), (14.8, 'certE', .35), (15.8, 'cert0', .3), (17.0, 'cert1', .35), (18.6, 'cert2', .4),
 (20.0, 'path2', .4), (20.6, 'path306090', .4), (21.8, 'pathComp', .4), (23.0, 'path2', .4),
 (23.8, 'perf0', .35), (24.8, 'perf360', .4), (27.6, 'perf0', .4),
 (28.3, 'learn0', .35), (31.3, 'learnWs', .4), (33.0, 'learn0', .4), (33.7, 'jobs', .35),
 (37.3, 'h0', .5), (38.9, 'hready', .35), (40.5, 'h0', .35), (41.0, 'hexc', .4), (42.6, 'h0', .4),
 (43.3, 'hneeds', .35), (46.0, 'hdev', .4), (46.8, 'hplan0', .35), (48.4, 'hplan1', .3),
 (49.6, 'hgov', .45), (51.4, 'hbias', .4),
 (53.8, 'm0', .5), (55.2, 'mpal', .35), (56.3, 'm0', .3), (56.8, 'mperf', .3), (57.4, 'mknow', .3), (58.0, 'mbudget', .3),
 (58.9, 't0', .45), (59.9, 'tplans', .3), (60.9, 'tchamps', .3), (62.0, 'tover', .3),
]
END = 63.4; CLOSE = Closing(6.6); TOTAL = END + CLOSE.dur      # 70.0 s
FOCUS = [  # (t0, t1, box x,y,w,h)
 (.6, 5.2, (88, 186, 425, 456)), (5.5, 6.9, (867, 387, 320, 213)), (13.6, 14.7, (565, 387, 290, 213)),
 (20.7, 21.7, (88, 68, 1103, 380)), (21.9, 22.9, (88, 68, 1103, 640)), (25.0, 27.5, (88, 319, 1103, 310)),
 (28.5, 30.0, (533, 459, 658, 270)), (30.0, 31.2, (88, 459, 425, 270)), (31.5, 32.9, (88, 82, 1103, 599)),
 (33.9, 36.6, (88, 300, 1103, 410)), (37.6, 38.8, (368, 186, 264, 195)), (41.1, 42.5, (88, 303, 1103, 326)),
 (43.5, 45.9, (88, 82, 1103, 563)), (47.0, 49.2, (584, 261, 672, 99)), (49.8, 51.3, (88, 70, 1103, 620)),
 (51.5, 53.2, (88, 232, 425, 300)), (54.0, 55.1, (88, 342, 1103, 260)),
]
CUR = [  # (t, x, y)
 (5.4, 720, 470), (6.6, 1084, 547), (7.4, 1084, 600), (8.2, 785, 679), (9.5, 785, 679), (10.3, 991, 652), (11.4, 831, 679),
 (12.4, 760, 560), (13.0, 640, 498), (13.6, 700, 470), (14.4, 773, 525), (15.5, 846, 319), (16.6, 813, 679), (17.4, 900, 520),
 (18.2, 784, 679), (19.8, 640, 498), (20.6, 700, 420), (22.6, 760, 380), (23.5, 1066, 139), (24.6, 1000, 260), (27.8, 1000, 200),
 (28.0, 992, 139), (29.2, 900, 600), (32.6, 900, 500), (33.4, 894, 139), (35.0, 252, 430), (36.4, 300, 300),
 (37.0, 228, 38), (37.8, 400, 330), (38.5, 500, 300), (40.2, 800, 614), (41.6, 700, 520), (42.9, 1018, 139),
 (44.6, 900, 420), (46.0, 876, 139), (47.4, 1000, 420), (48.0, 1099, 328), (49.2, 1000, 450), (49.5, 763, 139), (51.6, 700, 420),
 (53.6, 350, 38), (54.4, 900, 470), (54.8, 1091, 480), (56.1, 800, 536), (56.7, 1048, 139), (57.3, 924, 139), (57.9, 790, 139),
 (58.6, 110, 38), (59.8, 984, 139), (60.8, 880, 139), (61.9, 783, 139), (63.0, 700, 300),
]
CLICKS = [6.8, 8.4, 9.5, 10.4, 11.6, 13.2, 14.6, 15.7, 16.8, 18.4, 19.8, 23.6, 28.1, 33.5, 37.1, 38.7, 40.3, 43.1, 48.2,
          53.6, 55.0, 56.1, 56.7, 57.3, 57.9, 58.7, 59.8, 60.8, 61.9]
CAPS = [
 (.5, 2.8, 'عبدالله يفتح «مساري»… ونخلته تكبر مع التزامه،'), (2.9, 5.3, 'تقيس استمراريته: سعفة مع كل إنجاز.'),
 (5.5, 8.3, 'عنده مهارة بس ما عنده شهادة؟ يثبتها بتحدي من شغله.'), (8.4, 11.4, 'يقرأ الموقف، ويستخدم الأداة، ويسلّم الحل…'),
 (11.6, 13.4, 'وتطلع له التهنئة، ويرتفع مستواه.'),
 (13.5, 16.6, 'وإذا عنده شهادة خارجية؟ يضيفها…'), (16.7, 19.9, 'ويختبر عليها بمواقف عملية… وتنضاف لملفه.'),
 (20.1, 23.0, 'ودورته 30-60-90، وجداراته، وطريقه للترقية.'),
 (23.8, 27.6, 'وفي «أدائي»: تقييم 360 يقيس سلوكه بعيون اللي حوله.'),
 (28.3, 31.2, 'ويتعلّم من أهل الدبره: مرشد مباشر، ومحتوى من شركته،'), (31.3, 33.0, 'وورش ودورات… كلها مجانية.'),
 (33.8, 36.6, 'وفرص داخلية تطابق مسماه ومهاراته… بتحليل الذكاء الاصطناعي.'),
 (37.4, 40.4, 'وهيا من تطوير المواهب: تعرف بضغطة مين الجاهز للترقية.'),
 (43.3, 46.0, 'والنظام يقترح القرار: توظيف داخلي، أو إيقاف الوظيفة، أو خارجي.'),
 (46.2, 49.4, 'وتبني خطة تطوير بميزانيتها… والسعوديين أولًا.'),
 (49.7, 51.3, 'وتتحكم بنسبة كل جدارة من الأربع،'), (51.4, 53.3, 'والنظام يرصد أي تحيّز في التقييم.'),
 (53.9, 56.2, 'ومحمد المدير المباشر يشوف حديقة فريقه، وكل نخلة تفتح ملف موظف،'), (56.3, 58.7, 'وبلمحة: العبء، والمعرفة الحرجة، والخطط.'),
 (59.0, 63.3, 'وفيصل من الإدارة العليا يعتمد الترقيات والخطط، ويشوف الأبطال وأداء الشركة.'),
]
SCRIPT_END = (END + 2.8, TOTAL - .4, 'دبره… لا تسأل عن الخبرة، اسأل عن الدبره.')

def state_at(t):
    i = max(k for k in range(len(STATES)) if STATES[k][0] <= t); return i
def frame(T):
    if T >= END: return CLOSE.render(T - END) if T - END >= CLOSE.tr else Image.blend(frame_ui(END - .001 + 0 * T), CLOSE.render(T - END), soft((T - END) / CLOSE.tr))
    return frame_ui(T)
def frame_ui(T):
    i = state_at(T); t0, n, xf = STATES[i]
    base, bl = img(n), None
    a_f = 0; fb = None
    for (f0, f1, box) in FOCUS:
        a = min(1, (T - f0) / .45, (f1 - T) / .45)
        if a > 0: a_f, fb = soft(a), box
    def comp(name):
        if not fb: return img(name)
        m = mask(fb).point(lambda v: int(v * a_f)); return Image.composite(blur(name), img(name), m)
    fr = comp(n)
    if i > 0 and xf and T - t0 < xf: fr = Image.blend(comp(STATES[i - 1][1]), fr, soft((T - t0) / xf))
    if T < .9: fr = Image.blend(Image.new('RGBA', (W, H), (0, 0, 0, 255)), fr, soft(T / .9))
    fr = fr.copy()
    if CUR[0][0] <= T <= CUR[-1][0] + .5:
        x, y = keyed(CUR, T); sx, sy = x * S, y * S
        for c in CLICKS: ripple(fr, sx, sy, (T - c) / .6)
        vis = min(1, (T - CUR[0][0]) / .3, (CUR[-1][0] + .5 - T) / .3)
        press = any(0 <= T - c < .14 for c in CLICKS)
        fr.alpha_composite(fade_a(CUR_P if press else CURSOR, vis), (int(sx - 5), int(sy - 5)))
    return fr
def add_caption(fr, T):
    for a, b, txt in CAPS:
        if a <= T <= b:
            al = min(1, (T - a) / .2, (b - T) / .2); c = fade_a(cap_img(txt), soft(al))
            fr.alpha_composite(c, ((W - c.width) // 2, H - c.height - 26))

SEGS = [0, 13.4, 23.8, 37.3, 49.6, END, TOTAL]
def render(stills=None):
    if stills:
        for T in stills:
            fr = frame(T); add_caption(fr, T); fr.convert('RGB').save(OUT + f'still_{T:05.2f}.jpg', quality=88)
        return
    for k in range(len(SEGS) - 1):
        f0, f1 = round(SEGS[k] * FPS), round(SEGS[k + 1] * FPS)
        pc, pv = enc(OUT + f'c{k:02d}.tmp.mp4'), enc(OUT + f'v{k:02d}.tmp.mp4')
        for f in range(f0, f1):
            T = f / FPS; fr = frame(T); pc.stdin.write(fr.convert('RGB').tobytes()); add_caption(fr, T); pv.stdin.write(fr.convert('RGB').tobytes())
        for p_, nm in ((pc, 'c'), (pv, 'v')):
            p_.stdin.close(); assert p_.wait() == 0; os.replace(OUT + f'{nm}{k:02d}.tmp.mp4', OUT + f'{nm}{k:02d}.mp4')
        print('seg', k, flush=True)
if __name__ == '__main__':
    if sys.argv[1] == 'stills': render([float(x) for x in sys.argv[2:]])
    else: render()
