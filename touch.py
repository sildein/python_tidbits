#!/usr/bin/env python
# touch.py
# Literally just creates empty files.

from sys import argv

import _mod_config as config
import _mod_prettyprint as prettyprint

pprint = prettyprint.pretty_print
color_string = prettyprint.color_string

###############################################################################
# Begin per-program config
###############################################################################
py2_gtfo = True
unix_check = True
###############################################################################
# End per-program config
###############################################################################

if __name__ == '__main__':
    config.sanity_check()

    if len(argv) == 1 or argv[1] == 'help':
        print(config.msg_list['touch_help'])
        exit()

    # Touch file
    file = open(argv[1], 'wb')
    file.close()
