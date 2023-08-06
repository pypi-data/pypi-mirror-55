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

meson_version: map = {
    'meson-50.0': ['0', '50', '0'],
    'meson-51.0': ['0', '51', '0'],
    'meson-52.0': ['0', '52', '0'],
}

MESON_BUILD_FILE = 'meson.build'


class MesonString(str):
    """Meson string type"""

    def type_id(self):
        return 'string'


class MesonCombo(str):
    """Meson combo type"""

    def type_id(self):
        return 'combo'


class MesonArray(str):
    """Meson array type"""

    def type_id(self):
        return 'array'


class MesonInteger(str):
    """Meson integer type"""

    def type_id(self):
        return 'integer'


class MesonBool(str):
    """Meson boolean type"""

    def type_id(self):
        return 'bool'

    def false(self):
        return 'false'

    def true(self):
        return 'true'
