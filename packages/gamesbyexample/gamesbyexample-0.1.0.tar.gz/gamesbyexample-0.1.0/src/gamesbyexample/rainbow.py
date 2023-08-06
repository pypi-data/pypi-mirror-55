# Rainbow, by Al Sweigart al@inventwithpython.com
# Shows a simple rainbow animation.

import time, sys

try:
    import bext
except ImportError:
    print("""This program requires the bext module, which you can install by
opening a Terminal window (on macOS & Linux) and running:

    python3 -m pip install --user bext

or a Command Prompt window (on Windows) and running:

    python -m pip install --user bext""")
    sys.exit()

indent = 0 # How many spaces to indent.
indentIncreasing = True # Whether the indentation is increasing or not.

while True:
    print(' ' * indent, end='')
    bext.fg('red')
    print('##', end='')
    bext.fg('yellow')
    print('##', end='')
    bext.fg('green')
    print('##', end='')
    bext.fg('blue')
    print('##', end='')
    bext.fg('cyan')
    print('##', end='')
    bext.fg('purple')
    print('##')

    if indentIncreasing:
        # Increase the number of spaces:
        indent = indent + 1
        if indent == 20:
            # Change direction:
            indentIncreasing = False
    else:
        # Decrease the number of spaces:
        indent = indent - 1
        if indent == 0:
            # Change direction:
            indentIncreasing = True

    time.sleep(0.05) # Add a slight pause.
