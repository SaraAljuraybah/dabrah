-- =====================================================================
-- دبره · مخطط قاعدة البيانات (PostgreSQL 14+)
-- يطابق طبقة البيانات (DATA LAYER) وطبقة الربط (API LAYER) في المنصة.
-- شغّله مرة وحدة على قاعدة فاضية، بعدها seed.sql للبيانات التجريبية.
-- =====================================================================
BEGIN;

-- ---------- المراجع الثابتة ----------
CREATE TABLE levels (
  level        smallint PRIMARY KEY CHECK (level BETWEEN 1 AND 5),
  name         text NOT NULL                      -- مبتدئ، شاطر، ذيب، سنع، دبره
);

CREATE TABLE palm_stages (
  stage        smallint PRIMARY KEY,              -- 0 فسيلة … 3 باسقة
  name         text NOT NULL,
  min_fronds   int  NOT NULL
);

CREATE TABLE readiness_groups (
  name          text PRIMARY KEY,                 -- جاهز الآن، قريب، يحتاج تطوير، بداية الطريق
  min_readiness int  NOT NULL,
  color         text NOT NULL
);

CREATE TABLE departments (
  id    serial PRIMARY KEY,
  name  text NOT NULL UNIQUE
);

CREATE TABLE skill_types (
  code      text PRIMARY KEY,                     -- technical | digital | behavioral | leadership
  name      text NOT NULL,                        -- فنية، تقنية، سلوكية، قيادية
  evidence  text NOT NULL                         -- كيف تُثبت
);

CREATE TABLE skills (
  code            text PRIMARY KEY,               -- cap, inv, ai, xl …
  name            text NOT NULL,
  type_code       text NOT NULL REFERENCES skill_types(code),
  required_level  smallint NOT NULL REFERENCES levels(level)
);

-- ملف الجدارات للوظيفة التالية وأوزانها (مجموعها 100)
CREATE TABLE job_profiles (
  code   text PRIMARY KEY,                        -- ops-planner
  title  text NOT NULL
);
CREATE TABLE job_profile_weights (
  job_code    text NOT NULL REFERENCES job_profiles(code) ON DELETE CASCADE,
  skill_code  text NOT NULL REFERENCES skills(code),
  weight      smallint NOT NULL CHECK (weight BETWEEN 0 AND 100),
  PRIMARY KEY (job_code, skill_code)
);

-- ---------- الأشخاص ----------
CREATE TABLE employees (
  id              serial PRIMARY KEY,
  full_name       text NOT NULL,
  gender          char(1) NOT NULL CHECK (gender IN ('m','f')),
  nationality     text NOT NULL,
  is_saudi        boolean NOT NULL,
  department_id   int NOT NULL REFERENCES departments(id),
  job_title       text,
  email           text UNIQUE,
  fronds          int NOT NULL DEFAULT 0 CHECK (fronds >= 0),          -- السعف (الاستمرارية)
  excel_health    text NOT NULL DEFAULT 'green' CHECK (excel_health IN ('green','yellow','red')),
  score_360       numeric(2,1) CHECK (score_360 BETWEEN 1 AND 5),
  performance     smallint CHECK (performance BETWEEN 1 AND 3),
  potential       smallint CHECK (potential BETWEEN 1 AND 3),
  weekly_hours    int CHECK (weekly_hours >= 0),
  on_leave        boolean NOT NULL DEFAULT false,                      -- الإجازة تجمّد النخلة وعمر المهارات
  created_at      timestamptz NOT NULL DEFAULT now()
);

-- مستوى كل موظف في كل جدارة مُثبتة بأدلة (الجدارات المشتقة تُحسب في الواجهة)
CREATE TABLE employee_skills (
  employee_id  int  NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
  skill_code   text NOT NULL REFERENCES skills(code),
  level        smallint NOT NULL REFERENCES levels(level),
  last_used_at timestamptz NOT NULL DEFAULT now(),                     -- عمر المهارة
  updated_at   timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (employee_id, skill_code)
);

-- حسابات الدخول (اربطها بمزوّد هوية حقيقي قبل البيانات الفعلية)
CREATE TABLE app_users (
  id           serial PRIMARY KEY,
  email        text NOT NULL UNIQUE,
  role         text NOT NULL CHECK (role IN ('emp','mgr','haya','top')),
  employee_id  int REFERENCES employees(id),
  created_at   timestamptz NOT NULL DEFAULT now()
);

-- ---------- الإثبات: التحديات والشهادات والتجديد ----------
CREATE TABLE challenges (
  code                text PRIMARY KEY,
  skill_code          text NOT NULL REFERENCES skills(code),
  title               text NOT NULL,
  max_score           smallint NOT NULL,
  auto_approve_score  smallint NOT NULL,                               -- 7 من 8 = اعتماد تلقائي «ذيب»
  week_data           jsonb NOT NULL DEFAULT '[]',
  criteria            jsonb NOT NULL DEFAULT '[]'
);

CREATE TABLE certificate_questions (
  skill_code     text NOT NULL REFERENCES skills(code),
  position       smallint NOT NULL,
  question       text NOT NULL,
  options        jsonb NOT NULL,
  correct_index  smallint NOT NULL,
  PRIMARY KEY (skill_code, position)
);

CREATE TABLE renewal_questions (
  skill_code     text NOT NULL REFERENCES skills(code),
  position       smallint NOT NULL,
  question       text NOT NULL,
  options        jsonb NOT NULL,
  correct_index  smallint NOT NULL,
  PRIMARY KEY (skill_code, position)
);

CREATE TABLE submissions (
  id              serial PRIMARY KEY,
  employee_id     int  NOT NULL REFERENCES employees(id),
  skill_code      text NOT NULL REFERENCES skills(code),
  type            text NOT NULL CHECK (type IN ('report','certificate')),
  payload         jsonb NOT NULL DEFAULT '{}',                         -- نص التقرير، أو بيانات الشهادة والإجابات
  score           smallint,
  level_awarded   smallint REFERENCES levels(level),
  status          text NOT NULL CHECK (status IN ('approved','recorded','theory','returned')),
  created_at      timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX submissions_employee_idx ON submissions(employee_id, created_at DESC);

CREATE TABLE renewals (
  id           serial PRIMARY KEY,
  employee_id  int  NOT NULL REFERENCES employees(id),
  skill_code   text NOT NULL REFERENCES skills(code),
  score        smallint NOT NULL,
  passed       boolean NOT NULL,
  created_at   timestamptz NOT NULL DEFAULT now()
);

-- ---------- التعلّم ----------
CREATE TABLE mentors (
  employee_id  int PRIMARY KEY REFERENCES employees(id),
  slot         text NOT NULL
);
CREATE TABLE mentorship_sessions (
  id          serial PRIMARY KEY,
  mentee_id   int NOT NULL REFERENCES employees(id),
  mentor_id   int NOT NULL REFERENCES employees(id),
  slot        text NOT NULL,
  status      text NOT NULL DEFAULT 'booked' CHECK (status IN ('booked','cancelled','done')),
  created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE workshops (code text PRIMARY KEY, title text NOT NULL, details text NOT NULL);
CREATE TABLE workshop_registrations (
  workshop_code text NOT NULL REFERENCES workshops(code),
  employee_id   int  NOT NULL REFERENCES employees(id),
  created_at    timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (workshop_code, employee_id)
);

CREATE TABLE courses (code text PRIMARY KEY, title text NOT NULL, schedule text NOT NULL, seats_note text);
CREATE TABLE course_registrations (
  course_code  text NOT NULL REFERENCES courses(code),
  employee_id  int  NOT NULL REFERENCES employees(id),
  created_at   timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (course_code, employee_id)
);

CREATE TABLE content_items (code text PRIMARY KEY, title text NOT NULL, meta text);
CREATE TABLE content_progress (
  content_code  text NOT NULL REFERENCES content_items(code),
  employee_id   int  NOT NULL REFERENCES employees(id),
  status        text NOT NULL CHECK (status IN ('saved','done')),
  updated_at    timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (content_code, employee_id)
);

-- ---------- الفرص الداخلية ----------
CREATE TABLE internal_jobs (code text PRIMARY KEY, title text NOT NULL, meta text, skills text);
CREATE TABLE job_applications (
  job_code     text NOT NULL REFERENCES internal_jobs(code),
  employee_id  int  NOT NULL REFERENCES employees(id),
  created_at   timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (job_code, employee_id)
);

-- ---------- الأداء والمؤشرات ----------
CREATE TABLE kpi_definitions (
  code             text PRIMARY KEY,
  name             text NOT NULL,
  formula          text NOT NULL,
  source           text NOT NULL,
  unit             text NOT NULL DEFAULT '',
  lower_is_better  boolean
);
CREATE TABLE kpi_values (
  kpi_code     text NOT NULL REFERENCES kpi_definitions(code),
  employee_id  int  NOT NULL REFERENCES employees(id),
  value        numeric NOT NULL,
  measured_at  date NOT NULL DEFAULT current_date,
  PRIMARY KEY (kpi_code, employee_id, measured_at)
);

-- ---------- المدير المباشر ----------
CREATE TABLE rotations (
  code              text PRIMARY KEY,
  to_employee_id    int NOT NULL REFERENCES employees(id),   -- ينتقل له العبء
  from_employee_id  int NOT NULL REFERENCES employees(id),   -- يخف عنه
  hours             int NOT NULL,
  description       text NOT NULL,
  impact            text,
  approved          boolean NOT NULL DEFAULT false,
  approved_at       timestamptz
);

CREATE TABLE shadowing (
  id          serial PRIMARY KEY,
  skill_code  text NOT NULL,                                  -- مهارة حرجة (wms, cold, cap)
  expert_id   int REFERENCES employees(id),
  learner_name text,
  weeks       smallint NOT NULL DEFAULT 6,
  started_at  timestamptz NOT NULL DEFAULT now()
);

-- ملف الترقية: المقابلة دور المدير الوحيد، والرفض بسبب يتحوّل للإدارة العليا
CREATE TABLE promotion_files (
  id                   serial PRIMARY KEY,
  employee_id          int  NOT NULL REFERENCES employees(id),
  from_title           text NOT NULL,
  to_title             text NOT NULL,
  readiness            smallint,
  interview            text CHECK (interview IN ('pass','fail')),
  reason               text,
  status               text NOT NULL DEFAULT 'open' CHECK (status IN ('open','sent','esc','retry')),
  escalation_decision  text CHECK (escalation_decision IN ('uphold','overturn')),
  updated_at           timestamptz NOT NULL DEFAULT now(),
  CHECK (interview IS DISTINCT FROM 'fail' OR length(coalesce(reason,'')) >= 10)
);

-- ---------- تطوير المواهب ----------
CREATE TABLE exceptional_promotions (
  id            serial PRIMARY KEY,
  employee_id   int  NOT NULL REFERENCES employees(id),
  from_title    text NOT NULL,
  to_title      text NOT NULL,
  rationale     text,
  votes_needed  smallint NOT NULL DEFAULT 3,
  status        text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','ok','rejected'))
);
CREATE TABLE exceptional_votes (
  promotion_id   int  NOT NULL REFERENCES exceptional_promotions(id) ON DELETE CASCADE,
  approver_role  text NOT NULL,
  created_at     timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (promotion_id, approver_role)
);

CREATE TABLE positions (
  code            text PRIMARY KEY,
  title           text NOT NULL,
  department_id   int  NOT NULL REFERENCES departments(id),
  reason          text NOT NULL,
  recommendation  text NOT NULL,                              -- داخلي، داخلي مع ظل، إغلاق، خارجي
  note            text,
  decision        text,                                       -- القرار اللي طبّقته هيا
  decided_at      timestamptz
);

CREATE TABLE talent_boxes (                                  -- مصفوفة المواهب 3×3 (أداء × إمكانات)
  code          text PRIMARY KEY,                             -- '3-3' … '1-1'
  name          text NOT NULL,
  meaning       text NOT NULL,
  action        text NOT NULL,
  done_message  text NOT NULL
);

CREATE TABLE programs (
  skill_code         text PRIMARY KEY REFERENCES skills(code),
  name               text NOT NULL,
  description        text NOT NULL,
  required_level     smallint NOT NULL,
  cost_per_employee  numeric(10,2) NOT NULL DEFAULT 0,
  hadaf_support      numeric(3,2) NOT NULL DEFAULT 0 CHECK (hadaf_support BETWEEN 0 AND 1)  -- نسبة دعم التدريب للسعوديين
);

CREATE TABLE budgets (year int PRIMARY KEY, total numeric(12,2) NOT NULL);
CREATE TABLE department_budgets (
  department_id    int PRIMARY KEY REFERENCES departments(id),
  last_year_spend  numeric(12,2) NOT NULL,
  impact           text NOT NULL,
  skills_needed    int NOT NULL
);
CREATE TABLE completed_programs (
  id             serial PRIMARY KEY,
  name           text NOT NULL,
  cost           numeric(12,2) NOT NULL,
  department_id  int REFERENCES departments(id),
  kpi            text NOT NULL,
  before_value   text NOT NULL,
  after_value    text NOT NULL
);

CREATE TABLE development_plans (
  id             serial PRIMARY KEY,
  skill_code     text NOT NULL REFERENCES programs(skill_code),
  net_cost       numeric(12,2) NOT NULL,
  hadaf_support  numeric(12,2) NOT NULL DEFAULT 0,
  status         text NOT NULL DEFAULT 'wait' CHECK (status IN ('wait','ok','rej')),
  created_by     text,
  created_at     timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE plan_members (
  plan_id      int NOT NULL REFERENCES development_plans(id) ON DELETE CASCADE,
  employee_id  int NOT NULL REFERENCES employees(id),
  PRIMARY KEY (plan_id, employee_id)
);

-- طلبات تعديل أوزان الجدارات (تحتاج اعتماد لجنة)
CREATE TABLE weight_change_requests (
  id            serial PRIMARY KEY,
  job_code      text NOT NULL REFERENCES job_profiles(code),
  weights       jsonb NOT NULL,
  status        text NOT NULL DEFAULT 'pending' CHECK (status IN ('pending','approved','rejected')),
  requested_by  text,
  decided_by    text,
  created_at    timestamptz NOT NULL DEFAULT now(),
  decided_at    timestamptz
);

-- ---------- الإشعارات والسجلات ----------
CREATE TABLE notification_reads (
  key        text NOT NULL,
  role       text NOT NULL,
  read_at    timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (key, role)
);

CREATE TABLE audit_log (                                     -- سجل الحوكمة
  id         serial PRIMARY KEY,
  actor      text NOT NULL,
  action     text NOT NULL,
  when_text  text,
  created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE approvals_log (                                 -- «آخر الاعتمادات التلقائية»
  id             serial PRIMARY KEY,
  employee_name  text NOT NULL,
  item           text NOT NULL,
  decision       text NOT NULL,
  approved       boolean NOT NULL,
  when_text      text,
  created_at     timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE team_members (                                  -- فريق دبره (فوتر المنصة)
  id        serial PRIMARY KEY,
  name      text NOT NULL,
  lead      boolean NOT NULL DEFAULT false,
  roles     jsonb NOT NULL,
  linkedin  text
);

COMMIT;
