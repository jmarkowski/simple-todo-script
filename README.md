# Simple Todo Script

Super simple command line interface (CLI) todo script to help track your
list of todos.

No more post-its!


# Details

The todo script tracks your todo items in a `.todo_list` in your home
directory. If the file doesn't exist, one will be created.


# Installation

    $ git clone https://github.com/jmarkowski/simple-todo-script.git
    $ cd simple-todo-script
    $ python3 setup.py install


# Usage

## Add

Initially, the todo list is empty. Let's add a couple of items.

```bash
$ todo

$ todo -a 'Return books to the library.'

 1 - Return books to the library.

$ todo -a 'Buy cat food.'

 1 - Return books to the library.
 2 - Buy cat food.

```

## Reword

You can reword items in your todo list.

```bash
$ todo -r 2

Original: Buy cat food.
Reword:   Buy dog food.

 1 - Return books to the library.
 2 - Buy dog food.

```

## Remove

You can delete items from your todo list when you're done.

```bash
$ todo -d 1

Removed: Return books to the library.

 1 - Buy dog food.

```

## Categorize

Finally, you may also categorize your todo list by prefixing the todo.

```bash
$ todo -a 'HOME: Fix faucet.'

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

HOME:

  2 - Fix faucet.
  4 - Replace bathroom mirror.

PROJECT:

  3 - Finish design diagram.

```

Note that the order in which todos are added is preserved in the list.
