import requests

__version__ = '/brightid/v5'


class Testblocks:
    def __init__(self, node) -> None:
        self.node = node

    def put(self, app, action, context_id, testing_key):
        params = (
            ('testingKey', testing_key),
        )
        response = requests.put(
            f'{self.node.url}/{__version__}/testblocks/{app}/{action}/{context_id}', params=params)
        try:
            res = response.json()
        except:
            return
        if res.get('error'):
            raise RuntimeError(res.get('errorMessage'))

    def delete(self, app, action, context_id, testing_key):
        params = (
            ('testingKey', testing_key),
        )
        response = requests.delete(
            f'{self.node.url}/{__version__}/testblocks/{app}/{action}/{context_id}', params=params)
        try:
            res = response.json()
        except:
            return
        if res.get('error'):
            raise RuntimeError(res.get('errorMessage'))
