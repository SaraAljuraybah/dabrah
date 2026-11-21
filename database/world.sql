-- =====================================================================
-- دبره · عالمين في نفس القاعدة:
--   عالم العرض: الحسابات الأربعة التجريبية وبيانات «مستودعات الشرق».
--   العالم الحقيقي: كل حساب جديد، ويشوف الحسابات الحقيقية ونشاطها بس.
-- تعليم الصفوف الموجودة بأنها «عرض» يصير مرة وحدة بس (لما ينضاف العمود).
-- =====================================================================
ALTER TABLE app_users ADD COLUMN IF NOT EXISTS is_demo boolean NOT NULL DEFAULT false;
UPDATE app_users SET is_demo = true
 WHERE email IN ('abdullah.alshammari@sharq.sa','mohammed.alanazi@sharq.sa','haya.alqahtani@sharq.sa','faisal.aldosari@sharq.sa');

DO $$ BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='approvals_log' AND column_name='demo') THEN
    ALTER TABLE approvals_log ADD COLUMN demo boolean NOT NULL DEFAULT false;
    UPDATE approvals_log SET demo = true;          -- الموجود الحين كله من بيانات العرض
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='audit_log' AND column_name='demo') THEN
    ALTER TABLE audit_log ADD COLUMN demo boolean NOT NULL DEFAULT false;
    UPDATE audit_log SET demo = true;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='development_plans' AND column_name='demo') THEN
    ALTER TABLE development_plans ADD COLUMN demo boolean NOT NULL DEFAULT false;
    UPDATE development_plans SET demo = true;
  END IF;
END $$;
