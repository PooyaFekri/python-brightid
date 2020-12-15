import requests


class Operations:
    def __init__(self, node):
        self.node = node

    def post(self, op):
        response = requests.post(
            f'{self.node.url}/operations', json=op)
        res = response.json()
        self.node.check_error(res)
        return res.get('data').get('hash')

    def get(self, hash):
        response = requests.get(
            f'{self.node.url}/operations/{hash}')
        res = response.json()
        self.node.check_error(res)
        return res.get('data')
