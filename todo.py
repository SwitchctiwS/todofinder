"""
Title: Todofinder

Author: Jared Thibault
Date: 27 February 2017

Program description:
    This will find all the different TODO's in a file and output every TODO to stdout.
    If there is a file named 'TODO.txt', then it will output that file's contents as well.
    It will recurse into all folders if recursive option is specified.

Operation:
    Put HTML-like TODO flags around code, bullet points, etc.

    Example:
    <TODO>
    [...]    and    <TODO>[...]</TODO>
    </TODO>
"""

"""
<TODO>
- comment code
- figure this out:
    import argparse

    parse = argparse.ArgumentParser(description='Finds all TODO\'s in
            a folder and outputs them to stdout')
    parse.add_argument('')
</TODO>
"""

START_TODO_DELIM = '<TODO>'
STOP_TODO_DELIM = '</TODO>'
SPACE_TAB = '    '
INDENT_1 = '    '
INDENT_2 = '      '

def todofinder(filename):
    """Finds TODOs in file"""

    print(filename)
    with open(filename, 'r') as file:
        text = file.read()

    if text.count(START_TODO_DELIM) != text.count(STOP_TODO_DELIM):
        print(INDENT_1 + '!!! ERROR !!! TODOs don\'t match!')
        print()
        return

    line_num = 1
    for line in text.splitlines():
        line_num += 1
    cols = len(str(line_num))

    line_num = 1
    todo_num = 0
    in_todo = False
    for line in text.splitlines():
        line = line.expandtabs(tabsize=len(SPACE_TAB))

        if START_TODO_DELIM in line and STOP_TODO_DELIM in line:
            todo_num += 1

            start = line.find(START_TODO_DELIM) + len(START_TODO_DELIM)
            stop = line.find(STOP_TODO_DELIM)

            print(INDENT_1 + 'TODO{0}'.format(todo_num))
            print_line_nums(cols, line_num)
            print(line[start:stop])
            print(INDENT_1 + 'END{0}'.format(todo_num))
            print()

        elif START_TODO_DELIM in line:
            todo_num += 1
            in_todo = True

            initial_tabs = count_tabs(line)

            start = line.find(START_TODO_DELIM) + len(START_TODO_DELIM)
            stop = len(line)

            print(INDENT_1 + 'TODO{0}'.format(todo_num))
            if start != stop:
                print_line_nums(cols, line_num)
                print(line[start:stop])

        elif STOP_TODO_DELIM in line:
            in_todo = False

            line_tabs = count_tabs(line)
            if line_tabs > initial_tabs:
                start = initial_tabs * len(SPACE_TAB)
            elif line_tabs < initial_tabs:
                start = line_tabs * len(SPACE_TAB)
            else:
                start = initial_tabs * len(SPACE_TAB)

            stop = line.find(STOP_TODO_DELIM)

            if start != stop:
                print_line_nums(cols, line_num)
                print(line[start:stop])
            print(INDENT_1 + 'END{0}'.format(todo_num))
            print()

        else:
            if in_todo:
                line_tabs = count_tabs(line)
                if line_tabs > initial_tabs:
                    start = initial_tabs * len(SPACE_TAB)
                elif line_tabs < initial_tabs:
                    start = line_tabs * len(SPACE_TAB)
                else:
                    start = initial_tabs * len(SPACE_TAB)

                stop = len(line)

                print_line_nums(cols, line_num)
                print(line[start:stop])

        line_num += 1

def count_tabs(line):
    """Counts the amount of leading tab-spaces in a string"""

    if line.startswith(SPACE_TAB):
        start = 0
        end = 0

        while line[end] == ' ':
            end += 1
        end += 1

        count = line.count(SPACE_TAB, start, end)

    else:
        count = 0

    return count

def print_line_nums(cols, line_num):
    """
    Prints ' xxx', where 'x' is the line number.
    There is a constant amount of columns printed.
    """

    print(INDENT_2, end='')
    for _ in range(cols - len(str(line_num))):
        print('0', end='')
    print('{0} '.format(line_num), end='')

todofinder('./testfile')
todofinder('./testfile2')
todofinder('./testfile3')
todofinder('./testfile4')
