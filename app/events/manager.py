from datetime import datetime


async def get_events(date_from, date_to, cache):
    date_from = datetime.combine(date_from, datetime.min.time())
    date_to = datetime.combine(date_to, datetime.min.time())
    cursor = cache.common.events.find({'created': {'$gte': date_from, '$lte': date_to}}, {'_id': False})

    events = []
    while await cursor.fetch_next:
        event = cursor.next_object()
        event['created'] = event['created'].isoformat()
        events.append(event)
    return events
