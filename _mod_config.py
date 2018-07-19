# _mod_config.py
# This module is responsible for sanity checking and displaying error and help
# messages.

import os
from sys import argv, modules, version as py_version

import _mod_prettyprint as prettyprint

pprint = prettyprint.pretty_print

# Dictionary of ID/message pairs
msg_list = {}


def sanity_check():
    ###########################################################################
    # Get variables from the main scope and check per-program configuration
    ###########################################################################
    main_vars = modules['__main__']

    # Check to see if the user ignored the warnings about using aging shit.
    try:
        py2_gtfo = main_vars['py2_gtfo']
    except KeyError:
        py2_gtfo = False

    # Is the tool redundant or useless on the average *nix?
    try:
        unix_check = main_vars['unix_check']
    except KeyError:
        unix_check = False

    ###########################################################################
    # Begin enforcing per-program config
    ###########################################################################
    if py2_gtfo and py_version.startswith('2'):
        print(msg_list['python2_msg'])
        exit()
    if unix_check and os.name == 'posix':
        print(msg_list['unix_os_msg'])
        exit()


def parse_messages(msg_loc):
    msg_file = open(msg_loc, 'r')
    msg_lines = msg_file.readlines()
    msg_file.close()

    cur_id = ''
    cur_msg = ''

    for line in msg_lines:
        if line.startswith('#'):
            continue
        elif line.startswith('$'):
            line = line.strip()
            line = line.strip('$')

            if line == 'end':
                msg_list[cur_id] = cur_msg
                cur_id = ''
                cur_msg = ''
            else:
                cur_id = line
        else:
            cur_msg += (line)


###############################################################################
# Run on import
###############################################################################
install_root = os.path.dirname(argv[0])
msg_location = os.path.join(install_root, 'messages.lst')

parse_messages(msg_location)
