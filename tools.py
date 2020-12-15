import pyqrcode


def creat_deep_link(context, context_id, url='http://node.brightid.org', format='long'):
    url = url.replace('/', '%2f')
    if format == 'long':
        deep_link = f'https://app.brightid.org/link-verification/{url}/{context}/{context_id}/'
    elif format == 'short':
        deep_link = f'brightid://link-verification/{url}/{context}/{context_id}'
    else:
        raise RuntimeError('Wrong format')
    return deep_link


def createQR(deep_link):
    qr = pyqrcode.create(deep_link)
    return qr.png_as_base64_str()
