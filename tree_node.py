from textwrap import indent as textwrap_indent
from typing import List, Optional


class TreeNode:
    def __init__(
        self,
        name: str,
        contents: Optional[str] = None,
        children: Optional[List["TreeNode"]] = None,
        parent: Optional["TreeNode"] = None,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
    ):
        self.name = name
        self.contents = contents
        self.children = children or []
        self.parent = parent
        self.start_line = start_line
        self.end_line = end_line

    def __repr__(self, indent=0):
        lines = [f"{' ' * indent}└── {self.name}"]
        if self.contents:
            indented_contents = textwrap_indent(self.contents, " " * (indent + 4))
            lines.append(indented_contents)
        for child in self.children:
            lines.extend(child.__repr__(indent + 2).splitlines())
        return "\n".join(lines)

    def __getitem__(self, ind: int):
        return self.children[ind]
