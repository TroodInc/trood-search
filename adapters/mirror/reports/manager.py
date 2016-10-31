async def get_summary_reports(project_id_list, request):
    cursor = request['cache'].mirror.summary_report.find({'id': {'$in': project_id_list}}, {'_id': False})

    reports = []
    while await cursor.fetch_next:
        report = cursor.next_object()
        reports.append(report)
    return reports


async def get_dynamic_reports(project_id_list, request):
    cursor = request['cache'].mirror.dynamic_report.find({'id': {'$in': project_id_list}}, {'_id': False})

    reports = []
    while await cursor.fetch_next:
        report = cursor.next_object()
        reports.append(report)
    return reports


async def get_projects_for_manager(manager_id, pool):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT p.id FROM projects_project as p
                JOIN clients_client c on p.client_id = c.id
                JOIN clients_clientmanager cm ON c.id = cm.client_id
                JOIN users_genericuser u ON u.object_id = cm.id
                JOIN django_content_type ct ON ct.id = u.content_type_id
                WHERE ct.model = 'clientmanager' and u.id = %s
            """, (manager_id, ))
            projects = await cur.fetchall()
            projects_id_list = [project[0] for project in projects]
    return projects_id_list
