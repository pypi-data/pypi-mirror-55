# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hruid']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['hruid = hruid.cli:main', 'tests = scripts:run_tests']}

setup_kwargs = {
    'name': 'hruid',
    'version': '0.0.1',
    'description': 'Human Readable Unique Identifiers for Python',
    'long_description': '<p  align="center">\n  <strong>HRUID</strong>\n  <br>\n  <code>Human Readable Unique Identifier for Python</code>\n  <br><br>\n  <!-- <a href="https://badge.fury.io/py/conventional-commit"><img src="https://badge.fury.io/py/conventional-commit.svg" alt="PyPI version" height="18"></a>\n  <a href="https://travis-ci.org/nebbles/gitcommit/branches"><img src="https://travis-ci.org/nebbles/gitcommit.svg?branch=master" alt="Travis CI build" height="18"></a> -->\n</p>\n\n## Usage\n\nInstall\n```\n???\n```\n\nUse\n```python\nimport hruid\n\ngenerator = hruid.Generator()\nphrase = generator.random()\nprint(phrase)\n```\n\n## Overview\n\nThis Python package implements human readable ID generation based on the [Asanablog post by Greg\nSlovacek](https://blog.asana.com/2011/09/6-sad-squid-snuggle-softly/).\n\nIn it, he describes how a unique phrase can be generated in lieu of a confusing and complex\nalphanumeric ID.\n\n> Imagine representing 32 bits of information (numbers up to 4 billion) as a sentence instead of a jumble of digits. Each sentence can have the same predictable structure, and the number will be used to choose words from a dictionary to fill in that structure—like Mad Libs.\n> \n> One possible sentence structure can be: count + adjective + plural noun + verb + adverb, e.g. “6 sad squid snuggle softly.” We can divide the bit-space of the number like so:\n> \n> - 5 bits for the count (2-33, so it is always plural)  \n> - 7 bits for the adjective (one of 128 possibilities)  \n> - 7 bits for the plural noun (one of 128 possibilities, which we made all animals just for fun)  \n> - 7 bits for the verb (one of 128 possibilities)  \n> - 6 bits for the adverb (one of 64 possibilities)  \n>\n> Now, given a dictionary containing words categorized in this way, we can generate 4 billion unique (and sometimes very memorable) sentences. In Asana, the ID used to generate the error phrase is random, so the same sentence is unlikely to occur twice.\n\n## Develop\n\nInstall dependencies\n```\npoetry install\n```\n\nRun `example.py` which does some basic things with the package\n```\npoetry run python example.py\n```\n\nRun the package in CLI mode\n```\npoetry run python -m hruid\n```\n\nTo run tests\n```\npoetry run tests\n```\n\n## License\n\n[GNU GPLv3](./LICENSE)\n',
    'author': 'nebbles',
    'author_email': None,
    'url': 'https://github.com/nebbles/hruid-python',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
