# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiger_coins']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3,<20.0', 'funcy>=1.13,<2.0', 'py-aiger-bv>=1.0.5,<2.0.0']

extras_require = \
{'bdd': ['py-aiger-bdd>=0.2.3,<0.3.0']}

setup_kwargs = {
    'name': 'py-aiger-coins',
    'version': '1.1.0',
    'description': 'Library for creating circuits that encode discrete distributions.',
    'long_description': '[![Build Status](https://travis-ci.org/mvcisback/py-aiger-coins.svg?branch=master)](https://travis-ci.org/mvcisback/py-aiger-coins)\n[![codecov](https://codecov.io/gh/mvcisback/py-aiger-coins/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/py-aiger-coins)\n[![Updates](https://pyup.io/repos/github/mvcisback/py-aiger-coins/shield.svg)](https://pyup.io/repos/github/mvcisback/py-aiger-coins/)\n\n[![PyPI version](https://badge.fury.io/py/py-aiger-coins.svg)](https://badge.fury.io/py/py-aiger-coins)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n\n# py-aiger-coins\nLibrary for creating circuits that encode discrete distributions. The\nname comes from the random bit model of drawing from discrete\ndistributions using coin flips.\n\n<!-- markdown-toc start - Don\'t edit this section. Run M-x markdown-toc-refresh-toc -->\n**Table of Contents**\n\n- [py-aiger-coins](#py-aiger-coins)\n- [Install](#install)\n- [Usage](#usage)\n    - [Biased Coins](#biased-coins)\n    - [Distributions on discrete sets](#distributions-on-discrete-sets)\n    - [Distributions and Coins](#distributions-and-coins)\n        - [Manipulating Distributions](#manipulating-distributions)\n    - [Binomial Distributions](#binomial-distributions)\n\n<!-- markdown-toc end -->\n\n\n# Install\n\nTo install this library run:\n\n`$ pip install py-aiger-coins`\n\nNote that to actually compute probabilities, one needs to install with the bdd option.\n\n`$ pip install py-aiger-coins[bdd]`\n\nFor developers, note that this project uses the\n[poetry](https://poetry.eustace.io/) python package/dependency\nmanagement tool. Please familarize yourself with it and then run:\n\n`$ poetry install`\n\n# Usage\n\nNote this tutorial assumes `py-aiger-bdd` has been installed (see the\nInstall section).\n\n## Biased Coins\n\nWe start by encoding a biased coin and computing its bias.\n\n```python\nfrom fractions import Fraction\n\nimport aiger_coins\n\nbias = Fraction(1, 3)\ncoin1 = aiger_coins.coin(bias)\ncoin2 = aiger_coins.coin((1, 3))  # or just use a tuple.\n\nassert coin1.prob() == coin2.prob() == prob\n```\n\n## Distributions on discrete sets\n\nWe now illustrate how to create a set of mutually exclusive coins that\nrepresent distribution over a finite set. For example, a biased three\nsided dice can be 1-hot encoded with:\n\n```python\ndice = aiger_coins.dist([(1, 6), (3, 6), (2, 6)])\n\nprint(dice.freqs())\n# (Fraction(1, 6), Fraction(1, 2), Fraction(1, 3))\n```\n\nLetting, `⚀ = dice[0]`, `⚁ = dice[1]`, `⚂ = dice[2]`, \n```python\none, two, three = dice[0], dice[1], dice[2]\n```\n\nWe can ask the probability of drawing an element of `{⚀, ⚁}` with:\n\n```python\nassert (one | two).prob() == Fraction(2, 3)\nassert (~three).prob() == Fraction(2, 3)\n```\n\n## Distributions and Coins\n\n`Distribution`s and `Coin`s are really just wrappers around two\n`aiger_bv.UnsignedBVExpr` objects stored in the `expr` and `valid`\nattributes.\n\nThe attributes `expr` and `valid` encode an expression over fair coin\nflips and which coin flips are "valid" respectively. Coins is a\nspecial type of `Distribution` where the expression is a predicate\n(e.g. has one output).\n\nNote that accessing the ith element of a `Distribution` results in a\n`Coin` encoding the probability of drawing that element.\n\n### Manipulating Distributions\n\nIn general `Distribution`s can me manipulated by manipulating the\n`.expr` attribution to reinterpret the coin flips or manipulating\n`.valid` to condition on different coin flip outcomes.\n\nOut of the box `Distribution`s support a small number of operations:\n`+, <, <=, >=, >, ==, !=, ~, |, &, ^, .concat`, which they inherit\nfrom `aiger_bv.UnsignedBVExpr`. When using the same `.valid` predicate\n(same coin flips), these operations only manipulate the `.expr`\nattribute.\n\nMore generally, one can use the `apply` method to apply an arbitrary\nfunction to the `.expr` attribute. For example, using the dice from\nbefore:\n\n```python\ndice2 = dice.apply(lambda expr: ~expr[2])\nassert dice2[0].freqs() == Fraction(2, 3)\n```\n\nOne can also change the assumptions made on the coin flips by using\nthe condition method, for example, suppose we condition on the coin\nflips never being all `False`. This changes the distribution\nas follows:\n\n```python\ncoins = dice.coins  #  Bitvector Expression of coin variables.\ndice3 = dice.condition(coins != 0)\n\nprint(dice3.freqs())\n# [Fraction(0, 5), Fraction(3, 5), Fraction(2, 5)]\n```\n\n## Binomial Distributions\n\nAs a convenience, `py-aiger-coins` also supports encoding Binomial\ndistributions.\n\n```python\nx = binomial(3)\n\nprint(x.freqs())\n# (Fraction(1, 8), Fraction(3, 8), Fraction(3, 8), Fraction(1, 8))\n```\n',
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'url': 'https://github.com/mvcisback/py-aiger-coins',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
