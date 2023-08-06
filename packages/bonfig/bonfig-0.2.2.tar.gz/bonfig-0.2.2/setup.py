# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['bonfig']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'bonfig',
    'version': '0.2.2',
    'description': "Don't write configurations, write class declarations.",
    'long_description': '# Bonfig\n\n    >>> import os, json, configparser\n    >>> from bonfig import Bonfig, Store\n    >>>\n    >>> class Config(Bonfig):\n    ...     with Store() as basic:\n    ...         VERSION = basic.Field(\'0.2\')\n    ...\n    ...     with Store() as secrets:\n    ...         CREDENTIALS = secrets.Field(default="XXXXXX-XX")\n    ...         PIN = secrets.IntField(default=1234)\n    ...\n    ...     with Store() as data:\n    ...         SAMPLE = data.Field()\n    ...         AVERAGE = data.FloatField()\n    ...\n    ...     with Store() as prefs:\n    ...         with prefs.Section(\'LINES\') as lines:\n    ...             X_MARKER = lines.Field()\n    ...             SHOW = lines.BoolField()\n    ...\n    ...         with prefs.Section(\'META\') as meta:\n    ...             DATE = meta.DatetimeField(name=\'start\', fmt=\'%d/%m/%y\')\n    ...\n    ...     def load(self, fn):\n    ...         self.basic = {}\n    ...         self.secrets = dict(os.environ)\n    ...\n    ...         with open(f"examples/{fn}.json") as f:\n    ...             self.data = json.load(f)\n    ...\n    ...         with open(f"examples/{fn}.ini") as f:\n    ...             self.prefs = configparser.ConfigParser()\n    ...             self.prefs.read_file(f)\n    ...\n    >>> c = Config("bonfig")\n    >>> c.VERSION\n    \'0.2\'\n    >>> c.CREDENTIALS\n    "XXXXXX-XX"\n    >>> c.AVERAGE\n    3.14159\n    >>> c.SHOW\n    True\n    >>> c.DATE\n    datetime.datetime(1982, 11, 18, 0, 0)\n    >>> c = Config(frozen=False)  # create a mutable version\n    >>> c.AVERAGE = 365.2\n    >>> c.AVERAGE\n    365.2\n\n\nStop writing your configurations as dictionaries and strange floating dataclasses, make them `Bonfigs` and make use of\na whole bunch of great features:\n\n* Declare your configurations as easy to read classes.\n* Pull in values from various sources into one neatly packaged class.\n* Get all the power that comes with classes built into your configurations - polymorphism, custom methods and custom initialisation.\n* Sleep safe in the knowledge your config won\'t change unexpectedly with configuration with `Bonfig.freeze`.\n* Ready made serialisation and deserialisation with custom `Fields` - `IntField`, `FloatField`, `BoolField` and `DatetimeField`, with [tools to help you easily define your own](https://0hughman0.github.io/bonfig/api.html#bonfig.fields.FieldDict.add).\n\n## Installation\n\n    pip install bonfig\n\nPlease checkout the project docs for more information: https://0hughman0.github.io/bonfig/index.html\n\n',
    'author': '0Hughman0',
    'author_email': 'rammers2@hotmail.co.uk',
    'url': 'https://github.com/0Hughman0/bonfig',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
