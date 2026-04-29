#!/usr/bin/env python3
import argparse
import os
import sys


class RetCode():
    OK, ERR, ARG, WARN = range(4)


class TodoError(Exception):
    pass


class TodoList(object):

    def __init__(self, todo_file=None):
        self.todo_list = []
        self.todo_file = None

        if todo_file and os.path.isfile(todo_file):
            self.load(todo_file)

    def load(self, todo_file):
        self.todo_file = todo_file
        with open(self.todo_file, 'r') as f:
            item = None
            for line in f:
                line = line.rstrip('\n')
                if line.startswith('- text: '):
                    if item:
                        self.todo_list.append(item)
                    item = {'text': line[len('- text: '):]}
                elif line.startswith('  category: ') and item:
                    item['category'] = line[len('  category: '):]
            if item:
                self.todo_list.append(item)

    def save(self):
        with open(self.todo_file, 'w') as f:
            for item in self.todo_list:
                f.write('- text: {}\n'.format(item['text']))
                if 'category' in item:
                    f.write('  category: {}\n'.format(item['category']))

    def _format_item(self, item):
        if 'category' in item:
            return '{}: {}'.format(item['category'], item['text'])
        return item['text']

    def show(self):
        if len(self.todo_list) == 0:
            print("The todo list is empty. Add items with the '-a' argument.")
            return

        categories = []
        for item in self.todo_list:
            cat = item.get('category')
            if cat and cat not in categories:
                categories.append(cat)

        for k, item in enumerate(self.todo_list):
            if 'category' not in item:
                print('{:>3} - {}'.format(k + 1, item['text']))

        for cat in categories:
            print('\n{}:\n'.format(cat))
            for k, item in enumerate(self.todo_list):
                if item.get('category') == cat:
                    print('{:>3} - {}'.format(k + 1, item['text']))

    def add(self, text, category=None):
        item = {'text': text}
        if category:
            item['category'] = category
        self.todo_list.append(item)

    def delete(self, index):
        try:
            item = self.todo_list[index]
            del self.todo_list[index]
            print('\nRemoved: {}'.format(self._format_item(item)))
        except IndexError:
            raise TodoError('Index {} is out of range.'.format(index + 1))

    def reword(self, index):
        try:
            item = self.todo_list[index]
            print('\nOriginal: {}'.format(self._format_item(item)))
            item['text'] = input('Reword:   ')
        except IndexError:
            raise TodoError('Index {} is out of range.'.format(index + 1))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Simple Todo Script'
    )

    parser.add_argument(
        '-a', '--add',
        dest='add',
        metavar='"todo item"',
        help='add a todo item'
    )

    parser.add_argument(
        '-c', '--category',
        dest='category',
        metavar='"category"',
        help='category for the todo item (use with -a)'
    )

    parser.add_argument(
        '-d', '--delete',
        dest='delete',
        metavar='#',
        type=int,
        help='delete a todo item at index #'
    )

    parser.add_argument(
        '-r', '--reword',
        dest='reword',
        metavar='#',
        type=int,
        help='reword a todo item at index #'
    )

    args = parser.parse_args()

    return args


def main():
    args = parse_arguments()

    todo_file = os.path.expanduser('~/.todo_list.yaml')

    todo_list = TodoList(todo_file)

    if args.add:
        todo_list.add(args.add, category=args.category)
    elif args.delete:
        todo_list.delete(args.delete - 1)
    elif args.reword:
        todo_list.reword(args.reword - 1)

    if args.add or args.delete or args.reword:
        todo_list.save()

    todo_list.show()

    return RetCode.OK


if __name__ == '__main__':
    try:
        retcode = main()
    except KeyboardInterrupt as e:
        retcode = RetCode.WARN
    except TodoError as e:
        retcode = RetCode.ARG
        print('ERROR: {}'.format(e))

    sys.exit(retcode)
