# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dbvirus_searcher']

package_data = \
{'': ['*']}

install_requires = \
['biopython>=1.74,<2.0',
 'dbvirus-cacher>=0.0.2,<0.0.3',
 'fire>=0.2.1,<0.3.0',
 'pytz>=2019.2,<2020.0',
 'tqdm>=4.36,<5.0',
 'xmltodict>=0.12,<0.13']

setup_kwargs = {
    'name': 'dbvirus-searcher',
    'version': '0.1.1',
    'description': 'SRA data searcher w/ local caching for the DBVirus project',
    'long_description': '# DBVirus - Searcher\n\nSearcher is a CLI tool that provides a locally cached search for NCBI data,\nmainly focused on the SRA dataset.\n\n## Usage\n\nYou can find this project on [Docker Hub](https://hub.docker.com/r/fbidu/dbvirus-searcher)\n\n```\ndocker pull fbidu/dbvirus-searcher\n```\n',
    'author': 'Felipe Rodrigues',
    'author_email': 'felipe@felipevr.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
