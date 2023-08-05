# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['flirextractor']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17,<2.0', 'pillow>=6.2,<7.0', 'pyexiftool>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'flirextractor',
    'version': '0.1.0',
    'description': 'A library from extracting temperature values from FLIR IRT Images.',
    'long_description': '# flirextractor\n\nA library from extracting temperature values from FLIR IRT Images.\n\n## Differences from existing libraries\n\nThere is an existing Python package for extracting temperature\nvalues from raw IRT images, see\n[nationaldronesau/FlirImageExtractor](https://github.com/nationaldronesau/FlirImageExtractor).\nHowever, it has some issues that I didn\'t like:\n\n  - Most importantly, it is forked from the UNLICENSED\n    [Nervengift/read_thermal.py](https://github.com/Nervengift/read_thermal.py),\n    so until\n    [Nervengift/read_thermal.py#4](https://github.com/Nervengift/read_thermal.py/issues/4)\n    is answered, this package cannot be legally used.\n  - Secondly, it is quite inefficient, as it runs a new exiftool process\n    for each image, and it converts the temperature for each pixel, instead\n    of using numpy\'s vectorized math.\n\n## Installing\n\nYou can install flirextractor from pip.\n\n```bash\npip3 install flirextractor\n```\n\nMake sure you install exiftool as well.\n\nOn RHEL, this can be installed via:\n\n```bash\nsudo yum install perl-Image-ExifTool\n```\n\nOn debian, this can be installed via:\n\n```bash\nsudo apt update && sudo apt install libimage-exiftool-perl -y\n```\n\n## Usage\n\nData is loaded in Celcius as 2-dimensional\n[`numpy.ndarray`s](https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html).\n\nTo load data from a single FLIR file, run:\n\n```python3\nfrom flirextractor import FlirExtractor\nwith FlirExtractor() as extractor:\n    thermal_data = extractor.get_thermal("path/to/FLIRimage.jpg")\n```\n\nData can also be loaded from multiple FLIR files at once in batch mode,\nwhich is slightly more efficient:\n\n```python3\nfrom flirextractor import FlirExtractor\nwith FlirExtractor() as extractor:\n    list_of_thermal_data = extractor.get_thermal_batch(\n        ["path/to/FLIRimage.jpg", "path/to/another/FLIRimage.jpg"])\n```\n\n## Testing\n\nUse the Python package manager `poetry` to install test dependecies:\n\n```bash\npoetry install\n```\n\nThen run pytest to run tests.\n\n```bash\npoetry run pytest\n```\n\nRun mypy to run type tests:\n\n```bash\npoetry run mypy -p flirextractor\n```\n\nRun black to auto-format code:\n\n```bash\npoetry run black .\n```\n\nAnd run flake8 to test for anything black missed:\n\n```bash\npoetry run flake8 tests/ flirextractor/\n```\n',
    'author': 'Alois Klink',
    'author_email': 'alois.klink@gmail.com',
    'url': 'https://github.com/aloisklink/flirextractor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
