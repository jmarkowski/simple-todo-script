#!/usr/bin/env python3
import argparse
import os
import sys
import pickle


class RetCode():
    OK, ERR, ARG, WARN = range(4)


class TodoList(object):

    def __init__(self, todo_file=None):
        self.todo_list = []
        self.todo_file = None

        if todo_file and os.path.isfile(todo_file):
            self.load(todo_file)

    def load(self, todo_file):
        self.todo_file = todo_file
        try:
            with open(self.todo_file, 'r+b') as f:
                self.todo_list = pickle.load(f)
        except EOFError:
            # File is empty.
            pass

    def save(self):
        with open(self.todo_file, 'wb') as f:
            pickle.dump(self.todo_list, f)

    def show(self):
        found_categories = []

        # Print all the uncategorized todos first
        for idx,item in enumerate(self.todo_list):
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
            for idx,item in enumerate(self.todo_list):
                cat_idx = item.rfind(':')
                if cat_idx > 0 and cat == item[0:cat_idx]:
                    print('\n {0} - {1}'.format(idx+1, item[cat_idx+1:].lstrip()))

    def add(self, todo):
        self.todo_list.append(todo)

    def delete(self, index):
        item = self.todo_list[index]
        del self.todo_list[index]
        print('\nRemoved: {0}'.format(item))

    def modify(self, index):
        print('\nOriginal: {0}'.format(self.todo_list[index]))
        reword = input('Reword:   ')
        self.todo_list[index] = reword


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
        '-d', '--delete',
        dest='delete',
        metavar='#',
        help='delete a todo item at the given index #'
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

    todo_list = TodoList(todo_file)

    if args.add:
        todo_list.add(args.add)
        todo_list.save()
    elif args.delete or args.modify:
        try:
            if args.modify:
                idx = int(args.modify)
            elif args.delete:
                idx = int(args.delete)

            assert(idx > 0)
            idx = idx - 1

            if args.modify:
                todo_list.modify(idx)
            elif args.delete:
                todo_list.delete(idx)

            todo_list.save()
        except IndexError:
            print('Error: Index is out of range.')
        except ValueError:
            print('Error: Index must be an integer.')
        except AssertionError:
            print('Error: Index must be > 0.')

    todo_list.show()

    return RetCode.OK


if __name__ == '__main__':
    retcode = main()
    sys.exit(retcode)
