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
from .cmesoninit import CMeson


def cmeson_main():
    cmeson = CMeson()
    cmeson.setup_ncurses()
# end of function mesonui_main

if __name__ == "__main__":
    cmeson_main()
