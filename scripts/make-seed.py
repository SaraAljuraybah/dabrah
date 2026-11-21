"""يحوّل database/seed.json إلى database/seed.sql (INSERT جاهزة لـ PostgreSQL).
التشغيل: python3 scripts/make-seed.py
"""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(os.path.join(ROOT, 'database', 'seed.json'), encoding='utf8'))

def q(v):
    if v is None: return 'NULL'
    if isinstance(v, bool): return 'true' if v else 'false'
    if isinstance(v, (int, float)): return repr(v)
    if isinstance(v, (list, dict)): return "'" + json.dumps(v, ensure_ascii=False).replace("'", "''") + "'::jsonb"
    return "'" + str(v).replace("'", "''") + "'"

out = ['-- دبره · البيانات التجريبية (مولّدة من seed.json عبر scripts/make-seed.py)', 'BEGIN;']
def ins(table, cols, rows):
    if not rows: return
    out.append(f'INSERT INTO {table} ({", ".join(cols)}) VALUES')
    out.append(',\n'.join('  (' + ', '.join(q(r[c] if isinstance(r, dict) else r[i]) for i, c in enumerate(cols)) + ')' for r in rows) + ';')

ins('levels', ['level', 'name'], d['levels'])
ins('palm_stages', ['stage', 'name', 'min_fronds'], d['palm_stages'])
ins('readiness_groups', ['name', 'min_readiness', 'color'], d['readiness_groups'])
ins('departments', ['id', 'name'], d['departments'])
ins('skill_types', ['code', 'name', 'evidence'], d['skill_types'])
ins('skills', ['code', 'name', 'type_code', 'required_level'], [{**s, 'type_code': s['type']} for s in d['skills']])
ins('job_profiles', ['code', 'title'], d['job_profiles'])
ins('job_profile_weights', ['job_code', 'skill_code', 'weight'],
    [{'job_code': j['code'], 'skill_code': k, 'weight': w} for j in d['job_profiles'] for k, w in j['weights'].items()])
ins('employees', ['id', 'full_name', 'gender', 'nationality', 'is_saudi', 'department_id', 'fronds', 'excel_health', 'score_360', 'performance', 'potential', 'weekly_hours'], d['employees'])
ins('employee_skills', ['employee_id', 'skill_code', 'level'],
    [{'employee_id': e['id'], 'skill_code': k, 'level': v} for e in d['employees'] for k, v in e['levels'].items()])
ins('challenges', ['code', 'skill_code', 'title', 'max_score', 'auto_approve_score', 'week_data', 'criteria'], d['challenges'])
ins('certificate_questions', ['skill_code', 'position', 'question', 'options', 'correct_index'], d['certificate_questions'])
ins('renewal_questions', ['skill_code', 'position', 'question', 'options', 'correct_index'], d['renewal_questions'])
ins('mentors', ['employee_id', 'slot'], d['mentors'])
ins('workshops', ['code', 'title', 'details'], d['workshops'])
ins('courses', ['code', 'title', 'schedule', 'seats_note'], d['courses'])
ins('content_items', ['code', 'title', 'meta'], d['content_items'])
ins('internal_jobs', ['code', 'title', 'meta', 'skills'], d['internal_jobs'])
ins('kpi_definitions', ['code', 'name', 'formula', 'source', 'unit', 'lower_is_better'], d['kpi_definitions'])
ins('kpi_values', ['kpi_code', 'employee_id', 'value'], d['kpi_values'])
ins('rotations', ['code', 'to_employee_id', 'from_employee_id', 'hours', 'description', 'impact'], d['rotations'])
ins('promotion_files', ['id', 'employee_id', 'from_title', 'to_title', 'readiness', 'status'], d['promotion_files'])
ins('exceptional_promotions', ['id', 'employee_id', 'from_title', 'to_title', 'rationale', 'votes_needed', 'status'], d['exceptional_promotions'])
ins('positions', ['code', 'title', 'department_id', 'reason', 'recommendation', 'note'], d['positions'])
ins('talent_boxes', ['code', 'name', 'meaning', 'action', 'done_message'], d['talent_boxes'])
ins('programs', ['skill_code', 'name', 'description', 'required_level', 'cost_per_employee', 'hadaf_support'], d['programs'])
ins('budgets', ['year', 'total'], [d['budget']])
ins('department_budgets', ['department_id', 'last_year_spend', 'impact', 'skills_needed'], d['department_budgets'])
ins('completed_programs', ['name', 'cost', 'department_id', 'kpi', 'before_value', 'after_value'],
    [{**c, 'before_value': c['before'], 'after_value': c['after']} for c in d['completed_programs']])
ins('audit_log', ['actor', 'action', 'when_text'], d['audit_log'])
ins('approvals_log', ['employee_name', 'item', 'decision', 'approved', 'when_text'], d['approvals_log'])
ins('team_members', ['name', 'lead', 'roles', 'linkedin'], d['team'])
# تصحيح عدّادات serial بعد إدخال معرّفات صريحة
for t in ['departments', 'employees', 'promotion_files', 'exceptional_promotions']:
    out.append(f"SELECT setval(pg_get_serial_sequence('{t}','id'), (SELECT max(id) FROM {t}));")
out.append('COMMIT;')
open(os.path.join(ROOT, 'database', 'seed.sql'), 'w', encoding='utf8').write('\n'.join(out) + '\n')
print('seed.sql written')
