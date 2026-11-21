-- =====================================================================
-- دبره · الحسابات الحقيقية (يتشغّل بعد schema.sql و seed.sql)
-- كلمات المرور مجزّأة بـ scrypt، والجلسات نخزّن بصمتها بس (sha256).
-- آمن إذا انشغّل أكثر من مرة.
-- =====================================================================
ALTER TABLE app_users ADD COLUMN IF NOT EXISTS full_name     text;
ALTER TABLE app_users ADD COLUMN IF NOT EXISTS staff_no      text;
ALTER TABLE app_users ADD COLUMN IF NOT EXISTS password_hash text;
ALTER TABLE app_users ADD COLUMN IF NOT EXISTS profile       jsonb NOT NULL DEFAULT '{}';
CREATE UNIQUE INDEX IF NOT EXISTS app_users_staff_no_key ON app_users(staff_no);

-- الموظفين اللي سجّلوا بأنفسهم ما يظهرون في قوائم الفريق لين ينضافون رسميًا (ما عندهم تقييم 360 ولا أداء)
ALTER TABLE employees ADD COLUMN IF NOT EXISTS is_listed boolean NOT NULL DEFAULT true;

CREATE TABLE IF NOT EXISTS sessions (
  token_hash  text PRIMARY KEY,
  user_id     int  NOT NULL REFERENCES app_users(id) ON DELETE CASCADE,
  created_at  timestamptz NOT NULL DEFAULT now(),
  expires_at  timestamptz NOT NULL
);
CREATE INDEX IF NOT EXISTS sessions_user_idx ON sessions(user_id);

-- حسابات العرض الأربعة (كلمة المرور لكلها: Dabrah2026). عبدالله مربوط بالموظف رقم 1 وبياناته كاملة،
-- وبداية حسابه قبل 44 يوم عشان دورة 30-60-90 تكون في يومها 45 مثل العرض.
INSERT INTO app_users (email, role, employee_id, full_name, staff_no, password_hash, profile, created_at) VALUES
  ('abdullah.alshammari@sharq.sa', 'emp',  1,    'عبدالله الشمري', '10482', 'scrypt$16384$8$1$qRfxmMZLIVmESJMm+WwmIA==$2l/rucNA8+bJUPWhUeGR3/8j0iWYC4CHRtDfUrZuKYQW3SXtKI2XFeEjFsishVU49fN5F0Q0C+94hknPhtnXeQ==', '{"title":"مشرف مستودع","dept":"0","gender":"m","nat":"sa"}', now() - interval '44 days'),
  ('mohammed.alanazi@sharq.sa',    'mgr',  NULL, 'محمد العنزي',    '20117', 'scrypt$16384$8$1$jfSxN+NKwHK6+qwKQmjTjw==$UK/GwlkN9VbHW1txpqoSPLHdAmj4pLJFdqmygHhSnMt3YBWMJ1Ph74dJZzsjFDoVSb4a3/ndgOTbPgz6aY2Q/Q==', '{"dept":"0","team":"7"}', now() - interval '44 days'),
  ('haya.alqahtani@sharq.sa',      'haya', NULL, 'هيا القحطاني',   '30561', 'scrypt$16384$8$1$rCe7Iv8AGes5CFfTHg+/vg==$/OAfdGWlof8pr1R0E7mzEveiOcL7E/kXqGQ+QWg+X96z7QXkIc75VpxJLe4x9ytgOr/sSSNHeefP8iX6INhQ8g==', '{"org":"مستودعات الشرق","count":"52"}', now() - interval '44 days'),
  ('faisal.aldosari@sharq.sa',     'top',  NULL, 'فيصل الدوسري',   '40023', 'scrypt$16384$8$1$77ZwgfaOu9tfRQhjkFCBZg==$NaND1TO74kSrJEB/UMVBhVo5IP+kIYMTio1mwlI+0eBdCeWuhFyW4bM9m4x+u5ATlolvndMUwB3Wm87FDkq40w==', '{"title":"مدير العمليات"}', now() - interval '44 days')
ON CONFLICT (email) DO NOTHING;

-- قفل الجدول الجديد مثل باقي الجداول
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
DO $$ BEGIN
  IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'anon') THEN
    EXECUTE 'REVOKE ALL ON sessions FROM anon, authenticated';
  END IF;
END $$;
