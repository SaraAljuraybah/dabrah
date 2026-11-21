-- =====================================================================
-- دبره · مساعد دبره: عدّاد الرسائل اليومي لكل حساب (يحمي حصة Gemini)
-- آمن إذا انشغّل أكثر من مرة.
-- =====================================================================
CREATE TABLE IF NOT EXISTS chat_usage (
  user_id  int  NOT NULL REFERENCES app_users(id) ON DELETE CASCADE,
  day      date NOT NULL DEFAULT current_date,
  n        int  NOT NULL DEFAULT 0,
  PRIMARY KEY (user_id, day)
);
ALTER TABLE chat_usage ENABLE ROW LEVEL SECURITY;
DO $$ BEGIN
  IF EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'anon') THEN
    EXECUTE 'REVOKE ALL ON chat_usage FROM anon, authenticated';
  END IF;
END $$;
