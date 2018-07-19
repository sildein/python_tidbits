#!/usr/bin/env python
# archive_all.py
# Creates individual 7z archives for directories and files within the PWD.
# Obviously requires the console version of 7zip to be present.

import os
import shutil
from sys import argv
from subprocess import Popen, PIPE

import _mod_config as config
import _mod_prettyprint as prettyprint

pprint = prettyprint.pretty_print
color_string = prettyprint.color_string

###############################################################################
# Begin per-program config
###############################################################################
py2_gtfo = True
unix_check = False
###############################################################################
# End per-program config
###############################################################################

input_dir = '.'
output_dir = '.'
verbose = False
trash_dir = 'Trash'
use_trash = True


def mkarchive(file):
    archive_cmd = ['7z', 'a']
    archive_name = file + '.7z'
    input_file_path = os.path.join(input_dir, file)
    output_file_path = os.path.join(output_dir, archive_name)

    archive_cmd.append(output_file_path)
    archive_cmd.append(input_file_path)

    archive_process = Popen(archive_cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = archive_process.communicate()

    file_fmt = color_string(file, fg='blue', fmt='bold')
    archive_fmt = color_string(archive_name, fg='purple', fmt='bold')
    txt = '{0} -> {1}'.format(file_fmt, archive_fmt)
    print(txt)

    archive_process.wait()
    txt = 'Archive ' + archive_name + ' done.'
    pprint(txt, fg='info')

    if use_trash:
        shutil.move(input_file_path, 'Trash')


if __name__ == '__main__':
    config.sanity_check()

    if len(argv) == 2 and argv[1] == 'help':
        print(config.msg_list['archive_all_help'])
        exit()

    use_blist = False
    use_wlist = False
    list_file = None
    usr_list = []
    filenames = []

    # Parse arguments
    for i in argv[1:]:
        if i.startswith('id'):
            input_dir = os.path.abspath(i.split('=')[1])
        elif i.startswith('od'):
            output_dir = os.path.abspath(i.split('=')[1])
        elif i.startswith('wlist'):
            use_wlist = True
            list_file = i.split('=')[1]
        elif i.startswith('blist'):
            use_blist = True
            list_file = i.split('=')[1]
        elif i == 'verbose' or i == 'v':
            verbose = True

    # Blacklists and whitelists can't be used together
    if use_blist and use_wlist:
        pprint(config.msg_list['archive_all_list_error'], fg='error')
        exit()

    if verbose:
        indir_fmt = color_string(input_dir, fg='info', fmt='bold')
        outdir_fmt = color_string(output_dir, fg='info', fmt='bold')
        print('Input dir:', indir_fmt)
        print('Output dir:', outdir_fmt)

    # Read list file (if any)
    if list_file is not None:
        if verbose:
            pprint('Using list file: ' + list_file, fg='info')
        lst = open(list_file, 'r')
        for i in lst.readlines():
            i = i.strip()
            usr_list.append(i)
            if verbose:
                i_fmt = color_string(i, fg='info', fmt='bold')
                print('List has entry for', i_fmt)
        lst.close()

    # Check for necessity and existence of Trash folder
    if input_dir == output_dir:
        trash_dir = os.path.abspath(os.curdir)
        trash_dir = os.path.join(trash_dir, 'Trash')
        if not os.path.isdir(trash_dir):
            os.mkdir(trash_dir)
    else:
        use_trash = False

    # Get list of applicable file and directory names
    for i in os.listdir(input_dir):
        if (use_blist and i in usr_list) or (use_wlist and i not in usr_list):
            if verbose and use_blist:
                pprint('Blacklist blocked entry for ' + i, fg='warning')
            elif verbose and use_wlist:
                pprint('Whitelist blocked entry for ' + i, fg='warning')
            continue
        elif i != 'Trash' and not i.endswith('.7z'):
            if verbose:
                filenames.append(i)

    for i in filenames:
        mkarchive(i)
