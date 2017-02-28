def test():
    string = '    yeee'
    string2 = '\tasdf'

    print(string.startswith('    '))
    print(string2.startswith('\t'))

    print(string + '\n' + string2)
    for i in range(4, len(string)):
        print(string[i], end='')
    print()

    for i in range(1, len(string2)):
        print(string2[i], end='')
    print()

test()
