from itertools import count
import requests

__version__ = '/brightid/v5'


class Verifications:
    def __init__(self, node) -> None:
        self.node = node

    def get(self, app, context_id='', **kwargs):
        params_key = ('count_only', 'timestamp', 'signed')
        params = []
        url = f'{self.node.url}/{__version__}/verifications/{app}/{context_id}?'
        for i in kwargs:
            if i in params_key:
                params.append((i, kwargs[i]))
        for i in params:
            if i[0] == 'count_only':
                url += i[0] + '&'
                continue
            url += f'{i[0]}={i[1]}&'
        response = requests.get(url)
        res = response.json()
        if res.get('error'):
            raise RuntimeError(res.get('errorMessage'))
        if res.get('data').get('count') and kwargs.get('count_only'):
            return res.get('data').get('count')
        return res.get('data')
