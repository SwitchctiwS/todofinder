#!/usr/bin/env python3
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

#Imports:
import argparse # For CLI arguments
import os # For file/directory operations

# Defines:
VERSION = '1.0.1' # [major].[minor].[patch]

START_TODO_DELIM = '<TODO>' # Start-todo delimiter
STOP_TODO_DELIM = '</TODO>' # Stop-todo delimiter
SPACE_TAB = '    ' # 1 tab = 4 spaces
INDENT_1 = '    ' # 4 spaces
INDENT_2 = '      ' # 6 spaces

# Methods:

"""
<TODO>
make proper exceptions
make todofinder.py * -r -x *.exe work correctly
    globbing?
</TODO>
"""

def main():
    """
    Main method

    Params:
        None

    Returns:
        None
    """

    # argparse
    parser = argparse.ArgumentParser(prog='Todofinder',
                                     description='Finds and outputs TODOs in file.')

    parser.add_argument('filename',
                        nargs='+',
                        help='name of file(s)/dir(s)')

    parser.add_argument('-r', '--recursive',
                        action='store_true',
                        default=False,
                        help='recurse into folders')
    parser.add_argument('-x', '--exclude',
                        nargs='+',
                        help='excludes file(s)/dir(s)')
    parser.add_argument('-s', '--follow-links',
                        action='store_true',
                        default=False,
                        help='follow symlinks')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s {0}'.format(VERSION),
                        help='prints version information')

    args = parser.parse_args()

    for file_or_dir in args.filename:
        find_files(file_or_dir, args.exclude, args.recursive, args.follow_links)

def todofinder(f):
    """
    Finds and displays TODOs in a file

    Params:
        f -> The file to find TODOs

    Returns:
        None
    """

    print(f.name)

    # Counts line numbers and finds out how many
    # columns the line number takes up
    # Also counts number of start-TODOs and stop-TODOs
    line_num = 1
    start_todo = 0
    stop_todo = 0
    for line in f.readlines():
        if START_TODO_DELIM in line:
            start_todo += 1
        if STOP_TODO_DELIM in line:
            stop_todo += 1

        line_num += 1
    cols = len(str(line_num))

    # <TODO>
    # Gives error and returns if there are different
    # number of start-TODO and stop-TODO
    if start_todo != stop_todo:
        print(INDENT_1 + '!!! ERROR !!! Unmatched TODOs')
        print()
        return
    # </TODO>

    # Bring file back to beginning
    f.seek(0)

    # Goes line-by-line and sees if there are
    # any TODOs in that line
    line_num = 1
    todo_num = 0
    in_todo = False
    for line in f.readlines():
        # Convert tabs to spaces (easier to deal with)
        line = line.expandtabs(tabsize=len(SPACE_TAB))

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
            stop = len(line) - 1

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
                stop = len(line) - 1

                print_line_nums(cols, line_num)
                print(line[start:stop])

        line_num += 1

    # Newline if there are no todos
    # Makes things look pretty
    if todo_num == 0:
        print(INDENT_1 + 'None')
        print()

def find_files(file_or_dir, excludes, recursive, followlinks):
    """
    Performs file testing and optional recursion

    Params:
        file_or_dir -> File/directory to test
        recursive -> User-specified flag to recurse into directories
        followlinks -> User-specified flag to follow symlinks

    Returns:
        None
    """

    # Return if current file_or_dir is in the list of excludes
    # No reason to continue further
    if excludes is not None:
        if file_or_dir in excludes:
            return

    # If no excludes, makes it equal to the empty set
    # Prevents errors later on, since set() cannot iterate
    # over None
    else:
        excludes = set()

    #<TODO>
    # Gives error when file/dir doesn't exist
    # Also gives an error if file is a broken symlink
    if os.path.exists(file_or_dir) is False:
        print('!!! ERROR !!! \'{0}\' is not a file/directory'.format(file_or_dir)
              + ' or is a broken symlink')
        print()
        return
    #</TODO>

    # No point of checking file if it's a symlink and
    # followlinks is off
    # However, it will continue to check other files/dirs
    # Thus, no error
    if os.path.islink(file_or_dir) and followlinks is False:
        print('\'{0}\' is a symlink'.format(file_or_dir))
        print()
        return

    # Goes (walks) into directory and reads directories and files
    if os.path.isdir(file_or_dir):
        # Automatically recurses into folders (elements in subdirs)
        for root, subdirs, files in os.walk(file_or_dir, followlinks=followlinks):
            # If not recursive, set of excludes is all subdirs
            # That is, do not enter any subdirectories
            if recursive is False:
                exclude_dirs = set(subdirs)

            else:
                exclude_dirs = set(excludes) & set(subdirs)

            # Creates set of files/dirs that are in subdirs and in excludes
            exclude_files = set(excludes) & set(files)

            # Removes directories from recursion list
            if exclude_dirs is not set():
                for directory in exclude_dirs:
                    subdirs.remove(directory)

            # Removes files from checking list
            if exclude_files is not set():
                for f in exclude_files:
                    files.remove(f)

            # Call todofinder() on left over files
            for filename in files:
                with open(os.path.join(root, filename), 'r') as f:
                    todofinder(f)

    #Reads file
    elif os.path.isfile(file_or_dir):
        with open(file_or_dir, 'r') as f:
            todofinder(f)

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
        # Case:
        #       <TODO>...
        #   </TODO>
        # You shouldn't be doing this anyway!

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

# Execute code
if __name__ == '__main__':
    main()
