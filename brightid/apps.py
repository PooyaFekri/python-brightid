import requests


class Apps:
    def __init__(self, node):
        self.node = node

    def get(self, app=''):
        response = requests.get(f'{self.node.url}/apps/{app}')
        res = response.json()
        self.node.check_error(res)
        return res.get('data').get('apps') or res.get('data')
