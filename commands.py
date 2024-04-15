import subprocess
from pathlib import Path

from build_tree import build_tree
from navigate_tree import navigate_tree


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


def run(directory):
    tree = build_tree(Path(directory))
    filename, testname = navigate_tree(tree)
    command = f"pytest --pdb --pdbcls=IPython.terminal.debugger:TerminalPdb {filename}::{testname}"
    subprocess.run(command, shell=True)


def clean_run(directory):
    clean(directory)
    run(directory)


commands = {"run": run, "clean": clean, "clean-run": clean_run}
