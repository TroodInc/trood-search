from psycopg2.extras import DictCursor

from adapters.mirror.constants import EXAMINATION_ACCEPTED_BY_CLIENT
from adapters.mirror.reports.place_summary_report import build_place_report


async def get_summary_report(project_id, request):
    cursor = request['cache'].mirror.summary_reports.find({'project_id': project_id})

    summary_report = []
    for report in (await cursor.to_list(length=100)):
        summary_report.append(report['report'])
    return summary_report


async def generate_base_place_report(project_id, place_id, pool, cache):
    async with pool.acquire() as conn:
        async with conn.cursor(cursor_factory=DictCursor) as cur:
            await cur.execute("""
                SELECT id FROM projects_examination
                WHERE status = %s AND project_id = %s
                AND place_id = %s AND point_not_work = FALSE
            """, (EXAMINATION_ACCEPTED_BY_CLIENT, project_id, place_id))
            examinations_list = await cur.fetchall()

            await cur.execute("""
                SELECT title, place_tags_string FROM clients_place
                WHERE id = %s
            """, (place_id,))
            place = await cur.fetchone()
            place_labels = place['place_tags_string'].split(',') if place['place_tags_string'].strip() else []

            await cur.execute("""
                SELECT examination_id, content, seller, exit_time, entry_time, visit_date
                FROM questionnaires_completedquestionnaire
                WHERE id = ANY(%s)
            """, (examinations_list,))
            questionnaire_list = await cur.fetchall()
            questionnaire_dict = {
                questionnaire['examination_id']: questionnaire for questionnaire in questionnaire_list
                }
            result = build_place_report(examinations_list, questionnaire_dict, place['title'], place_labels)

    cache.mirror.summary_reports.update(
        spec={
            'project_id': project_id,
            'place_id': place_id,
        },
        document={
            'project_id': project_id,
            'place_id': place_id,
            'report': result
        },
        upsert=True
    )
    return result
