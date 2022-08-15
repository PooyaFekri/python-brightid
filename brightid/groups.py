import requests

class Groups:
    def __init__(self, node):
        self.node = node

    def get(self, group):
        response = requests.get(
            f'{self.node.url}/groups/{group}')
        res = response.json()
        self.node.check_error(res)
        return res.get('data')

