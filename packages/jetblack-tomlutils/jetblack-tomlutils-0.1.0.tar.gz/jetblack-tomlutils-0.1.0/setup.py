# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['jetblack_tomlutils']

package_data = \
{'': ['*']}

install_requires = \
['qtoml>=0.2.4,<0.3.0']

entry_points = \
{'console_scripts': ['json2toml = jetblack_tomlutils.toml_json:json2toml',
                     'toml2json = jetblack_tomlutils.toml_json:toml2json']}

setup_kwargs = {
    'name': 'jetblack-tomlutils',
    'version': '0.1.0',
    'description': 'Utilities for working with toml files',
    'long_description': '# bhdg-toml\n\nSome utilities for working with toml files.\n\n## Usage\n\nTo convert toml to json:\n\n```bash\n$ toml2json < pyproject.toml > pyproject.json\n$ toml2json pyproject.toml > pyproject.json\n$ toml2json pyproject.toml - > pyproject.json\n$ toml2json pyproject.toml pyproject.json\n$ cat pyproject.toml | toml2json\n$ cat pyproject.toml | toml2json -\n```\nTo convert json to toml:\n\n```bash\n$ json2toml < pyproject.json\n$ json2toml pyproject.json\n$ cat pyproject.toml | json2toml\n$ cat pyproject.toml | json2toml -\n```',
    'author': 'Rob Blackbourn',
    'author_email': 'rblackbourn@gmail.com',
    'url': 'https://github.com/rob-blackbourn/jetblack-tomlutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
