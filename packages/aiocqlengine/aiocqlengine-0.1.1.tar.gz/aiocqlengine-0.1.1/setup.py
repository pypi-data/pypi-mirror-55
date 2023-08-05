# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiocqlengine']

package_data = \
{'': ['*']}

install_requires = \
['aiocassandra>=2.0,<3.0', 'cassandra-driver>=3.20,<4.0']

setup_kwargs = {
    'name': 'aiocqlengine',
    'version': '0.1.1',
    'description': 'Async wrapper for cqlengine of cassandra python driver.',
    'long_description': "# aiocqlengine\nAsync wrapper for cqlengine of cassandra python driver.\n\nThis project is built on [cassandra-python-driver](https://github.com/datastax/python-driver) and [aiocassandra](https://github.com/aio-libs/aiocassandra).\n\n[![Actions Status](https://github.com/charact3/aiocqlengine/workflows/unittest/badge.svg)](https://github.com/charact3/aiocqlengine/actions)\n\n## Installation\n```sh\n$ pip install aiocqlengine\n```\n\n## Get Started\n\n```python\nimport asyncio\nimport uuid\nimport os\n\nfrom aiocassandra import aiosession\nfrom aiocqlengine.models import AioModel\nfrom cassandra.cluster import Cluster\nfrom cassandra.cqlengine import columns, connection, management\n\ncluster = Cluster()\nsession = cluster.connect()\n\n\nclass User(AioModel):\n    user_id = columns.UUID(primary_key=True)\n    username = columns.Text()\n\n\nasync def main():\n    aiosession(session)\n\n    # Set aiosession for cqlengine\n    session.set_keyspace('example_keyspace')\n    connection.set_session(session)\n\n    # Model.objects.create() and Model.create() in async way:\n    user_id = uuid.uuid4()\n    await User.objects.async_create(user_id=user_id, username='user1')\n    # also can use: await User.async_create(user_id=user_id, username='user1)\n\n    # Model.objects.all() and Model.all() in async way:\n    print(list(await User.async_all()))\n    print(list(await User.objects.filter(user_id=user_id).async_all()))\n\n    # Model.object.update() in async way:\n    await User.objects(user_id=user_id).async_update(username='updated-user1')\n\n    # Model.objects.get() and Model.get() in async way:\n    user = await User.objects.async_get(user_id=user_id)\n    assert user.user_id == (await User.async_get(user_id=user_id)).user_id\n    print(user, user.username)\n\n    # obj.save() in async way:\n    user.username = 'saved-user1'\n    await user.async_save()\n\n    # obj.delete() in async way:\n    await user.async_delete()\n\n    # Didn't break original functions\n    print('Left users: ', len(User.objects.all()))\n\n\ndef create_keyspace(keyspace):\n    os.environ['CQLENG_ALLOW_SCHEMA_MANAGEMENT'] = 'true'\n    connection.register_connection('cqlengine', session=session, default=True)\n    management.create_keyspace_simple(keyspace, replication_factor=1)\n    management.sync_table(User, keyspaces=[keyspace])\n\n\ncreate_keyspace('example_keyspace')\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(main())\ncluster.shutdown()\nloop.close()\n\n```\n\n\n## License\nThis project is under MIT license.\n",
    'author': 'Darren',
    'author_email': 'charact3@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
