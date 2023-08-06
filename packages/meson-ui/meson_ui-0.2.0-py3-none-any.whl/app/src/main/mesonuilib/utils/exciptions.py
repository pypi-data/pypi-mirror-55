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

class MesonCommandFailedException(Exception):
    """There was an ambiguous exeption do to a Meson command failed!"""

class NinjaCommandFailedException(Exception):
    """There was an ambiguous exeption do to a Ninja command failed!"""

class MesonUiException(Exception):
    """Meson-ui exception!"""

class CMesonException(Exception):
    """CMeson exception!"""

class MesonUiNotImplementedError(NotImplementedError):
    """Meson-ui exception do to class not implemented!"""

class CMesonNotImplementedError(NotImplementedError):
    """CMeson exception do to class not implemented!"""
