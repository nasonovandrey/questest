import sys

from commands import commands

if __name__ == "__main__":
    if len(sys.argv) == 2:
        command = "run"
        testdir = sys.argv[1]
    elif len(sys.argv) == 3:
        command = sys.argv[1]
        testdir = sys.argv[2]
    commands[command](testdir)
