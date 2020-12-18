import ed25519
import json
import base64
import pyqrcode


def create_deep_link(context, context_id, url='http://node.brightid.org', schema='https'):
    url = url.replace('/', '%2f')
    if schema == 'brightid':
        deep_link = f'brightid://link-verification/{url}/{context}/{context_id}'
    else:
        deep_link = f'https://app.brightid.org/link-verification/{url}/{context}/{context_id}/'
    return deep_link


def create_qr(deep_link, scale=8):
    qr = pyqrcode.create(deep_link)
    return qr.png_as_base64_str(scale=scale)


def sign(op, private):
    signing_key = ed25519.SigningKey(base64.b64decode(private))
    message = json.dumps(op, sort_keys=True,
                         separators=(',', ':')).encode('ascii')
    sig = signing_key.sign(message)
    sig = base64.b64encode(sig).decode('ascii')
    return sig


def create_bright_id():
    private, public = ed25519.create_keypair()
    private = base64.b64encode(private.to_bytes()).decode('ascii')
    public = base64.b64encode(public.to_bytes()).decode('ascii')
    id = public.strip('=').replace('/', '_').replace('+', '-')
    return {
        'id': id,
        'private': private,
        'public': public
    }
