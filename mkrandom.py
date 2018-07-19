#!/usr/bin/env python
# mkrandom.py
# Writes files of a given size with junk data.

import os
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

# Default to writing 1MB files
DEFAULT_SIZE = 1048576

verbose = True
quiet = False


def write_random_files(filename, size, num_files):
    for i in range(num_files):
        random_data = os.urandom(size)

        if num_files > 1:
            fname = filename + '.' + str(i)
        else:
            fname = filename

        if not quiet:
            pprint('Writing file: ' + fname, fg='info')

        file = open(fname, 'wb')
        file.write(random_data)
        file.close()


if __name__ == '__main__':
    config.sanity_check()

    if len(argv) == 1 or argv[1] == 'help':
        print(config.msg_list['mkrandom_help'])
        exit()

    size = DEFAULT_SIZE
    iterations = 1

    # Parse arguments
    for i in argv[2:]:
        if i.startswith('size='):
            size = int(i.replace('size=', ''))
        elif i.startswith('iter='):
            iterations = int(i.replace('iter=', ''))
        elif i == 'quiet':
            quiet = True
        elif i == 'verbose' or i == 'v':
            verbose = True

    write_random_files(argv[1], size, iterations)
