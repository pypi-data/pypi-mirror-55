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
from ..meson.mesonmanager import Meson


class InterfaceMesonUiBacken:
    def __init__(self, meson: Meson):
        self._meson = meson

    def as_ninja(self):
        return 'ninja'

    def generate_project(self):
        pass

    def generate_file_map(self):
        pass

    def generate_build_map(self):
        pass

    def compile_command(self):
        pass

    def build_command(self):
        pass

    def clean_command(self):
        pass

    def test_command(self):
        pass

    def dist_command(self):
        pass

    def project_recipe(self):
        pass
