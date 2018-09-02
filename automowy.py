# SPDX-License-Identifier: Unlicense

import requests


class AutomowyError(Exception):
    pass


class AutomowySession:
    AUTH_URL_BASE = 'https://iam-api.dss.husqvarnagroup.net/api/v3/token/'
    URL_BASE = 'https://amc-api.dss.husqvarnagroup.net/app/v1/'

    def __init__(self):
        self.session = requests.Session()
        self.user = None
        self.token = None
        self.mowers = None

    def login(self, user, password):
        response = self.session.post(
            self.AUTH_URL_BASE,
            json={'data': {
                'type': 'token',
                'attributes': {'username': user, 'password': password}
            }}
        )
        response.raise_for_status()
        self.user = user
        json = response.json()
        self.token = json['data']['id']
        provider = json['data']['attributes']['provider']
        self.session.headers.update({
            'Authorization': 'Bearer ' + self.token,
            'Authorization-Provider': provider
        })
        return self

    def logout(self):
        response = self.session.delete(self.AUTH_URL_BASE + self.token)
        response.raise_for_status()
        self.token = None
        del (self.session.headers['Authorization'])

    def list_mowers(self):
        response = self.session.get(
            self.URL_BASE + 'mowers'
        )
        response.raise_for_status()
        json = response.json()
        self.mowers = [
            {'id': mower['id'], 'name': mower['name']}
            for mower in json
        ]
        return json

    def find_mower(self, match=None):
        return Automowy(self, match)


class Automowy:
    def __init__(self, session, match=None):
        self.session = session
        if not session.mowers:
            session.list_mowers()
        if not len(self.session.mowers):
            raise AutomowyError('No mower for %s' % session.user)
        if match:
            for mower in session.mowers + [None]:
                if mower is None:
                    raise AutomowyError('No mower matching %s' % match)
                if mower['id'] == match or mower['name'] == match:
                    break
        else:
            mower = session.mowers[0]
        self.name = mower['name']
        self.id = mower['id']
        self.url = session.URL_BASE + 'mowers/%s/' % self.id

    def query(self, command):
        """
        :param command: can be 'status', 'geofence' or 'settings'
        """
        response = self.session.session.get(
            self.url + command
        )
        response.raise_for_status()
        return response.json()

    def control(self, command, param=None):
        """
        :param command: can be 'start', 'start/override/period',
            'pause', 'park', 'park/duration/timer'
        :param param: must be {'period':minutes} for 'start/override/period'
        """
        response = self.session.session.post(
            self.url + 'control/%s' % command,
            json=param
        )
        response.raise_for_status()
        return response.json()

    def set(self, key, value):
        """
        :param key: examples: 'cuttingHeight', 'ecoMode'
        """
        response = self.session.session.put(
            self.url + 'settings',
            json={'settings': {key: value}}
        )
        response.raise_for_status()
