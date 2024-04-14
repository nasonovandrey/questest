from tree_node import TreeNode


def print_current_node(node):
    print("Available children:")
    for i, child in enumerate(node.children, start=1):
        print(f"{i}. {child.name}")


def get_valid_choice(num_choices):
    while True:
        choice = input(f"Enter your choice (1-{num_choices} or 'b' to go back): ").strip()
        if choice == "b":
            return choice
        elif choice.isdigit() and 1 <= int(choice) <= num_choices:
            return choice
        else:
            print("Invalid choice, try again.")


def navigate_tree(tree: TreeNode):
    current_node = tree

    while True:
        clear_screen()
        if current_node.children:
            print_current_node(current_node)
            choice = get_valid_choice(len(current_node.children))
            if choice == "b":
                current_node = current_node.parent
            else:
                current_node = current_node.children[int(choice) - 1]
        else:
            result = breakpoint_insert(current_node.contents)
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


def clear_screen():
    print("\033[H\033[J")


def breakpoint_insert(contents):
    breakpoint_line = "breakpoint()  # Inserted by navigate_tree"
    code_lines = contents.split("\n")
    code_lines.insert(1, breakpoint_line)
    num_lines = len(code_lines)
    current_line = 1
    indent = "    "

    while True:
        clear_screen()

        for line in code_lines:
            print(line)

        key = input(
            "\nUse 'w' to move up \n's' to move down \n'd' to mode right \n'a' to move left \n'i' to insert a breakpoint \n'n' to run test without insertion \n'b' to go back: "
        ).lower()

        if key == "w" and current_line > 1:
            code_lines[current_line], code_lines[current_line - 1] = (
                code_lines[current_line - 1],
                breakpoint_line,
            )
            current_line -= 1
        elif key == "s" and current_line < num_lines - 1:
            code_lines[current_line], code_lines[current_line + 1] = (
                code_lines[current_line + 1],
                breakpoint_line,
            )
            current_line += 1
        elif key == "d":
            breakpoint_line = indent + breakpoint_line
            code_lines[current_line] = breakpoint_line
        elif key == "a" and breakpoint_line.startswith(indent):
            breakpoint_line = breakpoint_line[4:]
            code_lines[current_line] = breakpoint_line
        elif key == "i" or key == "b" or key == "n":
            break

    if key == "b":
        return None
    if key == "n":
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
