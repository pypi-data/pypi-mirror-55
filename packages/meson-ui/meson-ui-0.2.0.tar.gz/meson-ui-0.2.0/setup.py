#!/user/bin/env python3
###################################################################################
#                                                                                 #
# AUTHOR: Michael Brockus.                                                        #
#                                                                                 #
# CONTACT: <mailto:michaelbrockus@gmail.com>                                      #
#                                                                                 #
# LICENSE: Apache 2.0 :http://www.apache.org/licenses/LICENSE-2.0                 #
#                                                                                 #
###################################################################################
from setuptools import setup
from app.src.main.appinfo import MesonUiAppInfo as PyPiInfo
import sys

pypi_info = PyPiInfo()

pypi_info.required_version()

package_list = [
    'app',
    'app.src',
    'app.src.main',
    'app.src.main.controller',
    'app.src.main.model',
    'app.src.main.repo',
    'app.src.main.view',
    'app.src.main.ui',
    'app.src.main.mesonuilib',
    'app.src.main.mesonuilib.interface',
    'app.src.main.mesonuilib.component',
    'app.src.main.mesonuilib.backends',
    'app.src.main.mesonuilib.ninja',
    'app.src.main.mesonuilib.meson',
    'app.src.main.mesonuilib.utils',
]

data_files = []
if sys.platform != 'win32':
    # Only useful on UNIX-like systems
    data_files = [('share/man/man1', ['man/mesonui.1'])]

setup(
    name=pypi_info.get_name(),
    version=pypi_info.get_version(),
    description=pypi_info.get_description(),
    author=pypi_info.get_author(),
    author_email=pypi_info.get_gmail(),
    license=pypi_info.get_license(),
    zip_safe=True,
    include_package_data=True,
    packages=package_list,
    data_files=data_files,
    entry_points={
        'gui_scripts': ['meson-ui=app.__main__:mesonui_main'],
        # 'console_scripts': ['cmeson=app.__main__:cmeson_main']
    },
    install_requires=['PyQt5']
)
