"""
MIT License

Copyright (c) 2017 Jared Thibault

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


Title: Todofinder

Author: Jared Thibault
Date: 27 February 2017

Program description:
    This finds all the different TODO's in a file and outputs them to stdout.
    It recurses into all folders if recursive option is specified.
    If there is a file named 'TODO.txt', then it will output that file's contents as well.

Operation:
    Put HTML-like TODO flags around code, bullet points, etc.

    Example:
    <TODO>
    [...]
    </TODO>
    or
    <TODO>[...]</TODO>
"""

"""
<TODO>
figure this out:
    import argparse

    parse = argparse.ArgumentParser(description='Finds all TODO\'s in
            a folder and outputs them to stdout')
    parse.add_argument('')
</TODO>
"""

# Defines:
START_TODO_DELIM = '<TODO>'
STOP_TODO_DELIM = '</TODO>'
SPACE_TAB = '    '
INDENT_1 = '    '
INDENT_2 = '      '

# Methods:
def todofinder(filename):
    """
    Finds and displays TODOs in a file

    Params:
        filename -> The file to find TODOs

    Returns:
        None
    """

    # with keyword handles opening and closing file
    print(filename)
    with open(filename, 'r') as file:
        text = file.read()

    # Gives error
    if text.count(START_TODO_DELIM) != text.count(STOP_TODO_DELIM):
        print(INDENT_1 + '!!! ERROR !!! TODO flags do not match!')
        print()
        return

    # Convert all tabs to spaces
    text = text.expandtabs(tabsize=len(SPACE_TAB))

    # Counts line numbers and finds out how many
    # columns the line number takes up
    line_num = 1
    for line in text.splitlines():
        line_num += 1
    cols = len(str(line_num))

    # Goes line-by-line and sees if there are
    # any TODOs in that line
    line_num = 1
    todo_num = 0
    in_todo = False
    for line in text.splitlines():
        # Inline TODO
        if START_TODO_DELIM in line and STOP_TODO_DELIM in line:
            todo_num += 1

            start = line.find(START_TODO_DELIM) + len(START_TODO_DELIM)
            stop = line.find(STOP_TODO_DELIM)

            print(INDENT_1 + 'TODO{0}'.format(todo_num))
            print_line_nums(cols, line_num)
            print(line[start:stop])
            print(INDENT_1 + 'END{0}'.format(todo_num))
            print()

        # Non-inline TODO
        elif START_TODO_DELIM in line:
            todo_num += 1
            in_todo = True

            # All other line tabs are compared to this TODO flag tab.
            # This is so that the relative position of lines is kept.
            # If the TODO flag is in a weird spot (e.g. not after a tab),
            # then the subsequent code won't be indented right.
            initial_tabs = count_tabs(line)

            start = line.find(START_TODO_DELIM) + len(START_TODO_DELIM)
            stop = len(line)

            print(INDENT_1 + 'TODO{0}'.format(todo_num))
            # True if there is text after the TODO flag
            if start != stop:
                print_line_nums(cols, line_num)
                print(line[start:stop])

        elif STOP_TODO_DELIM in line:
            in_todo = False
            line_tabs = count_tabs(line)

            start = find_start(initial_tabs, line_tabs)
            stop = line.find(STOP_TODO_DELIM)

            # True if there is text before the end-TODO flag
            if start != stop:
                print_line_nums(cols, line_num)
                print(line[start:stop])
            print(INDENT_1 + 'END{0}'.format(todo_num))
            print()

        else:
            # Works same as above two, but with whole line
            if in_todo:
                line_tabs = count_tabs(line)

                start = find_start(initial_tabs, line_tabs)
                stop = len(line)

                print_line_nums(cols, line_num)
                print(line[start:stop])

        line_num += 1

def find_start(initial_tabs, line_tabs):
    """
    Changes starting point depending on where the TODO text is,
    relative to the start-TODO flag itself.

    Params:
        initial_tabs -> The amount of tabs to get to the start-TODO flag
        line_tabs -> The amount of tabs to get to the TODO text

    Returns:
        start -> The index to start printing the TODO from
    """

    if line_tabs < initial_tabs:
        # Start from the first non-tab character
        # This will cause the indentation to be off,
        # but the TODO text is still readable
        start = line_tabs * len(SPACE_TAB)
    else:
        # Start relative to the TODO flag
        start = initial_tabs * len(SPACE_TAB)

    return start


def count_tabs(line):
    """
    Counts the amount of leading tab-spaces in a string

    Params:
        line -> The string to operate on

    Returns:
        count -> Number of leading tab-spaces
    """

    if line.startswith(SPACE_TAB):
        start = 0
        end = 0

        while line[end] == ' ':
            end += 1
        end += 1

        count = line.count(SPACE_TAB, start, end)

    else:
        # If there isn't any leading whitespace,
        # no need to count
        count = 0

    return count

def print_line_nums(cols, line_num):
    """
    Prints the line number a certain amount of columns wide.
    The column width is equal to the max line number.
    Has leading 0's.

    Params:
        cols -> Columns that the max line number would take up
        line_num -> Current line number

    Returns:
        None
    """

    # cols - line_num.columns() = constant amount of characters
    print(INDENT_2, end='')
    for _ in range(cols - len(str(line_num))):
        print('0', end='')
    print('{0} '.format(line_num), end='')

# Test files:
todofinder('./tests/testfile')
todofinder('./tests/testfile2')
todofinder('./tests/testfile3')
todofinder('./tests/testfile4')
