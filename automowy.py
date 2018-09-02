# SPDX-License-Identifier: Unlicense

import requests


class AutomowySession:
    AUTH_URL_BASE = 'https://iam-api.dss.husqvarnagroup.net/api/v3/token/'

    def __init__(self):
        self.session = requests.Session()
        self.user = None
        self.token = None

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
