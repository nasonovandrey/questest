import ast
from pathlib import Path
from typing import List, Optional

from tree_node import TreeNode


def get_function_definitions(file_path: Path) -> List[TreeNode]:
    with file_path.open() as f:
        source = f.read()

    tree = ast.parse(source)
    function_nodes = []

    for node in tree.body:
        if (
            isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef)
        ) and node.name.startswith("test_"):
            start_line = node.lineno
            end_line = node.body[-1].end_lineno + 1
            function_lines = source.splitlines()[start_line - 1 : end_line - 1]
            function_definition = "\n".join(function_lines)
            function_node = TreeNode(
                node.name,
                contents=function_definition,
                start_line=start_line - 1,
                end_line=end_line - 1,
            )
            function_nodes.append(function_node)

    return function_nodes


def build_tree(root_dir: Path, root_name: str = "") -> Optional[TreeNode]:
    root_node = TreeNode(root_name if root_name else str(root_dir))

    for entry in root_dir.iterdir():
        if entry.is_dir():
            child_node = build_tree(entry, root_name=root_name)
            if child_node:
                child_node.parent = root_node
                root_node.children.append(child_node)
        elif entry.is_file() and entry.suffix == ".py" and entry.name.startswith("test_"):
            parent_name = root_node.name
            relative_path = Path(parent_name) / entry.name
            test_file_node = TreeNode(str(relative_path))
            test_file_node.parent = root_node
            root_node.children.append(test_file_node)

            # Get function nodes and add them as children of the test file node
            function_nodes = get_function_definitions(entry)
            for function_node in function_nodes:
                function_node.parent = test_file_node
                test_file_node.children.append(function_node)

    if root_node.children:
        return root_node
    else:
        return None
