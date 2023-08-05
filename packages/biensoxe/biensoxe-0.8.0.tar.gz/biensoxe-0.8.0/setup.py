# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['biensoxe']

package_data = \
{'': ['*']}

install_requires = \
['dedict>=1.0.7,<2.0.0', 'pydantic>=1.0,<2.0']

setup_kwargs = {
    'name': 'biensoxe',
    'version': '0.8.0',
    'description': 'Library to parse and validate Vietnamese vehicle plate',
    'long_description': "========\nBienSoXe\n========\n\nLibrary to parse and validate Vietnamese vehicle plate\n\nInstall\n-------\n\n.. code-block:: sh\n\n    pip3 install biensoxe\n\n\nUsage\n-----\n\n.. code-block:: python\n\n    >>> from biensoxe import VietnamVehiclePlate\n\n    >>> VietnamVehiclePlate.from_string('44A-112.23')\n    VietnamVehiclePlate(compact='44A11223', vehicle_type=<VehicleType.DOMESTIC_AUTOMOBILE: 1>,\n    series='A', order='11223', locality='44', dip_country=None)\n",
    'author': 'Nguyễn Hồng Quân',
    'author_email': 'ng.hong.quan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sunshine-tech/BienSoXe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
