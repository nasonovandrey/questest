import curses
import subprocess
from pathlib import Path

from questest.build_tree import build_tree
from questest.navigate_tree import navigate_tree

dump_filename = ".prev_command"


def clean(directory):
    sed_command = r"sed -i '/^\s*breakpoint()/d' {}"
    subprocess.run(
        [
            "find",
            directory,
            "-type",
            "f",
            "-name",
            "*.py",
            "-exec",
            "bash",
            "-c",
            sed_command + r" && echo {}",
            ";",
        ],
        check=True,
    )


def run_again():
    if not Path(dump_filename).exists():
        print("No history to remember. First do a usual run")
        return

    with open(dump_filename, "r") as f:
        lines = f.readlines()
    filename = lines[0].rstrip("\n")
    testname = lines[1].rstrip("\n")

    command = f"pytest --pdb --pdbcls=IPython.terminal.debugger:TerminalPdb {filename}::{testname}"
    subprocess.run(command, shell=True)


def run(directory):
    def run_wrapper(stdscr):
        tree = build_tree(Path(directory))
        filename, testname = navigate_tree(stdscr, tree)
        return filename, testname

    filename, testname = curses.wrapper(run_wrapper)
    with open(dump_filename, "w") as f:
        f.write(f"{filename}\n{testname}")

    command = f"pytest --pdb --pdbcls=IPython.terminal.debugger:TerminalPdb {filename}::{testname}"
    subprocess.run(command, shell=True)


def run_clean(directory):
    clean(directory)
    run(directory)


commands = {"run": run, "clean": clean, "run-clean": run_clean, "run-again": run_again}
