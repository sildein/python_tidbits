# _mod_prettyprint.py
# This module enables printing with ANSI codes in Unix shells (and in Cygwin)
# Has no local dependencies and can be used in every script and other module.
#
# Copy functions from this module into the current namespace as needed.

import os

# Foreground color codes
fg_codes = {
    'black': '\033[90m',
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'purple': '\033[95m',
    'cyan': '\033[96m',
    'white': '\033[97m',
    'reset': '\033[39m'
}

# Some duplicates of the above, named semantically
sem_codes = {
    'pass': '\033[92m',
    'warning': '\033[93m',
    'error': '\033[91m',
    'info': '\033[96m'
}

# Background color codes
bg_codes = {
    'black': '\033[40m',
    'red': '\033[41m',
    'green': '\033[42m',
    'yellow': '\033[43m',
    'blue': '\033[44m',
    'purple': '\033[45m',
    'cyan': '\033[46m',
    'white': '\033[47m',
}

# Formatting codes
fmt_codes = {
    'bold': '\033[1m',
    'italic': '\033[3m',
    'undl': '\033[4m',  # Underline
    'strk': '\033[9m',  # Strikethrough
}

rst_codes = {
    'bold_off': '\033[22m',
    'italic_off': '\033[23m',
    'undl_off': '\033[24m',
    'strk_off': '\033[29m',
    'fg': '\033[39m',
    'bg': '\033[49m',
    'all': '\033[0m'
}


# This function should be assigned to a variable in the current namespace to
# save keystrokes.
def pretty_print(msg, **kwargs):
    # This should accept all data types like the builtin function
    msg = str(msg)

    if os.name != 'posix':
        print(msg)
        return

    for k, v in kwargs.items():
        if k == 'fg':
            if v in sem_codes:
                msg = sem_codes[v] + msg + rst_codes['fg']
            else:
                msg = fg_codes[v] + msg + rst_codes['fg']
        elif k == 'bg':
            msg = bg_codes[v] + msg + rst_codes['bg']
        elif k == 'fmt':
            msg = fmt_codes[v] + msg + rst_codes[v + '_off']

    print(msg)


# This one can also be copied into the current namespace. It's more useful when
# only a partial string should be colored or formatted.
def color_string(msg, **kwargs):
    if os.name != 'posix':
        return msg

    for k, v in kwargs.items():
        if k == 'fg':
            if v in sem_codes:
                msg = sem_codes[v] + msg + rst_codes['fg']
            else:
                msg = fg_codes[v] + msg + rst_codes['fg']
        elif k == 'bg':
            msg = bg_codes[v] + msg + rst_codes['bg']
        elif k == 'fmt':
            msg = fmt_codes[v] + msg + rst_codes[v + '_off']

    return msg


###############################################################################
# Main method for module testing
###############################################################################
if __name__ == '__main__':
    print('\nTesting _mid_prettyprint.py\n')

    if os.name == 'nt':
        print('ANSI colors don\'t work in Windows shells')

    for i in fg_codes.keys():
        txt = 'Testing foreground color: ' + i + '.'
        pretty_print(txt, fg=i)

    for i in bg_codes.keys():
        txt = 'Testing background color: ' + i + '.'
        pretty_print(txt, bg=i)

    for i in fmt_codes.keys():
        txt = 'Testing format: ' + i + '.'
        pretty_print(txt, fmt=i)

    for i in sem_codes.keys():
        txt = 'This text should indicate a status of: ' + i + '.'
        pretty_print(txt, fg=i)

    txt = 'This text should be blue and underlined on a white background.'
    pretty_print(txt, fg='black', bg='white', fmt='undl')

    print('This text should be normal.')

    print('\nEnd tests for _mod_prettyprint.py\n')
