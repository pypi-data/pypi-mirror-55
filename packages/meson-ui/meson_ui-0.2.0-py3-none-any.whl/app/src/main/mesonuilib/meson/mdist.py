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
from ..interface.interfacemesoncmd import InterfaceMesonCommand


class MesonDist(InterfaceMesonCommand):
    def __init__(self, context):
        self._context = context
        super().__init__(context=self._context)

    def run(self):
        try:
            meson_args = ['dist', '-C', self._context.get_builddir(), '--formats', 'zip']
            process = self._run(cmd=meson_args)
        except Exception as e:
            print(f'Exception: {e}')
        return process
