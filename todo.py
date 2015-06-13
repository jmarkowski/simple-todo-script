#!/usr/bin/env python3
import os
import sys
import pickle
from optparse import OptionParser


TODO_FILE = os.path.expanduser('~/.todo_list')

todo_list = []


def load_todo_list():
    global todo_list, TODO_FILE

    if os.path.isfile(TODO_FILE):
        try:
            f = open(TODO_FILE, 'r+b')
            todo_list = pickle.load(f)
            f.close()
        except EOFError:
            # File is empty.
            pass


def save_todo_list():
    global todo_list, TODO_FILE

    f = open(TODO_FILE, 'wb')
    pickle.dump(todo_list, f)
    f.close()


def print_todo_list():
    global todo_list

    for idx,item in enumerate(todo_list):
        print('\n {0} - {1}'.format(idx+1, item))


def add_todo(todo):
    global todo_list
    todo_list.append(todo)


def remove_todo(idx):
    global todo_list
    item = todo_list[idx]
    del todo_list[idx]
    print('\nRemoved: {0}'.format(item))


def modify_todo(idx):
    global todo_list
    print('\nOriginal: {0}'.format(todo_list[idx]))
    reword = input('Reword:   ')
    todo_list[idx] = reword


def parse_arguments():
    parser = OptionParser()

    parser.usage = os.path.basename(sys.argv[0]) + ' [options]'

    parser.add_option('-a', '--add', dest='add', metavar='"item"',
        help='add a todo item')

    parser.add_option('-r', '--remove', dest='remove', metavar='#',
        help='remove a todo item at the given index #')

    parser.add_option('-m', '--modify', dest='modify', metavar='#',
        help='modify a todo item at the given index #')

    (options, args) = parser.parse_args()

    return options


def main():
    options = parse_arguments()

    load_todo_list()

    if options.add:
        add_todo(options.add)
        save_todo_list()
    elif options.remove or options.modify:
        try:
            if options.modify:
                idx = int(options.modify)
            elif options.remove:
                idx = int(options.remove)

            assert(idx > 0)
            idx = idx - 1

            if options.modify:
                modify_todo(idx)
            elif options.remove:
                remove_todo(idx)

            save_todo_list()
        except IndexError:
            print('Error: Index is out of range.')
        except ValueError:
            print('Error: Index must be an integer.')
        except AssertionError:
            print('Error: Index must be > 0.')

    print_todo_list()

    return 0


if __name__ == '__main__':
    retcode = main()
