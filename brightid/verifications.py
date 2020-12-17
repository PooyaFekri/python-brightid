import requests


class Verifications:
    def __init__(self, node):
        self.node = node

    def get(self, app, context_id='', **kwargs):
        params = (
            ('timestamp', kwargs.get('timestamp')),
            ('signed', kwargs.get('signed')),
            ('count_only', kwargs.get('count_only'))
        )
        response = requests.get(f'{self.node.url}/verifications/{app}/{context_id}', params=params)
        res = response.json()
        self.node.check_error(res)
        if res.get('data').get('count') and kwargs.get('count_only'):
            return res.get('data').get('count')
        return res.get('data')
