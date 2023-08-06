# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['axgridcommons']

package_data = \
{'': ['*']}

install_requires = \
['asq>=1.3,<2.0', 'pytoml>=0.1.21,<0.2.0', 'pyyaml>=5.1,<6.0']

setup_kwargs = {
    'name': 'axgridcommons',
    'version': '0.1.2',
    'description': 'AxGrid commons',
    'long_description': 'AxGrid Commons\n==============\n\nAbstract path\n-------------\n\n```python\np = Path(ct_root="/ctx/", fs_root="/tmp/fs/ctx/")\np.item(ct_target="/tk/a.txt").fs\n# "/tmp/fs/tk/a.txt"\n``` \n\n',
    'author': 'Dmitry Vysochin',
    'author_email': 'dmitry.vysochin@gmail.com',
    'url': 'http://axgrid.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
