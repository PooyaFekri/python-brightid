import requests

__version__ = '/brightid/v5'


class Users:
    def __init__(self, node) -> None:
        self.node = node

    def get(self, user):
        response = requests.get(
            f'{self.node.url}/{__version__}/users/{user}')
        res = response.json()
        if res.get('error'):
            raise RuntimeError(res.get('errorMessage'))
        return res.get('data')

    def verifications(self, user):
        response = requests.get(
            f'{self.node.url}/{__version__}/users/{user}/verifications')
        res = response.json()
        if res.get('error'):
            raise RuntimeError(res.get('errorMessage'))
        return res.get('data').get('verifications')

    def connections(self, user, direction):
        response = requests.get(
            f'{self.node.url}/{__version__}/users/{user}/connections/{direction}')
        res = response.json()
        if res.get('error'):
            raise RuntimeError(res.get('errorMessage'))
        return res.get('data').get('connections')

    def profile(self, user, requestor):
        response = requests.get(
            f'{self.node.url}/{__version__}/users/{user}/profile/{requestor}')
        res = response.json()
        if res.get('error'):
            raise RuntimeError(res.get('errorMessage'))
        return res.get('data')
