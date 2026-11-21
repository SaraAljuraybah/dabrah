# قاموس البيانات

كل جداول `database/schema.sql`، مع وش يحفظ كل جدول وأعمدته.

| الجدول | وش يحفظ | الأعمدة |
| --- | --- | --- |
| `app_users` | حسابات الدخول | id (integer)، email (text)، role (text)، employee_id (integer)، created_at (timestamp with time zone) |
| `approvals_log` | سجل الاعتمادات التلقائية | id (integer)، employee_name (text)، item (text)، decision (text)، approved (boolean)، when_text (text)، created_at (timestamp with time zone) |
| `audit_log` | سجل الحوكمة | id (integer)، actor (text)، action (text)، when_text (text)، created_at (timestamp with time zone) |
| `budgets` | الميزانية السنوية | year (integer)، total (numeric) |
| `certificate_questions` | مواقف اختبار الشهادات | skill_code (text)، position (smallint)، question (text)، options (jsonb)، correct_index (smallint) |
| `challenges` | التحديات ومعاييرها | code (text)، skill_code (text)، title (text)، max_score (smallint)، auto_approve_score (smallint)، week_data (jsonb)، criteria (jsonb) |
| `completed_programs` | برامج منفّذة وأثرها | id (integer)، name (text)، cost (numeric)، department_id (integer)، kpi (text)، before_value (text)، after_value (text) |
| `content_items` | محتوى الشركة | code (text)، title (text)، meta (text) |
| `content_progress` | تقدّم الموظف في المحتوى | content_code (text)، employee_id (integer)، status (text)، updated_at (timestamp with time zone) |
| `course_registrations` | التسجيل في الدورات | course_code (text)، employee_id (integer)، created_at (timestamp with time zone) |
| `courses` | الدورات المجدولة | code (text)، title (text)، schedule (text)، seats_note (text) |
| `department_budgets` | ميزانية الأقسام | department_id (integer)، last_year_spend (numeric)، impact (text)، skills_needed (integer) |
| `departments` | الأقسام | id (integer)، name (text) |
| `development_plans` | خطط التطوير | id (integer)، skill_code (text)، net_cost (numeric)، hadaf_support (numeric)، status (text)، created_by (text)، created_at (timestamp with time zone) |
| `employee_skills` | مستوى كل موظف في كل جدارة | employee_id (integer)، skill_code (text)، level (smallint)، last_used_at (timestamp with time zone)، updated_at (timestamp with time zone) |
| `employees` | الموظفون | id (integer)، full_name (text)، gender (character)، nationality (text)، is_saudi (boolean)، department_id (integer)، job_title (text)، email (text)، fronds (integer)، excel_health (text)، score_360 (numeric)، performance (smallint)، potential (smallint)، weekly_hours (integer)، on_leave (boolean)، created_at (timestamp with time zone) |
| `exceptional_promotions` | الترقيات الاستثنائية | id (integer)، employee_id (integer)، from_title (text)، to_title (text)، rationale (text)، votes_needed (smallint)، status (text) |
| `exceptional_votes` | موافقات الترقية الاستثنائية | promotion_id (integer)، approver_role (text)، created_at (timestamp with time zone) |
| `internal_jobs` | الفرص الداخلية | code (text)، title (text)، meta (text)، skills (text) |
| `job_applications` | التقديم على الفرص | job_code (text)، employee_id (integer)، created_at (timestamp with time zone) |
| `job_profile_weights` | أوزان الجدارات (مجموعها 100) | job_code (text)، skill_code (text)، weight (smallint) |
| `job_profiles` | الوظيفة التالية | code (text)، title (text) |
| `kpi_definitions` | تعريف المؤشرات ومصادرها | code (text)، name (text)، formula (text)، source (text)، unit (text)، lower_is_better (boolean) |
| `kpi_values` | قيم المؤشرات | kpi_code (text)، employee_id (integer)، value (numeric)، measured_at (date) |
| `levels` | المستويات الخمسة | level (smallint)، name (text) |
| `mentors` | المرشدون | employee_id (integer)، slot (text) |
| `mentorship_sessions` | جلسات الإرشاد | id (integer)، mentee_id (integer)، mentor_id (integer)، slot (text)، status (text)، created_at (timestamp with time zone) |
| `notification_reads` | الإشعارات المقروءة | key (text)، role (text)، read_at (timestamp with time zone) |
| `palm_stages` | مراحل النخلة | stage (smallint)، name (text)، min_fronds (integer) |
| `plan_members` | الموظفون في كل خطة | plan_id (integer)، employee_id (integer) |
| `positions` | قرارات الوظائف (داخلي/إيقاف/خارجي) | code (text)، title (text)، department_id (integer)، reason (text)، recommendation (text)، note (text)، decision (text)، decided_at (timestamp with time zone) |
| `programs` | برامج التطوير وتكلفتها ودعم هدف | skill_code (text)، name (text)، description (text)، required_level (smallint)، cost_per_employee (numeric)، hadaf_support (numeric) |
| `promotion_files` | ملفات الترقية والمقابلة والتحويل | id (integer)، employee_id (integer)، from_title (text)، to_title (text)، readiness (smallint)، interview (text)، reason (text)، status (text)، escalation_decision (text)، updated_at (timestamp with time zone) |
| `readiness_groups` | مجموعات الجاهزية | name (text)، min_readiness (integer)، color (text) |
| `renewal_questions` | أسئلة تجديد المهارة | skill_code (text)، position (smallint)، question (text)، options (jsonb)، correct_index (smallint) |
| `renewals` | تجديدات المهارة | id (integer)، employee_id (integer)، skill_code (text)، score (smallint)، passed (boolean)، created_at (timestamp with time zone) |
| `rotations` | اقتراحات التدوير الوظيفي | code (text)، to_employee_id (integer)، from_employee_id (integer)، hours (integer)، description (text)، impact (text)، approved (boolean)، approved_at (timestamp with time zone) |
| `shadowing` | الظل لنقل المعرفة الحرجة | id (integer)، skill_code (text)، expert_id (integer)، learner_name (text)، weeks (smallint)، started_at (timestamp with time zone) |
| `skill_types` | أنواع الجدارات الأربعة | code (text)، name (text)، evidence (text) |
| `skills` | الجدارات الـ16 | code (text)، name (text)، type_code (text)، required_level (smallint) |
| `submissions` | التقارير والشهادات المسلّمة | id (integer)، employee_id (integer)، skill_code (text)، type (text)، payload (jsonb)، score (smallint)، level_awarded (smallint)، status (text)، created_at (timestamp with time zone) |
| `talent_boxes` | مصفوفة المواهب 3×3 | code (text)، name (text)، meaning (text)، action (text)، done_message (text) |
| `team_members` | فريق دبره | id (integer)، name (text)، lead (boolean)، roles (jsonb)، linkedin (text) |
| `weight_change_requests` | طلبات تعديل الأوزان | id (integer)، job_code (text)، weights (jsonb)، status (text)، requested_by (text)، decided_by (text)، created_at (timestamp with time zone)، decided_at (timestamp with time zone) |
| `workshop_registrations` | التسجيل في الورش | workshop_code (text)، employee_id (integer)، created_at (timestamp with time zone) |
| `workshops` | الورش الداخلية | code (text)، title (text)، details (text) |
