import requests


class Testblocks:
    def __init__(self, node):
        self.node = node

    def put(self, app, action, context_id, testing_key):
        params = (
            ('testingKey', testing_key),
        )
        response = requests.put(
            f'{self.node.url}/testblocks/{app}/{action}/{context_id}', params=params)
        if not response.ok:
            res = response.json()
            self.node.check_error(res)

    def delete(self, app, action, context_id, testing_key):
        params = (
            ('testingKey', testing_key),
        )
        response = requests.delete(
            f'{self.node.url}/testblocks/{app}/{action}/{context_id}', params=params)
        if not response.ok:
            res = response.json()
            self.node.check_error(res)
