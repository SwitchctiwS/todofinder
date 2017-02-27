"""
Program description:
    This will find all the different TODO's in a file and output every TODO to stdout.
    If there is a file named 'TODO', then it will output that file's contents as well.
    It will recurse into all folders if recursive option is specified.

Possible operation:
    <TODO>
        [...]
    </TODO>

    ALSO (maybe)

    <TODO>[...]</TODO>
"""

# <TODO>
#import argparse

# figure this out:
#parse = argparse.ArgumentParser(description='Finds all TODO\'s in
# 		a folder and outputs them to stdout')
#parse.add_argument('')
# </TODO>

def todofinder(filename):
    """Finds TODOs in file"""

    start_todo_delim = '<TODO>'
    stop_todo_delim = '</TODO>'

    with open(filename, 'r') as file:
        line_num = 1
        for line in file:
            line_num += 1
        cols = len(str(line_num))

        file.seek(0)

        print(filename)
        line_num = 1
        todo_num = 0
        in_todo = False
        for line in file:
            if start_todo_delim in line and stop_todo_delim in line:
                todo_num += 1

                start = line.find(start_todo_delim) + len(start_todo_delim)
                stop = line.find(stop_todo_delim)

                print('  TODO{0}'.format(todo_num))
                print_line_nums(cols, line_num)
                print_todo(line, start, stop)
                print('  END{0}'.format(todo_num))
                print()

            elif start_todo_delim in line:
                todo_num += 1
                in_todo = True

                start = line.find(start_todo_delim) + len(start_todo_delim)
                stop = len(line) - 1

                print('  TODO{0}'.format(todo_num))
                if start != stop:
                    print_line_nums(cols, line_num)
                    print_todo(line, start, stop)

            elif stop_todo_delim in line:
                in_todo = False

                start = 0
                stop = line.find(stop_todo_delim)

                if start != stop:
                    print_line_nums(cols, line_num)
                    print_todo(line, start, stop)
                print('  END{0}'.format(todo_num))
                print()

            else:
                if in_todo:
                    print_line_nums(cols, line_num)
                    print_todo(line, 0, len(line) - 1)

            line_num += 1

def print_todo(line, start, stop):
    """Prints line inbetween start and stop"""
    for i in range(start, stop):
        print(line[i], end='')
    print()

def print_line_nums(cols, line_num):
    """
    Prints ' xxx', where 'x' is the line number.
    There is a constant amount of columns printed.
    """

    print('    ', end='')
    for _ in range(cols - len(str(line_num))):
        print('0', end='')
    print('{0} '.format(line_num), end='')


todofinder('./testfile')
todofinder('./testtt')
