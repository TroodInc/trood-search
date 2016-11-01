from app.authentication import BaseAuthentication


class MirrorAuthentication(BaseAuthentication):
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
                    SELECT t.user_id FROM authtoken_token AS t
                    JOIN users_genericuser u ON u.id = t.user_id
                    JOIN django_content_type ct ON ct.id = u.content_type_id
                    WHERE ct.model = 'clientmanager' AND key = %(token)s
                """, {'token': token})
                row = await cur.fetchone()
                if row:
                    self.request['user_id'] = row[0]
                    return True
                else:
                    return False
