import requests

__version__ = '/brightid/v5'


class Apps:
    def __init__(self, node):
        self.node = node

    def get(self, app=''):
        response = requests.get(f'{self.node.url}/{__version__}/apps/{app}')
        res = response.json()
        if res.get('error'):
            raise RuntimeError(res.get('errorMessage'))
        return res.get('data').get('apps') or res.get('data')
