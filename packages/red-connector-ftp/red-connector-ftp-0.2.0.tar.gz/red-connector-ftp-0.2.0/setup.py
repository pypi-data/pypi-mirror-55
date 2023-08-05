# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['red_connector_ftp',
 'red_connector_ftp.commons',
 'red_connector_ftp.ftp',
 'red_connector_ftp.ftp_archive']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.0,<4.0']

entry_points = \
{'console_scripts': ['red-connector-ftp = red_connector_ftp.ftp.main:main',
                     'red-connector-ftp-archive = '
                     'red_connector_ftp.ftp_archive.main:main']}

setup_kwargs = {
    'name': 'red-connector-ftp',
    'version': '0.2.0',
    'description': 'RED Connector FTP is part of the Curious Containers project.',
    'long_description': '# RED Connector FTP\n\nRED Connector SFTP is part of the Curious Containers project.\n\nFor more information please refer to the Curious Containers [documentation](https://www.curious-containers.cc/).\n\n## Acknowledgements\n\nThe Curious Containers software is developed at [CBMI](https://cbmi.htw-berlin.de/) (HTW Berlin - University of Applied Sciences). The work is supported by the German Federal Ministry of Economic Affairs and Energy (ZIM project BeCRF, grant number KF3470401BZ4), the German Federal Ministry of Education and Research (project deep.TEACHING, grant number 01IS17056 and project deep.HEALTH, grant number 13FH770IX6) and HTW Berlin Booster.\n\n',
    'author': 'Christoph Jansen',
    'author_email': 'Christoph.Jansen@htw-berlin.de',
    'url': 'https://www.curious-containers.cc/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
