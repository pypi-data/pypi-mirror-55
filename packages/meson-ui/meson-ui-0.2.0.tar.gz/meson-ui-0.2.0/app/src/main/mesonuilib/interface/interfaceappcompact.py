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
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication


class InterfaceAppCompact(QMainWindow, QApplication):

    def error(self, message) -> None:
        return RuntimeError(f'Error: {message}')

    def message(self, message) -> None:
        print(f'Log: {message}')
