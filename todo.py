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
                elif line.startswith('  done: ') and item:
                    item['done'] = line[len('  done: '):] == 'true'
            if item:
                self.todo_list.append(item)

    def save(self):
        with open(self.todo_file, 'w') as f:
            for item in self.todo_list:
                f.write('- text: {}\n'.format(item['text']))
                if 'category' in item:
                    f.write('  category: {}\n'.format(item['category']))
                if item.get('done'):
                    f.write('  done: true\n')

    def _format_item(self, item):
        if 'category' in item:
            return '{}: {}'.format(item['category'], item['text'])
        return item['text']

    def show(self, show_done=False):
        items = [(k, item) for k, item in enumerate(self.todo_list)
                 if item.get('done', False) == show_done]

        if len(items) == 0:
            if show_done:
                print("No completed items.")
            else:
                print("The todo list is empty. Add items with the '-a' argument.")
            return

        categories = []
        for _, item in items:
            cat = item.get('category')
            if cat and cat not in categories:
                categories.append(cat)

        for k, item in items:
            if 'category' not in item:
                print('{:>3} - {}'.format(k + 1, item['text']))

        for cat in categories:
            print('\n{}:\n'.format(cat))
            for k, item in items:
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
            print('\nRemoved: {}\n'.format(self._format_item(item)))
        except IndexError:
            raise TodoError('Index {} is out of range.'.format(index + 1))

    def reword(self, index):
        try:
            item = self.todo_list[index]
            print('\nOriginal: {}'.format(self._format_item(item)))
            item['text'] = input('Reword:   ')
        except IndexError:
            raise TodoError('Index {} is out of range.'.format(index + 1))

    def mark_done(self, index):
        try:
            item = self.todo_list[index]
            if item.get('done'):
                raise TodoError('Item {} is already done.'.format(index + 1))
            item['done'] = True
            print('\nDone: {}\n'.format(self._format_item(item)))
        except IndexError:
            raise TodoError('Index {} is out of range.'.format(index + 1))

    def categorize(self, index, category):
        try:
            item = self.todo_list[index]
            old = self._format_item(item)
            if category:
                item['category'] = category
            else:
                item.pop('category', None)
            print('\nRecategorized: {} -> {}\n'.format(old, self._format_item(item)))
        except IndexError:
            raise TodoError('Index {} is out of range.'.format(index + 1))

    def clear_done(self):
        removed = [item for item in self.todo_list if item.get('done')]
        self.todo_list = [item for item in self.todo_list if not item.get('done')]
        if removed:
            print('\nCleared {} completed item(s).\n'.format(len(removed)))
        else:
            print('\nNo completed items to clear.\n')

    def move(self, src_index, dst_index):
        try:
            item = self.todo_list.pop(src_index)
        except IndexError:
            raise TodoError('Index {} is out of range.'.format(src_index + 1))

        if dst_index < 0 or dst_index > len(self.todo_list):
            raise TodoError('Index {} is out of range.'.format(dst_index + 1))

        self.todo_list.insert(dst_index, item)
        print('\nMoved: {} -> position {}\n'.format(
            self._format_item(item), dst_index + 1))


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Simple Todo Script',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='examples:\n'
               '  todo -a "item one" "item two" "item three"\n'
               '  todo -a "item one" "item two" -c ideas\n'
               '  todo -d 3 5 7\n'
               '  todo -m 5 1\n'
               '  todo -n 3 -c "new category"\n'
               '  todo --done 3 5\n'
               '  todo --done\n'
               '  todo --clear-done\n'
    )

    parser.add_argument(
        '-a', '--add',
        dest='add',
        nargs='+',
        metavar='"todo item"',
        help='add one or more todo items'
    )

    parser.add_argument(
        '-c', '--category',
        dest='category',
        metavar='"category"',
        help='set category (use with -a to categorize new items, '
             'or with -n to recategorize an existing item)'
    )

    parser.add_argument(
        '-n', '--item-number',
        dest='item_number',
        metavar='#',
        type=int,
        help='item index to recategorize (use with -c)'
    )

    parser.add_argument(
        '--done',
        dest='done',
        nargs='*',
        metavar='#',
        type=int,
        help='mark items as done at index #, or show done items if no index given'
    )

    parser.add_argument(
        '--clear-done',
        dest='clear_done',
        action='store_true',
        help='remove all completed items from the list'
    )

    parser.add_argument(
        '-d', '--delete',
        dest='delete',
        nargs='+',
        metavar='#',
        type=int,
        help='delete one or more todo items at index #'
    )

    parser.add_argument(
        '-m', '--move',
        dest='move',
        nargs=2,
        metavar=('#', '#'),
        type=int,
        help='move a todo item from index # to index #'
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

    modified = False

    if args.add:
        for text in args.add:
            todo_list.add(text, category=args.category)
        modified = True
    elif args.item_number and args.category is not None:
        todo_list.categorize(args.item_number - 1, args.category)
        modified = True
    elif args.done is not None and len(args.done) > 0:
        for index in sorted(args.done, reverse=True):
            todo_list.mark_done(index - 1)
        modified = True
    elif args.clear_done:
        todo_list.clear_done()
        modified = True
    elif args.delete:
        for index in sorted(args.delete, reverse=True):
            todo_list.delete(index - 1)
        modified = True
    elif args.move:
        todo_list.move(args.move[0] - 1, args.move[1] - 1)
        modified = True
    elif args.reword:
        todo_list.reword(args.reword - 1)
        modified = True

    if modified:
        todo_list.save()

    show_done = args.done is not None and len(args.done) == 0
    todo_list.show(show_done=show_done)

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
