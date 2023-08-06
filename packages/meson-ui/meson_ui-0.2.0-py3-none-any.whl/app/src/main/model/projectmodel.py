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


class ProjectModel:
    '''
        This is a data class for Meson project
    '''

    def __init__(self, context=None):
        self._context = context
        self._sourcedir = self._context.get_sourcedir()
        self._scriptdir = self._context.get_scriptdir()
        self._builddir = self._context.get_builddir()

    def get_sourcedir(self) -> str:
        return self._sourcedir

    def get_builddir(self) -> str:
        return self._builddir

    def get_scriptdir(self) -> str:
        return self._scriptdir

    def set_sourcedir(self, value) -> None:
        self._sourcedir = value

    def set_builddir(self, value) -> None:
        self._builddir = value

    def set_scriptdir(self, value) -> None:
        self._scriptdir = value
