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
    'version': '0.2.4',
    'description': 'OpenFEC API Client',
    'long_description': '# PyOpenFec\nA Python wrapper for the OpenFEC API. Documentation for this API can be found [here](https://api.open.fec.gov/developers)\n\n## Installation\n```\npip install pyopenfec\n```\n\n## Examples\n\n### Candidates\n\n#### Candidate\nThe `Candidate` class holds fields for each candidate in the OpenFEC API.\n\nA number of class and instance methods are available.\n\n##### count\nThe `Candidate.count()` method will return the number of Candidate objects available for a given query. Note: This method returns an integer representing the number of items available in the OpenFEC API. It does not return a list of objects.\n```\nfrom pyopenfec import Candidate\ncandidate_count = Candidate.count(cycle=2016, office="P", candidate_status="C")\n```\n\n#### fetch\nThe `Candidate.fetch()` method will return a list of Candidate objects available for a given query. This method will automatically page through the results and return all objects available in the OpenFEC API.\n```\nfrom pyopenfec import Candidate\ncandidate_count = Candidate.count(cycle=2016, office="P", candidate_status="C")\ncandidates = Candidate.fetch(cycle=2016, office="P", candidate_status="C")\nfor candidate in candidates:\n    print("{name}, {party}".format(name=candidate.name, party=candidate.party))\n```\n### Committees\ntktk\n\n### Reports\ntktk\n',
    'author': 'Jeremy Bowers',
    'author_email': 'jeremyjbowers@gmail.com',
    'url': 'https://github.com/jeremyjbowers/pyopenfec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
