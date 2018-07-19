#!/usr/bin/env python
# tree.py
# Prints files discovered while drilling through the folder hierarchy of a
# given root.

import os
from sys import argv

import _mod_config as config
import _mod_prettyprint as prettyprint
import _mod_tree as tree

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
    if len(argv) == 1 or argv[1] == 'help':
        print(config.msg_list['tree_help'])
        exit()

    # Parse arguments
    if argv[1] != os.curdir and argv[1] != os.pardir:
        use_abs = True
    else:
        use_abs = False

    files = tree.crawl(argv[1], use_abs)
