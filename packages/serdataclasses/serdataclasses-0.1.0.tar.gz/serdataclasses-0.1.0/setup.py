# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['serdataclasses']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'serdataclasses',
    'version': '0.1.0',
    'description': 'Serialize/deserialize Python objects from/to dataclasses',
    'long_description': "# serdataclasses\n\n*Warning: vaporware, subject to change at any time, for any reason, in any way.*\n\nThis library has two goals:\n\n1. Deserialize JSON into python dataclasses\n2. Serialize Python data classes into JSON\n\nIt has no external dependencies. Python 3.8+.\n\n## Notes\n\n* Recursive types aren't currently supported by mypy. I have them anyway because recursive types will allegedly be supported soon. That said, the type checker isn't super happy with me at the moment.\n* Edge cases haven't been considered. This library is a learning project, for now.\n* Inspired by [undictify](https://github.com/Dobiasd/undictify), but special-cased to dataclasses and more-focused on serde instead of general function signature overrides.\n\n## Written by\n\n* Samuel Roeca\n",
    'author': 'Sam Roeca',
    'author_email': 'samuel.roeca@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
