import requests

from . import users, operations, verifications, testblocks

__version__ = '/brightid/v5'


class Node:
    def __init__(self, url='http://node.brightid.org') -> None:
        self.url = url
        self.users = users.Users(self)
        self.operations = operations.Operations(self)
        self.verifications = verifications.Verifications(self)
        self.testblocks = testblocks.Testblocks(self)
    def ip(self):
        response = requests.get(f'{self.url}/{__version__}/ip')
        res = response.json()
        if res.get('error'):
            raise RuntimeError(res.get('errorMessage'))
        return res.get('data').get('ip')

    def state(self):
        response = requests.get(f'{self.url}/{__version__}/state')
        res = response.json()
        if res.get('error'):
            raise RuntimeError(res.get('errorMessage'))
        return res.get('data')
