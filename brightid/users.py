import requests

class Users:
    def __init__(self, node):
        self.node = node

    def get(self, user):
        response = requests.get(
            f'{self.node.url}/users/{user}')
        res = response.json()
        self.node.check_error(res)
        return res.get('data')

    def verifications(self, user):
        response = requests.get(
            f'{self.node.url}/users/{user}/verifications')
        res = response.json()
        self.node.check_error(res)
        return res.get('data').get('verifications')

    def connections(self, user, direction):
        response = requests.get(
            f'{self.node.url}/users/{user}/connections/{direction}')
        res = response.json()
        self.node.check_error(res)
        return res.get('data').get('connections')

    def profile(self, user, requestor):
        response = requests.get(
            f'{self.node.url}/users/{user}/profile/{requestor}')
        res = response.json()
        self.node.check_error(res)
        return res.get('data')
