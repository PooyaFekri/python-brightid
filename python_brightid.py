# Be name khoda
import base64
import time
import json
import ed25519
import pyqrcode
import requests
import os

__version__ = 5  # if you want use another version just change this line


NODE_URL = f'http://node.brightid.org/brightid/v{__version__}'
APP_URL = f'https://app.brightid.org/node/v{__version__}'
DEEP_LINK = 'node.brightid.org'


class BrightId:
    def __init__(self, context='', sponser_private='', testing_key='') -> None:
        '''

        '''
        self.context = context
        self.api = self.Api(context, testing_key)
        self.operation = self.Operation(context, sponser_private)
        self.sponser_private = sponser_private
        self.testing_key = testing_key

    class Api:
        def __init__(self, context, testing_key) -> None:
            self.context = context
            self.testing_key = testing_key

        def verifications(self, context_id='', context='', *args, **kwargs) -> dict:
            '''
            by defualt use context enter when create instance of BrightId,
            but you can use another context by send it to function
            you can pass params -> count_only=(True), signed=(nacl or eth) and timestamp=(seconds or milliseconds)
            return dict,in good request key is data,
            but in bad request keys will be error:bool, errorNum:int, errorMessage:string, code: int
            '''
            params_key = ('count_only', 'timestamp', 'signed')
            params = []
            url = f'{APP_URL}/verifications/{context or self.context}/{context_id}?'
            for i in kwargs:
                if i in params_key:
                    params.append((i, kwargs[i]))

            for i in params:
                if i[0] == 'count_only':
                    url += i[0] + '&'
                    continue
                url += f'{i[0]}={i[1]}&'
            response = requests.get(url)
            return response.json()

        def app(self, context=''):
            url = APP_URL + f'/apps/{context or self.context}'
            response = requests.get(url)
            return response.json()

        def deep_link(self, context_id, context='') -> str:
            '''
            return link
            '''
            _link = f'{APP_URL[:APP_URL.find("/node")]}/link-verification/http:%2f%2f{DEEP_LINK}/{context or self.context}/{context_id}/'
            return _link

        def qr(self, context_id, context='', dir='', *args, **kwargs):
            '''
            create qr code as png file in dir as name context_id.png
            defualt scale is 8 but you can change it with scale=int
            '''
            qr_link = f'brightid://link-verification/http:%2f%2f{NODE_URL}/{context or self.context}/{context_id}'
            qrCode = pyqrcode.create(qr_link)
            if dir and not os.path.exists(dir):
                os.makedirs(dir)
            qrCode.png(dir+'/'+context_id+'.png',
                       scale=kwargs.get('scale') or '8')

        def block_user_verification(self, context_id, action, context='', testing_key=''):
            '''
            action = ('sponsorship', 'link', 'verification')
            in bad request return dict that keys will be error:bool, errorNum:int, errorMessage:string, code: int
            '''
            url = NODE_URL + \
                f'/testblocks/{context or self.context}/{action}/{context_id}'
            params = (
                ('testingKey', testing_key or self.testing_key),
            )
            response = requests.put(url, params=params)
            return response

        def remove_block_user_verification(self, context_id, action, context='', testing_key=''):
            '''
            action = ('sponsorship', 'link', 'verification')
            in bad request return dict that keys will be error:bool, errorNum:int, errorMessage:string, code: int
            '''
            url = NODE_URL + \
                f'/testblocks/{context or self.context}/{action}/{context_id}'
            params = (('testingKey', testing_key or self.testing_key),)
            response = requests.delete(url, params=params)
            return response

    class Operation:
        '''
        inner class to use operations function more suitable
        '''

        def __init__(self, context, sponser_private) -> None:
            self.conetxt = context
            self.sponser_private = sponser_private

        def sponser(self, context_id='', context='', sponser_private='', *args, **kwargs) -> dict:
            '''
            sponser context_id 
            return dict, if <response 200> dict has key data:dict
            else <response 400> or <response 500> it has key error:bool, errorNum:int, errorMessage:str, code:int
            '''
            URL = NODE_URL + '/operations'
            op = {
                'name': 'Sponsor',
                'app': context or self.conetxt,
                'context_id': context_id,
                'timestamp': int(time.time()*1000),
                'v': 5
            }
            signing_key = ed25519.SigningKey(base64.b64decode(
                sponser_private or self.sponser_private))
            message = json.dumps(op, sort_keys=True,
                                 separators=(',', ':')).encode('ascii')
            sig = signing_key.sign(message)
            op['sig'] = base64.b64encode(sig).decode('ascii')
            response = requests.post(URL, json=op)
            return response.json()


# Dar panah khoda
