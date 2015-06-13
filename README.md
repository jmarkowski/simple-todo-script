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

Initially, the todo list is empty. Let's add a couple of items.

```bash
$ todo.py

$ todo.py -a 'Return books to the library.'

 1 - Return books to the library.

$ todo.py -a 'Buy cat food.'

 1 - Return books to the library.

 2 - Buy cat food.

```

You can modify your todo list.

```bash
$ todo.py -m 2

Original: Buy cat food.
Reword:   Buy dog food.

 1 - Return books to the library.

 2 - Buy dog food.

```

Finally, you can remove items from your todo list when you're done.

```bash
$ todo.py -r 1

Removed: Return books to the library.

 1 - Buy dog food.

```
