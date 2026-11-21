# خريطة نقاط الـ API

كل نقطة تقابل دالة في طبقة الـ API داخل المنصة. الجسر (v14 في `src/template.html`) يرسل الطلب تلقائيًا بعد كل إجراء.

| الدالة في المنصة | الطلب | وش يسوي |
| --- | --- | --- |
| (عند الفتح) | `GET /api/bootstrap` | الموظفين ومستوياتهم، والأوزان، والخطط، والسجلات |
| — | `GET /api/health` | فحص الاتصال |
| `login` | `POST /api/auth/login` | تجريبي: يتحقق من الدور |
| `submitReport` | `POST /api/submissions` (type=report) | 7 من 8 فأكثر = «ذيب» تلقائيًا + سعف |
| `submitCert` | `POST /api/submissions` (type=certificate) | يصحّح المواقف الأربعة على الخادم ويعتمد المستوى |
| `renewSkill` | `POST /api/skills/:id/renewals` | يجدد عمر المهارة |
| `toggleLeave` | `PATCH /api/employees/:id/leave` | يجمّد النخلة وعمر المهارات |
| `bookMentor` / `cancelMentor` | `POST /api/mentorship/sessions` · `DELETE /api/mentorship/sessions/mine` | جلسة مع المرشد |
| `registerWorkshop` / `cancelWorkshop` | `POST /api/workshops/:id/registrations` · `DELETE …/registrations/me` | الورش |
| `registerCourse` / `cancelCourse` | `POST /api/courses/:id/registrations` · `DELETE …/registrations/me` | الدورات |
| `setContent` | `PATCH /api/content/:id/progress` | حفظ المحتوى أو إنهاؤه |
| `applyInternal` | `POST /api/internal-jobs/:id/applications` | التقديم على فرصة داخلية |
| `recordInterview` | `PATCH /api/promotions/:id` | نتيجة المقابلة. الرفض بدون سبب (10 أحرف) يُرفض |
| `reviewEscalation` | `PATCH /api/promotions/:id/escalation` | قرار الإدارة العليا: تأييد أو إلغاء الرفض |
| `approveRotation` / `undoRotation` | `POST` / `DELETE /api/rotations/:id/approval` | التدوير الوظيفي |
| `startShadow` | `POST /api/shadowing` | ظل 6 أسابيع لنقل المعرفة |
| `castVote` | `POST /api/promotions/exceptional/:id/votes` | 3 موافقات = اعتماد الترقية الاستثنائية |
| `decidePosition` | `PATCH /api/positions/:id` | تطبيق توصية الوظيفة |
| `requestWeights` | `POST /api/competency-profiles/:job/change-requests` | طلب تعديل الأوزان (مجموعها 100) |
| `resolveWeights` | `PATCH /api/competency-profiles/:job/change-requests/latest` | قرار اللجنة |
| `createPlan` | `POST /api/development-plans` | خطة تطوير، والتكلفة ودعم هدف تنحسب على الخادم |
| `setPlanStatus` | `PATCH /api/development-plans/by-skill/:k` | اعتماد أو رفض الخطة |
| `dismiss` | `PATCH /api/notifications/:key` | إشعار مقروء |
