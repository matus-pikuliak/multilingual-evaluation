
"""
CREATE HIERARCHY
"""


class Node:

    nodes = list()

    def __init__(self, name, parent, depth):
        self.parent = parent
        if self.parent:
            self.parent.children.append(self)
        self.children = []
        self.name = name
        self.depth = depth
        Node.nodes.append(self)

    def __repr__(self):
        return self.name

    def relevant_languages(self):
        return set().union(
            *(
                child.relevant_languages()
                for child
                in self.children
            )
        )

    def parents(self):
        if not self.parent:
            return []
        else:
            return [self.parent] + self.parent.parents()

    @classmethod
    def depth(cls, line):
        return line.count('\t') + 1

    @classmethod
    def find_by_abbrv(cls, abbrv):
        for node in cls.nodes:
            if isinstance(node, Language) and node.abbreviation == abbrv:
                return node
        return None


class Language(Node):

    def __init__(self, abbreviation, *args):
        Node.__init__(self, *args)
        self.abbreviation = abbreviation
        self.depth -= 1

    def relevant_languages(self):
        return {self.abbreviation}

    def belongs_to(self, families):
        return bool(
            families.intersection(
                set(node.name for node in self.parents())
            )
        )



hierarchy = [line.rstrip() for line in open('languages.txt', encoding='utf-8')]
root = Node('All languages', None, 0)
stack = [root]

for i, record in enumerate(hierarchy):

    depth = Node.depth(record)
    while stack[-1].depth >= depth:
        stack.pop()

    if i + 1 == len(hierarchy) or depth >= Node.depth(hierarchy[i+1]):
        # language
        abbreviation, name = record.strip().split(maxsplit=1)
        Language(abbreviation, name, stack[-1], depth)
    else:
        # family
        name = record.strip()
        stack.append(
            Node(name, stack[-1], depth)
        )

nodes = {
    node.name: node
    for node
    in Node.nodes
}