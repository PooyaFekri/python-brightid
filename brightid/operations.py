import requests

__version__ = '/brightid/v5'


class Operations:
    def __init__(self, node) -> None:
        self.node = node

    def post(self, op):
        response = requests.post(
            f'{self.node.url}/{__version__}/operations', json=op)
        res = response.json()
        if res.get('error'):
            raise RuntimeError(res.get('errorMessage'))
        return res.get('data').get('hash')

    def get(self, hash):
        response = requests.get(
            f'{self.node.url}/{__version__}/operations/{hash}')
        res = response.json()
        if res.get('error'):
            raise RuntimeError(res.get('errorMessage'))
        return res.get('data')
