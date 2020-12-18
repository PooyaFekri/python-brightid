# python-brightid

BrightID SDK for Python

##Introduction

This library provides a Python interface for the [BrightID API](https://dev.brightid.org/docs/node-api/web_services/foxx/node-api-5.6.0.yaml). It's compatible with Python 3 and supports BrightID API 5. In addition to the API implementation, this library provides required tools to make BrightID integration easy and straightforward for app developers[BrightID DEV](dev.brightid.org).

##Installing

You can install or upgrade python-brightid using:

    $ pip3 install python-brightid --upgrade

Or you can install from source with:

    $ git clone https://github.com/PooyaFekri/python-brightid.git
    $ cd python-brightid
    $ python3 setup.py install

##Integrating apps

Apps can use BrightID to make sure their users have no multiple accounts. To verify uniquness of a user, app should:

1. Create a unique `context_id` for the user

   > > > import uuid
   > > > context = 'top-up-gifter'
   > > > context_id = uuid.uuid4().hex
   > > > context_id
   > > > 'a9ee5dc6ac114c95af50ef90225e0e53'

2. Create a deep link with that `context_id`

   > > > url = 'http://node.brightid.org'
   > > > deep_link = brightid.tools.create_deep_link(context, context_id, url)
   > > > node = brightid.Node('http://node.brightid.org/brightid/v5')
   > > > brightid.tools.create_qr(deep_link)
   > > > 'iVBORw0KGgoAAAANSUhEUgAAAggAAA...dKGIAAAAAElFTkSuQmCC'

3. Ask the user to click the deep link or scan the QR code representation to link their BrightID to that `context_id`

4. Query BrightID nodes to check if the BrightID that linked the `context_id` is verified.

   > > > app = 'top-up-gifter'
   > > > try:
   > > > ... v = node.verifications.get(app, context_id)
   > > > ... except Exception as e:
   > > > ... print(str(e))
   > > > ...

If exception is raised and `str(e)` is:

- `context_id not found`, it means that user did not link the `context_id` to the BrightID yet. The app should query again after a while in such case.

- `user can not be verified for this app`, it means user is not verified on BrightID yet. The app should ask user to return back after [getting verified](https://brightid.gitbook.io/brightid/getting-verified) on BrightID.

- `user is not sponsored`, it means that user is not [sponsored](https://dev.brightid.org/docs/guides/docs/basic-integration.md#sponsoring-users) and app should sponsor the user by signing and sending a `Sponsor` operation, wait about 10 seconds for the operation to get applied, and then query again.

```
    >>> import brightid
    >>> import time
    >>> node = brightid.Node('http://node.brightid.org/brightid/v5')
    >>> op = {
    ...     'name': 'Sponsor',
    ...     'app': app,
    ...     'context_id': context_id,
    ...     'timestamp': int(time.time()*1000),
    ...     'v': 5
    ... }
    >>> sponsor_private_key = 'rXSGf0ka3WsvsX...ZKwujpNH51Q=='
    >>> op['sig'] = brightid.tools.sign(op, sponsor_private_key)
    >>> op['sig']
    '7wOmXH1ivk104a9kO5mWkslWstYnWnRtnS/jtXEz3P1PyxhTh06i3H0yZpIrST/iiYpd15iscCuyGJpghnOXDw=='
    >>> node.operations.post(op)
    'rFT1ASgPQuxUx0XfMq9EjBbuzCOaoOw_sdklaDamPXw'
    >>> time.sleep(10)
    >>> try:
    ...     v = node.verifications.get(app, context_id)
    ... except Exception as e:
    ...     print(str(e))
    ...
    >>> v
    {'unique': True, 'app': 'top-up-gifter', 'context': 'top-up-gifter', 'context_ids': ['a9ee5dc6ac114c95af50ef90225e0e53', '6e85ac7a7a1945d352de5c422db69f72']}
```

5. check its database to ensure none of linked `context_id`s by this user got the service supposed to be provided once for each user before. The response has a list of all `context_ids` the BrightID user linked under this context which can be used by app for this purpose.

##Using API

See BrightID API documantion in [BrightID API](https://dev.brightid.org/docs/node-api)

#### Connecting to Node

    >>> import brightid
    >>> node = brightid.Node('http://node.brightid.org/brightid/v5')
    >>> node.state()
    {'lastProcessedBlock': 3946366, 'verificationsBlock': 3946320, 'initOp': 0, 'sentOp': 248}
    >>> node.ip()
    '68.183.76.106'

#### Getting users data with brightid

    >>> id = 'kwQyKj5RS5DzPq9bvaNTKv0E6JxYIorylnF0ACUFbH0'
    >>> node.users.get(id)
    {'createdAt': 1553249775161, 'flaggers': {}, 'connections': [...], 'groups': [...],     'invites': [...], 'isSponsored': True, 'trusted': [...], 'verifications': [...]}
    >>> # direction can be 'inbound'/'outbound'
    >>> node.users.connections(id, direction='inbound')
    [{'id': '33Vo27uqL0KGRTytjV9ScJbSTJj1YskRZUjGk-DuO0A', 'level': 'already known', 'timestamp': 1553265996463}, ...]
    >>> requestor='0wT96mjCAje7If7qjUyrzkVYBPoLPu3tfOzesdT3ShE'
    >>> node.users.profile(id, requestor)
    {'connectionsNum': 6, 'groupsNum': 3, 'mutualConnections': ['hPAwqCeceA8quMdvo9TYU996iNBByuc65SrnXSvHgMs'], 'mutualGroups': ['IXDLiaHwMXKKHjSYUdOXMHPG1tJRTCa_Y0FjvSszEDE'], 'connectedAt': 1589978985397, 'createdAt': 1553249775161, 'reports': [], 'verifications': [{'name': 'BrightID', 'timestamp': 1604002284314}, ...]}
    >>> node.users.verifications(id)
    [{'name': 'BrightID', 'timestamp': 1604002284314}, {'name': 'Yekta', 'rank': 1, 'timestamp': 1608280959867, 'raw_rank': 4.596579161873709}, ...]

#### Getting apps data

    >>> node.apps.get()
    [{'id': '1hive', 'name': '1Hive Honey Faucet', 'context': '1hive', 'verification': 'BrightID', 'logo': 'data:image/png;base64,iVBoAYFAw...rkJggg==', 'url': 'https://1hive.org/', 'assignedSponsorships': 7775, 'unusedSponsorships': 701}, ...]
    >>> app = 'top-up-gifter'
    >>> node.apps.get(app)
    {'id': 'top-up-gifter', 'name': 'Top-up Gifter', 'context': 'top-up-gifter', 'verification': 'BrightID', 'logo': 'data:image/png;base64,iVBORF...YII=', 'url': 'https://t.me/top_up_gifter_bot', 'assignedSponsorships': 100, 'unusedSponsorships': 95}

#### Getting verifications data

    >>> node.verifications.get(app)
    {'count': 68, 'context_ids': ['6847e75f4351f70836c2e6330fb3d8ac', '6e85ac7a7a1945d352de5c422db69f72', ...]}
    >>> node.verifications.get(app, count_only=True)
    68
    >>> node.verifications.get(app, context_id, singed='eth', timestamp='seconds')
    {'unique': True, 'app': 'top-up-gifter', 'context': 'top-up-gifter', 'context_ids': ['dc100f7d468b232e65aa5545d718caa3', '386039e2db5916e1375b6227bf900b58'], 'timestamp': 1608282563}

#### Blocking verification for test

    >>> action='sponsorship' # sponsorship/link/verification are valid actions
    >>> testing_key='a8...OtD'
    >>> node.testblocks.put(app, action, context_id, testing_key)
    >>> try:
    ...     node.verifications.get(app, context_id, singed='eth', timestamp='seconds')
    ... except Exception as e:
    ...     print(str(e))
    ...
    user is not sponsored
    >>> node.testblocks.delete(app, action, context_id, testing_key)
    >>> node.verifications.get(app, context_id, singed='eth', timestamp='seconds')
    {'unique': True, 'app': 'top-up-gifter', 'context': 'top-up-gifter', 'context_ids': ['dc100f7d468b232e65aa5545d718caa3', '386039e2db5916e1375b6227bf900b58'], 'timestamp': 1608282714}

#### Posting operations

    >>> import time
    >>> user = brightid.tools.create_bright_id()
    >>> user
    {'id': 'Coh5IsaAGakYssl6_97nVN2MjLigOCAv_-OjWRpb4BY', 'private': '4ZiWpKli3PTW2CSlf7nqp4gp0H9ifxfSMGc0E5QCTogKiHkixoAZqRiyyXr/3udU3YyMuKA4IC//46NZGlvgFg==', 'public': 'Coh5IsaAGakYssl6/97nVN2MjLigOCAv/+OjWRpb4BY='}
    >>> op = {
    ...     'name': 'Connect',
    ...     'id1': user['id'],
    ...     'id2': id,
    ...     'level': 'just met',
    ...     'timestamp': int(time.time() * 1000),
    ...     'v': 5
    ... }
    >>> op['sig1'] = brightid.tools.sign(op, user['private'])
    >>> op['sig1']
    'JMx1erPZh+P0/en033JT7CgRycsO70WQCRHW+QADt22HzI5PK8zMUfzui1rXf9NJJm9eEtsYIYhqQa96AWJPDQ=='
    >>> op_hash = node.operations.post(op)
    >>> op_hash
    'ZB6LCV21fg2yDJPM8yqX_gZrsAU5ee9rrkP8u8YKS5s'
    >>> node.operations.get(op_hash)
    {'state': 'applied', 'result': None}
