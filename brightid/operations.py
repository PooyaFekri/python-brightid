import requests
import ed25519
import base64
import json

__version__ = '/brightid/v5'


class Operations:
    def __init__(self, node) -> None:
        self.node = node

    def sign(self, op, private):
        signing_key = ed25519.SigningKey(base64.b64decode(private))
        message = json.dumps(op, sort_keys=True,
                             separators=(',', ':')).encode('ascii')
        sig = signing_key.sign(message)
        sig = base64.b64encode(sig).decode('ascii')
        return sig

    def post(self, op):
        response = requests.post(
            f'{self.node.url}/{__version__}/operations', data=op)
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
