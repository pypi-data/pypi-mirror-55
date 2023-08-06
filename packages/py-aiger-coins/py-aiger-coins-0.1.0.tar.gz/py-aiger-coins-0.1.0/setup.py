# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiger_coins']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3,<20.0', 'funcy>=1.13,<2.0', 'py-aiger-bv>=1.0.5,<2.0.0']

setup_kwargs = {
    'name': 'py-aiger-coins',
    'version': '0.1.0',
    'description': 'Library for creating circuits that encode discrete distributions.',
    'long_description': "[![Build Status](https://travis-ci.org/mvcisback/py-aiger-coins.svg?branch=master)](https://travis-ci.org/mvcisback/py-aiger-coins)\n[![codecov](https://codecov.io/gh/mvcisback/py-aiger-coins/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/py-aiger-coins)\n[![Updates](https://pyup.io/repos/github/mvcisback/py-aiger-coins/shield.svg)](https://pyup.io/repos/github/mvcisback/py-aiger-coins/)\n\n[![PyPI version](https://badge.fury.io/py/py-aiger-coins.svg)](https://badge.fury.io/py/py-aiger-coins)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n\n# py-aiger-coins\nLibrary for creating circuits that encode discrete distributions. The\nname comes from the random bit model of drawing from discrete\ndistributions using coin flips.\n\n# Install\n\nTo install this library run:\n\n`$ pip install py-aiger-coins`\n\n# Usage\n\nThis tutorial assumes familiarity with\n[py-aiger](https://github.com/mvcisback/py-aiger) and\n[py-aiger-bdd](https://github.com/mvcisback/py-aiger-bdd).  `py-aiger`\nshould automatically be installed with `py-aiger-coins` and\n`py-aiger-bdd` can be installed via:\n\n`$ pip install py-aiger-bdd`\n\n## Biased Coins\n\nWe start by encoding a biased coin and computing its\nbias. The coin will be encoded as two circuits\n`top` and `bot` such that `bias = #top / #bot`, where `#`\nindicates model counting.\n```python\nfrom fractions import Fraction\n\nimport aiger\nimport aiger_coins\nfrom aiger_bdd import count\n\nprob = Fraction(1, 3)\ntop, bot = aiger_coins.coin(prob)\ntop, bot = aiger_coins.coin((1, 3))  # or just use a tuple.\n\nassert Fraction(count(top), count(bot)) == prob\n```\n\n## Distributions on discrete sets\n\nWe now illustrate how to create a set of mutually exclusive coins\nthat represent distribution over a finite set. Namely, coordinate\n`i` is `1` iff the `i`th element of the set is drawn. For\nexample, a three sided dice can be encoded with:\n\n```python\ncirc, bot = aiger_coins.mutex_coins(\n    {'x': (1, 6), 'y': (3, 6), 'z': (2, 6)}\n)\n```\n\nNow to ask what the probability of drawing `x` or `y` is,\none can simply feed it into a circuit that performs that test!\n\n```python\ntest = aiger.or_gate(['x', 'y']) | aiger.sink(['z'])\nassert Fraction(count(circ >> test), count(bot)) == Fraction(2, 3)\n```\n\n## Binomial Distributions\n\n`py-aiger-coins` also supports encoding Binomial distributions. There are two options for encoding, 1-hot encoding which is a format similar to that in the discrete sets section and as an unsigned integers. The following snippet shows how the counts correspond to entries in Pascal's triangle.\n\n```python\nx = binomial(6, use_1hot=False)\ny = binomial(6, use_1hot=True)\nfor i, v in enumerate([1, 6, 15, 20, 15, 6, 1]):\n    assert v == count(x == i)\n    assert v == count(y == (1 << i))\n```\n\nDividing by `2**n` (64 in the example above) results in the probabilities of a Bionomial Distribution.\n",
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'url': 'https://github.com/mvcisback/py-aiger-coins',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
