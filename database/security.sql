-- =====================================================================
-- دبره · قفل الجداول على Supabase
-- الواجهة ما تكلّم القاعدة مباشرة؛ كل شي يمر عبر دالة /api على الخادم
-- (تتصل بمستخدم postgres صاحب الجداول، فما يتأثر بالقفل).
-- هنا نشغّل RLS على كل جداول public بدون سياسات، ونسحب صلاحيات anon و authenticated،
-- عشان ما أحد يقدر يقرأ أو يعدّل البيانات من مفتاح Supabase العام.
-- آمن إذا انشغّل أكثر من مرة.
-- =====================================================================
DO $$
DECLARE t record;
BEGIN
  FOR t IN SELECT tablename FROM pg_tables WHERE schemaname = 'public' LOOP
    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', t.tablename);
  END LOOP;
  IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'anon') THEN
    EXECUTE 'REVOKE ALL ON ALL TABLES IN SCHEMA public FROM anon, authenticated';
    EXECUTE 'REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM anon, authenticated';
    EXECUTE 'ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON TABLES FROM anon, authenticated';
    EXECUTE 'ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON SEQUENCES FROM anon, authenticated';
  END IF;
END $$;
