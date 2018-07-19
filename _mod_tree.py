# _mod_tree.py
# Module for crawling directory trees, since os.walk() is retarded and
# pajeet-tier.

import os
from sys import argv

import _mod_prettyprint as prettyprint

pprint = prettyprint.pretty_print


# Recursive function that crawls a given directory tree and returns files in a
# list object. Returns names with absolute paths by default.
def crawl(root, abspath, echo=False):
    # Transparently use the absolute path for most operations
    root = os.path.abspath(root)

    ls = os.listdir(root)
    files = []
    folders = []

    # Separate files and folders
    for i in ls:
        i = os.path.join(root, i)

        if os.path.isdir(i):
            folders.append(i)
        elif os.path.isfile(i):
            files.append(i)

    # Recurse into subdirectories and append discovered files
    for i in folders:
        new_root = os.path.join(root, i)
        new_files = crawl(new_root, abspath, echo=echo)
        for j in new_files:
            if abspath:
                if echo:
                    pprint(j, fg='info')
                files.append(j)
            else:
                if echo:
                    j = os.path.relpath(j)
                pprint(j, fg='info')
                files.append(j)

    return files

# There is no '__main__' code for testing since tree.py basically piggybacks
# entirely on this module
