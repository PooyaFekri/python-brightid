import requests

from . import users, operations, verifications, testblocks, apps


class Node:
    def __init__(self, url='http://node.brightid.org/brightid/v5'):
        self.url = url
        self.users = users.Users(self)
        self.operations = operations.Operations(self)
        self.verifications = verifications.Verifications(self)
        self.testblocks = testblocks.Testblocks(self)
        self.apps = apps.Apps(self)
    def ip(self):
        response = requests.get(f'{self.url}/ip')
        res = response.json()
        self.check_error(res)
        return res.get('data').get('ip')

    def state(self):
        response = requests.get(f'{self.url}/state')
        res = response.json()
        self.check_error(res)
        return res.get('data')

    def check_error(self, res):
        if res.get('error'):
            raise RuntimeError(res.get('errorMessage'))