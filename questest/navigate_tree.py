import ast
import curses

from questest.tree_node import TreeNode


def print_current_node(stdscr, node, selected_index):
    stdscr.clear()
    stdscr.addstr("Available children:\n")
    for i, child in enumerate(node.children, start=1):
        if i - 1 == selected_index:
            stdscr.addstr(f"> {i}. {child.name}\n", curses.A_REVERSE)
        else:
            stdscr.addstr(f"  {i}. {child.name}\n")


def navigate_tree(stdscr, tree: TreeNode):
    current_node = tree
    selected_index = 0

    while True:
        if current_node.children:
            print_current_node(stdscr, current_node, selected_index)
            stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_UP:
                selected_index = max(0, selected_index - 1)
            elif key == curses.KEY_DOWN:
                selected_index = min(len(current_node.children) - 1, selected_index + 1)
            elif key == ord("b"):
                if current_node.parent:
                    current_node = current_node.parent
            elif key == curses.KEY_ENTER or key in [10, 13]:
                current_node = current_node.children[selected_index]
            stdscr.refresh()
        else:
            result = breakpoint_insert(stdscr, current_node.contents)
            if result is None:
                current_node = current_node.parent
            elif result is not None:
                edit_file(
                    current_node.parent.name,
                    current_node.start_line,
                    current_node.end_line,
                    result,
                )
                return current_node.parent.name, current_node.name


def breakpoint_insert(stdscr, contents):
    breakpoint_line = "breakpoint() # Inserted by navigate_tree"
    code_lines = contents.split("\n")
    code_lines.insert(1, breakpoint_line)
    num_lines = len(code_lines)
    current_line = 1
    indent = "    "
    help_info = "\nUse arrows to move, \nenter to insert a breakpoint and run, \n'n' to run test without insertion \n'b' to go back: "

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        line_num = 1
        for line in code_lines:
            if line_num == current_line:
                stdscr.addstr(line + "\n", curses.A_REVERSE)
            else:
                stdscr.addstr(line + "\n")
            line_num += 1

        stdscr.addstr(help_info)
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_line > 1:
            code_lines[current_line], code_lines[current_line - 1] = (
                code_lines[current_line - 1],
                breakpoint_line,
            )
            current_line -= 1
        elif key == curses.KEY_DOWN and current_line < num_lines - 1:
            code_lines[current_line], code_lines[current_line + 1] = (
                code_lines[current_line + 1],
                breakpoint_line,
            )
            current_line += 1
        elif key == curses.KEY_RIGHT:
            breakpoint_line = indent + breakpoint_line
            code_lines[current_line] = breakpoint_line
        elif key == curses.KEY_LEFT and breakpoint_line.startswith(indent):
            breakpoint_line = breakpoint_line[len(indent) :]
            code_lines[current_line] = breakpoint_line
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if is_valid_function_definition("\n".join(code_lines)):
                break
            else:
                stdscr.move(height - 1, 0)  # Move cursor to bottom of screen
                stdscr.clrtoeol()  # Clear the line
                stdscr.addstr("Invalid breakpoint placement")
                stdscr.getch()  # Wait for user input before continuing
                stdscr.move(0, 0)  # Move cursor back to top
        elif key == ord("b") or key == ord("n"):
            break

        stdscr.refresh()

    if key == ord("b"):
        return None
    if key == ord("n"):
        return contents

    updated_contents = "\n".join(code_lines)
    return updated_contents


def edit_file(filename, start_line, end_line, new_contents):
    with open(filename, "r") as file:
        lines = file.readlines()

    if start_line < 0 or end_line > len(lines):
        raise IndexError(f"Invalid start or end line numbers: {start_line}, {end_line}.")

    lines = [line.rstrip("\n") for line in lines]

    lines = lines[:start_line] + new_contents.split("\n") + lines[end_line:]

    with open(filename, "w") as file:
        file.write("\n".join(lines))

    print(
        f"Contents replaced successfully from line {start_line} to line {end_line} in '{filename}'."
    )


def is_valid_function_definition(contents):
    try:
        tree = ast.parse(contents)
        if len(tree.body) == 1 and isinstance(tree.body[0], ast.FunctionDef):
            return True
        else:
            return False
    except SyntaxError:
        return False
