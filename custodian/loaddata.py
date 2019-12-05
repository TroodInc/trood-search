import argparse
import os
import json
import requests
import glob
import logging

from utils import get_service_token

logger = logging.getLogger(__name__)


class FixtureLoader:

    def __init__(self, host, fixtures, no_input=False, token=None, **kwargs):
        if token is None:
            token = get_service_token()

        self.headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        self.host = '{}/custodian/data'.format(host)
        self.fixtures_path = fixtures
        if not no_input and self.is_work_host():
            a = input('Do you realy upload fixtures on {} y/[n|any]: '.format(host))
            if a != 'y':
                raise Exception('Droped')

    def is_work_host(self):
        return 'trood.com' in self.host

    def get_fixtures(self):
        return glob.glob(self.fixtures_path)

    def apply_fixtures(self, fixtures, update=False):
        for fixture in sorted(fixtures):
            self.apply_fixture(fixture, update=update)

    def apply_fixture(self, fixture, update=False):
        name = os.path.basename(fixture).split('.')[0][:-1]
        data = json.load(open(fixture))
        url = '{}/{}'.format(self.host, name)
        if update:
            response = requests.patch(url, json=data, headers=self.headers)
            if response.status_code != 200:
                print('Fixtures: {} update FALSE'.format(name))
                print(response.status_code)
                print(json.dumps(response.json(), indent=2))
            else:
                print('Fixture: {} updated.'.format(name))
        else:
            created, updated = 0, 0
            for bo in data:
                response = requests.post(url, json=bo, headers=self.headers)
                if response.status_code == 400 and response.json()['error']['Code'] == 'duplicated_value_error':
                    response = requests.patch(url, json=bo, headers=self.headers)
                    updated += 1
                    continue

                if response.status_code != 200:
                    print('Fixture {} data {} not uploaded.'.format(name, bo))
                    print(response.status_code)
                    print(json.dumps(response.json(), indent=2))
                    return
                
                created += 1

            print('Fixture: {} objects: {} created, {} updated.'.format(name, created, updated))


def load_fixtures(**kwargs):
    loader = FixtureLoader(**kwargs)
    fixtures = loader.get_fixtures()
    loader.apply_fixtures(sorted(fixtures), update=kwargs['update'])


def main():
    parser = argparse.ArgumentParser(description='Load BO fixtures.')
    parser.add_argument(
        '--host',
        dest='host',
        metavar='http://127.0.0.1:8000',
        type=str,
        nargs='?',
        default='http://127.0.0.1:8000',
        help='Custodian hostname'
    )
    parser.add_argument(
        '--fixtures',
        dest='fixtures',
        metavar='../custodian/.fixtures/*.json',
        type=str,
        nargs='?',
        default='../custodian/.fixtures/*.json',
        help='Path to BO fixtures'
    )
    parser.add_argument(
        '--no-input', action='store_true', help='Don\'t ask questions.'
    )
    parser.add_argument(
        '--token',
        dest='token',
        metavar='1815b607368741f9aec0109ae0f26b0d',
        type=str,
        nargs='?',
        default=None,
        help='User access token'
    )
    parser.add_argument(
        '--update',
        dest='update',
        action='store_true',
        default=False,
        help='Update fixture values instead of creation'
    )

    args = parser.parse_args()
    kwargs = {
        'host': args.host,
        'fixtures': args.fixtures,
        'no_input': args.no_input,
        'token': args.token,
        'update': args.update
    }

    load_fixtures(**kwargs)


if __name__ == "__main__":
    main()
