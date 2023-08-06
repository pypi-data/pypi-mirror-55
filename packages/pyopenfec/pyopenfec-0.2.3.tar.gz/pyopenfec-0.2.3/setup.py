# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pyopenfec']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2019.3,<2020.0', 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'pyopenfec',
    'version': '0.2.3',
    'description': 'OpenFEC API Client',
    'long_description': '# PyOpenFec\nA Python wrapper for the OpenFEC API. Documentation for this API can be found [here](https://api.open.fec.gov/developers)\n\n## Installation\n\n 1. Clone this repository\n```\ngit clone https://github.com/jeremyjbowers/pyopenfec.git\n```\n   \n 2. navigate into the new directory\n```\ncd pyopenfec\n```\n\n 3. (optional) start the virtual environment you\'d like to install to\n\n 4. run\n```\npython setup.py install\n```\n\n_Dependencies include [six](https://pypi.python.org/pypi/six) and [requests](https://pypi.python.org/pypi/requests) (will be installed by `setup.py`)_\n\n## Examples\n\n### Candidates\n\n#### Candidate\nThe `Candidate` class holds fields for each candidate in the OpenFEC API.\n\nA number of class and instance methods are available.\n\n##### count\nThe `Candidate.count()` method will return the number of Candidate objects available for a given query. Note: This method returns an integer representing the number of items available in the OpenFEC API. It does not return a list of objects.\n```\nfrom pyopenfec import Candidate\ncandidate_count = Candidate.count(cycle=2016, office="P", candidate_status="C")\n```\n\n#### fetch\nThe `Candidate.fetch()` method will return a list of Candidate objects available for a given query. This method will automatically page through the results and return all objects available in the OpenFEC API.\n```\nfrom pyopenfec import Candidate\ncandidate_count = Candidate.count(cycle=2016, office="P", candidate_status="C")\ncandidates = Candidate.fetch(cycle=2016, office="P", candidate_status="C")\nfor candidate in candidates:\n    print("{name}, {party}".format(name=candidate.name, party=candidate.party))\n```\n### Committees\ntktk\n\n### Reports\ntktk\n',
    'author': 'Robert Townley',
    'author_email': 'me@roberttownley.com',
    'url': 'https://github.com/roberttownley/pyopenfec/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
