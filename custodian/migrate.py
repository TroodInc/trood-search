import os
import json
import requests
import glob
import logging

from utils import get_service_token

from loaddata import FixtureLoader


logger = logging.getLogger(__name__)


class Migrator:

    def __init__(self):
        self.headers = {
            'Authorization': get_service_token(),
            'Content-Type': 'application/json'
        }
        self.host = 'http://127.0.0.1:8000/custodian/migrations'

    def get_migrations(self):
        def sort_key(migration):
            migration_name = migration.split('/')[-1]
            migration_index = int(migration_name.split('_')[0])
            return migration_index

        migrations_list = glob.glob('/home/migrations/*.json')
        migrations_list = sorted(migrations_list, key=sort_key)
        return migrations_list

    def get_last_current_migration(self):
        response = requests.get(self.host, headers=self.headers)
        response.raise_for_status()
        migrations = response.json()['data']
        last_migration = None
        for migration in migrations:
            if last_migration is None:
                last_migration = migration

            if migration['Data']['order'] > last_migration['Data']['order']:
                last_migration = migration

        return last_migration

    def apply_migrations(self, migrations):
        last_migration = self.get_last_current_migration()
        for i, migration in enumerate(migrations, start=1):
            if last_migration is not None and i <= last_migration['Data']['order']:
                print('Is applied {}'.format(migration))
                continue

            self.apply_migration(migration)

    def apply_migration(self, migration):
        migration_name = os.path.basename(migration)
        with open(migration, 'r') as migration_file:
            migration_data = json.loads('\n'.join(migration_file.readlines()))

        response = requests.post(
            '{}/apply'.format(self.host), json=migration_data, headers=self.headers
        )

        obj_name = migration_data['operations'][0].get('object', {}).get('name')
        if obj_name:
            self.apply_fixtures(obj_name)

        data = response.json()
        error = json.dumps(data, indent=2)
        if data['status'] == 'OK':
            print('Migration {} applied.'.format(migration_name))
        else:
            print('Failed to apply migration {}. {}'.format(migration_name, error))

    def apply_fixtures(self, name):
        loader = FixtureLoader(
            host='http://127.0.0.1:8000', fixtures='/home/.fixtures/*.json'
        )
        for fixture in loader.get_fixtures():
            if fixture.split('/')[-1].split('.')[0][:-1] == name:
                loader.apply_fixture(fixture)


def migrate():
    migrator = Migrator()
    migrations = migrator.get_migrations()
    migrator.apply_migrations(migrations)


if __name__ == "__main__":
    migrate()
