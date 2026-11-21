"""مؤثرات الفيديو (بدون موسيقى): نقرة مع كل ضغطة، وصوت انسحاب ناعم مع فتح/قفل اللوحات وتغيير التبويب والدور،
ولمعة خفيفة مع «كفو!»، وصوت هادي مع الشعار. التوقيتات تُقرأ من video/scripts/compose5.py.
التشغيل (من مجلد video/scripts): python3 ../audio/make_sfx.py
"""
import numpy as np, wave, sys
sys.path.insert(0, '.')
import compose5 as c
SR = 48000; T = 80.0; out = np.zeros((int(SR * T) + SR, 2), np.float32); rng = np.random.default_rng(3)
def db(x): return 10 ** (x / 20)
def norm(x, peak): return x / np.max(np.abs(x)) * db(peak)
def add(t, sig, pan=0.):
    i = int(t * SR); s = np.stack([sig * (1 - pan * .5), sig * (1 + pan * .5)], 1); out[i:i + len(s)] += s[:len(out) - i]
def bandnoise(d, f0, f1, bw=.35):
    n = int(d * SR); x = rng.standard_normal(n); N, H = 1024, 256; y = np.zeros(n + N); win = np.hanning(N); fr = np.fft.rfftfreq(N, 1 / SR)
    for i in range(0, n - N, H):
        p = i / max(1, n - N); fc = f0 * (f1 / f0) ** p; X = np.fft.rfft(x[i:i + N] * win)
        y[i:i + N] += np.fft.irfft(X * np.exp(-.5 * (np.log(fr / fc + 1e-9) / bw) ** 2)) * win
    return y[:n]
def click(v=0):
    n = int(.045 * SR); t = np.arange(n) / SR
    return norm(np.sin(2 * np.pi * (2300 + 120 * v) * t) * np.exp(-t / .0035) + np.convolve(rng.standard_normal(n), [1, -1], 'same') * np.exp(-t / .005) * .25 + np.sin(2 * np.pi * 170 * t) * np.exp(-t / .012) * .45, -21)
def whoosh(d=.45, f0=500, f1=2600, peak=-29):
    x = bandnoise(d, f0, f1); return norm(x * np.sin(np.pi * np.linspace(0, 1, len(x))) ** 2, peak)
def sparkle(d=.7, peak=-31):
    n = int(d * SR); y = np.zeros(n)
    for _ in range(14):
        i = rng.integers(0, n - 2000); m = int(.012 * SR); t = np.arange(m) / SR
        y[i:i + m] += bandnoise(.03, 5000 + rng.random() * 2500, 5000 + rng.random() * 2500, .15)[:m] * np.exp(-t / .004) * rng.uniform(.4, 1)
    return norm(y * np.linspace(1, .3, n), peak)
for k, t in enumerate(c.CLICKS): add(t, click(k % 3), pan=(rng.random() - .5) * .3)
prev = None
for s in c.STEPS:
    v = s['v']; t0 = s['t0']
    if v[0] == 'seq' and v[1] in ('caseOpen', 'certOpen', 'readyOpen', 'palOpen'): add(t0, whoosh(.42, 700, 2400, -30))
    elif v[0] == 'seq' and 'close' in v[1].lower(): add(t0, whoosh(.32, 2200, 700, -33))
    elif v[0] == 'drawerIn': add(t0, whoosh(.45, 700, 2400, -30))
    elif v[0] == 'seq' and v[1].startswith('celeb'): add(t0 + .05, sparkle())
    elif v[0] == 'page' and prev is not None and prev[0] == 'page' and prev[1] != v[1] and s.get('tr'):
        rc = prev[1][0] != v[1][0]; add(t0, whoosh(.5 if rc else .34, 450, 2000 if rc else 1600, -29 if rc else -33))
    prev = v
add(c.END, whoosh(.9, 300, 1500, -28)); add(c.END + .9, whoosh(1.7, 1500, 5000, -34))
w = wave.open('sfx.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(out[:int(SR * T)], -1, 1) * 32767).astype(np.int16).tobytes()); w.close(); print('sfx.wav')
