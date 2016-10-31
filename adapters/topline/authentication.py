from app.authentication import BaseAuthentication


class ToplineAuthentication(BaseAuthentication):
    async def authenticate(self):
        token_string = self.request.headers.get('Authorization')
        if not token_string:
            return False
        try:
            token = token_string.split()[1]
        except IndexError:
            return False
        async with self.request['db'].acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    SELECT user_id FROM authtoken_token
                    WHERE key = %(token)s
                """, {'token': token})
                row = await cur.fetchone()
                if row:
                    self.request['user_id'] = row[0]
                    return True
                else:
                    return False
