"""يبني site/index.html من src/template.html (يحقن الشعار، ويضيف env.js لربط قاعدة البيانات).
التشغيل: python3 scripts/build-site.py
"""
import os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(R, 'src', 'template.html'), encoding='utf8').read()
s = s.replace('__LOGO3__', open(os.path.join(R, 'src', 'logo3.b64')).read().strip())
assert s.count('<script>') == 1
s = s.replace('<script>', '<script src="/env.js"></script>\n<script>', 1)   # يعرّف window.__ENV قبل كود المنصة
assert '�' not in s
os.makedirs(os.path.join(R, 'site'), exist_ok=True)
open(os.path.join(R, 'site', 'index.html'), 'w', encoding='utf8').write(s)
print('site/index.html built', len(s))
