# python-todo-script

Super simple CLI todo script to help track a list of your general todos.
No more post-its!

**Note: This script written for python3 only.**

# Details

The todo.py script tracks your todo items in a `.todo_list` in your `$HOME`
directory. If the file doesn't exist, one will be created. It forever uses this
file to track your todos.

Items are listed in the order they are added.

# Usage

## Add

Initially, the todo list is empty. Let's add a couple of items.

```bash
$ todo.py

$ todo.py -a 'Return books to the library.'

 1 - Return books to the library.

$ todo.py -a 'Buy cat food.'

 1 - Return books to the library.

 2 - Buy cat food.

```

## Reword

You can reword items in your todo list.

```bash
$ todo.py -r 2

Original: Buy cat food.
Reword:   Buy dog food.

 1 - Return books to the library.

 2 - Buy dog food.

```

## Remove

You can delete items from your todo list when you're done.

```bash
$ todo.py -d 1

Removed: Return books to the library.

 1 - Buy dog food.

```

## Categorize

Finally, you may also categorize your todo list by prefixing the todo.

```bash
$ todo.py -a 'HOME: Fix faucet.'

 1 - Buy dog food.

HOME:

 2 - Fix faucet.

```

```bash
$ todo -a 'PROJECT: Finish design diagram.'

 1 - Buy dog food.

HOME:

 2 - Fix faucet.

PROJECT:

 3 - Finish design diagram.

```

Any new categorized todo items will automatically get grouped together.

```bash
$ todo -a 'HOME: Replace bathroom mirror.'

 1 - Buy dog food.

PROJECT:

 3 - Finish design diagram.

HOME:

 2 - Fix faucet.

 4 - Replace bathroom mirror.

```
