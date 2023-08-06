# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['csvprint']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['poetry = bin.csvprint:main']}

setup_kwargs = {
    'name': 'csvprint',
    'version': '0.7.0',
    'description': 'Print csv files in columnated format, either plain or as a Markdown or LaTeX table',
    'long_description': "# `csvprint`\n\n[![Build Status](https://travis-ci.org/vegarsti/csvprint.svg?branch=master)](https://travis-ci.org/travis-ci/travis-web)\n[![codecov](https://codecov.io/gh/vegarsti/csvprint/branch/master/graph/badge.svg)](https://codecov.io/gh/vegarsti/csvprint)\n\nA command-line utility for pretty printing csv files and converting to other formats.\n\n## Installation\n\nIf Python 3 with the package manager pip is installed, doing `pip3 install csvprint` in your terminal should do the trick.\n\n## Development installation\n\nWith [pipenv](https://github.com/pypa/pipenv) installed.\n\n1. Clone this repo\n2. Do `pipenv install`\n3. `pipenv shell`\n4. `pip install -e .`\n\n## Usage\n\n`csvprint [filename]` prints a formatted table if `filename` is a comma separated file.\n\n```\n» cat imdb.csv\nTitle,Release Year,Estimated Budget\nShawshank Redemption,1994,$25 000 000\nThe Godfather,1972,$6 000 000\nThe Godfather: Part II,1974,$13 000 000\nThe Dark Knight,2008,$185 000 000\n12 Angry Men,1957,$350 000\n\n» csvprint imdb.csv\nTitle                  Release Year Estimated Budget\nShawshank Redemption   1994         $25 000 000\nThe Godfather          1972         $6 000 000\nThe Godfather: Part II 1974         $13 000 000\nThe Dark Knight        2008         $185 000 000\n12 Angry Men           1957         $350 000\n```\nYou can also pipe into `csvprint`:\n\n```\n» cat imdb.csv | csvprint\nTitle                  Release Year Estimated Budget\nShawshank Redemption   1994         $25 000 000\nThe Godfather          1972         $6 000 000\nThe Godfather: Part II 1974         $13 000 000\nThe Dark Knight        2008         $185 000 000\n12 Angry Men           1957         $350 000\n```\n\n## Options\n\nCommand        | Result\n:--------------|:-------------------------------------------------------------\n`-a`           | specify alignment (left or right) - see examples below\n`-c`           | specify which columns to print \n`-h`           | print help message\n`--markdown`   | print as markdown\n`--latex`      | print as latex table\n`--numeric [c1:d1] [c2:d2] ...`   | specify decimal numbers for chosen numeric columns (`c` for column, `d` for digits)\n`--header`     | add header decoration around the first line\n`-s 'char'`    | file is delimited by `char` (instead of comma), `tab` for tab\n`-p [n]`       | add a padding of `n` spaces for each column, on both sides\n`-d [string]`  | specify the string to separate columns\n\n## Alignment example\n\nThere are three options for specifying alignment. One can use `l` or `r` for aligning all cells to the left or right, respectively. One can also specify a distinct alignment option for each column. Then the number of options will need to match the number of columns.\n\n```\n» csvprint imdb.csv -a l r r\nTitle                  Release Year Estimated Budget\nShawshank Redemption           1994      $25 000 000\nThe Godfather                  1972       $6 000 000\nThe Godfather: Part II         1974      $13 000 000\nThe Dark Knight                2008     $185 000 000\n12 Angry Men                   1957         $350 000\n```\n\n## Markdown example\n\nMarkdown output also supports left and right alignment.\n\n```\n» csvprint examples/imdb.csv --markdown -a l r r\nTitle                  | Release Year | Estimated Budget\n:----------------------|-------------:|----------------:\nShawshank Redemption   |         1994 |      $25 000 000\nThe Godfather          |         1972 |       $6 000 000\nThe Godfather: Part II |         1974 |      $13 000 000\nThe Dark Knight        |         2008 |     $185 000 000\n12 Angry Men           |         1957 |         $350 000\n```\n\nWhen rendered as HTML, this looks like\n\nTitle                  | Release Year | Estimated Budget\n:----------------------|-------------:|----------------:\nShawshank Redemption   |         1994 |      $25 000 000\nThe Godfather          |         1972 |       $6 000 000\nThe Godfather: Part II |         1974 |      $13 000 000\nThe Dark Knight        |         2008 |     $185 000 000\n12 Angry Men           |         1957 |         $350 000\n\n## Numeric example\n\n```\n» csvprint examples/numeric.csv\nmeasure1  measure2\n1.2323    9000\n1.299     9000001\n\n» csvprint examples/numeric.csv --numeric 1:1 2:1\nmeasure1  measure2\n1.2       9000.0\n1.3       9000001.0\n```\n\n## Testing\n\nRun `pytest` while in the root directory of this repository.\n",
    'author': 'Vegard Stikbakke',
    'author_email': 'vegard.stikbakke@gmail.com',
    'url': 'https://github.com/vegarsti/csvprint',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
