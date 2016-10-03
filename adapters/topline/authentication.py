async def is_authenticated(request):
    token_string = request.headers.get('Authorization')
    if not token_string:
        return False
    try:
        token = token_string.split()[1]
    except IndexError:
        return False
    async with request['db'].acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                SELECT user_id FROM authtoken_token
                WHERE key = %(token)s
            """, {'token': token})
            row = await cur.fetchone()
            if row:
                return True
            else:
                return False
