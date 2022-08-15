import requests
import time


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

    def sponsor(self, key, app, app_user_id):
        unusedSponsorships = self.node.apps.unusedSponsorships(app)
        if(unusedSponsorships < 1):
            raise RuntimeError(app + ' does not have any unused sponsorships')
        op = {
         'name': 'Sponsor',
         'app': app,
         'appUserId': app_user_id,
         'timestamp': int(time.time()*1000),
         'v': 6
        }
        op['sig'] = self.node.tools.sign(op, key)
        self.node.operations.post(op)

