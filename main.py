#!/usr/bin/python3

import sys

from commands import commands

help_info = "questest run <testdir> or questest <testdir> to run questest\nquestest clean <testdir> to remove all breakpoints\nquestest run-clean <testdir> to remove all breakpoints and then run questest\nquestest run-again to repeat last run\nquestest help to output this message\n"

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "run-again":
            commands[sys.argv[1]]()
            sys.exit(0)
        if sys.argv[1] == "help":
            print(help_info)
            sys.exit(0)
        command = "run"
        testdir = sys.argv[1]
    elif len(sys.argv) == 3:
        command = sys.argv[1]
        testdir = sys.argv[2]
    else:
        print("Unknown command")
        print(help_info)
        sys.exit(1)
    commands[command](testdir)
