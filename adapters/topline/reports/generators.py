async def get_pipeline_report(date_from, date_to, request):
    async with request['db'].acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT DISTINCT ON (t.instance_id) t.status_id, t.assignee_id, t.created, s._price
                FROM sells_selltransfer AS t
                JOIN sells_sell AS s ON s.id = t.instance_id
                WHERE cast(t.created AS DATE) <= %(created_date)s
                ORDER BY t.instance_id ASC, t.created DESC
            """, {'created_date': date_to})

            transfers_set = await cur.fetchall()
            await cur.execute("""
                SELECT ID, name, "order", status_type FROM sells_status
                ORDER BY "order" ASC
            """)
            status_set = await cur.fetchall()
            report = {
                'sells_in_work': 0,
                'status_reports': []
            }
            for status in status_set:
                if status[3] in ('SUCCESS', 'FAIL'):
                    status_transfers = [
                        transfer for transfer in transfers_set if
                        transfer[2].date() >= date_from and transfer[0] == status[0]
                        ]
                else:
                    status_transfers = [transfer for transfer in transfers_set if transfer[0] == status[0]]
                sells_in_status = len(status_transfers)
                report['status_reports'].append({
                    'status': {
                        'id': status[0],
                        'name': status[1],
                        'order': status[2],
                        'status_type': status[3]
                    },
                    'sells_in_status': sells_in_status,
                    'sells': [{
                                  'assignee': transfer[1],
                                  'created': transfer[2].strftime("%Y-%m-%d %H:%M:%S"),
                                  'price': str(transfer[3]) if transfer[3] else '0'
                              } for transfer in status_transfers]
                })
                report['sells_in_work'] += sells_in_status
    return report
