#!/usr/bin/env python3
import argparse
import os
import sys
import pickle


class RetCode():
    OK, ERR, ARG, WARN = range(4)


def load_todo_list(todo_file):
    todo_list = []

    if os.path.isfile(todo_file):
        try:
            f = open(todo_file, 'r+b')
            todo_list = pickle.load(f)
            f.close()
        except EOFError:
            # File is empty.
            pass

    return todo_list


def save_todo_list(todo_file, todo_list):
    f = open(todo_file, 'wb')
    pickle.dump(todo_list, f)
    f.close()


def print_todo_list(todo_list):
    found_categories = []

    # Print all the uncategorized todos first
    for idx,item in enumerate(todo_list):
        cat_idx = item.rfind(':')
        if cat_idx > 0:
            cat = item[0:cat_idx]
            try:
                found_categories.index(cat)
            except ValueError:
                # The category could not be found
                found_categories.append(cat)
        else:
            print('\n {0} - {1}'.format(idx+1, item))

    # Print all categorized todos
    for cat in found_categories:
        print('\n{0}:'.format(cat))
        for idx,item in enumerate(todo_list):
            cat_idx = item.rfind(':')
            if cat_idx > 0 and cat == item[0:cat_idx]:
                print('\n {0} - {1}'.format(idx+1, item[cat_idx+1:].lstrip()))


def add_todo(todo_list, todo):
    todo_list.append(todo)


def remove_todo(todo_list, idx):
    item = todo_list[idx]
    del todo_list[idx]
    print('\nRemoved: {0}'.format(item))


def modify_todo(todo_list, idx):
    print('\nOriginal: {0}'.format(todo_list[idx]))
    reword = input('Reword:   ')
    todo_list[idx] = reword


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Python Todo Script'
    )

    parser.add_argument(
        '-a', '--add',
        dest='add',
        metavar='"item"',
        help='add a todo item'
    )

    parser.add_argument(
        '-r', '--remove',
        dest='remove',
        metavar='#',
        help='remove a todo item at the given index #'
    )

    parser.add_argument(
        '-m', '--modify',
        dest='modify',
        metavar='#',
        help='modify a todo item at the given index #'
    )

    args = parser.parse_args()

    return args


def main():
    args = parse_arguments()

    todo_file = os.path.expanduser('~/.todo_list')

    todo_list = load_todo_list(todo_file)

    if args.add:
        add_todo(todo_list, args.add)
        save_todo_list(todo_file, todo_list)
    elif args.remove or args.modify:
        try:
            if args.modify:
                idx = int(args.modify)
            elif args.remove:
                idx = int(args.remove)

            assert(idx > 0)
            idx = idx - 1

            if args.modify:
                modify_todo(todo_list, idx)
            elif args.remove:
                remove_todo(todo_list, idx)

            save_todo_list(todo_file, todo_list)
        except IndexError:
            print('Error: Index is out of range.')
        except ValueError:
            print('Error: Index must be an integer.')
        except AssertionError:
            print('Error: Index must be > 0.')

    print_todo_list(todo_list)

    return RetCode.OK


if __name__ == '__main__':
    retcode = main()
    sys.exit(retcode)
