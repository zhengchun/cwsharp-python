import struct


class Dawg:
    def __init__(self):
        self.version = 1.0
        self.root = None

    def contains(self, word=None):
        if word is None or word == "":
            return False

        nextNode = self.root.next(word[0])
        for i in range(1, len(word)):
            if nextNode is None:
                break
            nextNode = nextNode.next(word[i])

        return nextNode is not None and nextNode.eow

    def load(self, f=None):
        self.version = struct.unpack("<f", f.read(4))[0]
        count = struct.unpack("<i", f.read(4))[0]
        nodes = [None] * count
        for i in range(count):
            node = Node()
            node.char = unichr(struct.unpack("<H", f.read(2))[0])
            node.freq = struct.unpack("<i", f.read(4))[0]
            node.depth = struct.unpack("<i", f.read(4))[0]
            if (struct.unpack("<b", f.read(1))[0]) == 1:
                node.eow = True
            struct.unpack("<i", f.read(4))
            nodes[i] = node

        # build a dawg.
        count = struct.unpack("<i", f.read(4))[0]
        root = Node()
        for i in range(count):
            j = struct.unpack("<i", f.read(4))[0]
            root.addChild(nodes[j])

        count = struct.unpack("<i", f.read(4))[0]
        for i in range(count):
            label = struct.unpack("<i", f.read(4))[0]
            node = nodes[label]
            childNodeCount = struct.unpack("<i", f.read(4))[0]
            for j in range(childNodeCount):
                label = struct.unpack("<i", f.read(4))[0]
                node.addChild(nodes[label])
        self.root = root


    def save(self, f=None):
        count = 0
        nodeLabels = dict()
        stack = []
        self.root.get_descendants(stack, False)
        print(len(stack))
        for node in stack:
            if nodeLabels.get(node) is not None:
                continue
            nodeLabels[node] = count
            count += 1
        f.write(struct.pack("<f", self.version))
        f.write(struct.pack("<i", count))
        count = 0
        for node in nodeLabels.iterkeys():           
            f.write(struct.pack("<H", ord(node.char)))
            f.write(struct.pack("<i", node.freq))
            f.write(struct.pack("<i", node.depth))
            if node.eow is True:
                f.write(struct.pack("<b", 1))
            else:
                f.write(struct.pack("<b", 0))
            f.write(struct.pack("<i", len(node.childs)))
            if node.hasChilds() is True:
                count += 1

        f.write(struct.pack("<i", len(self.root.childs)))
        for node in self.root.childs.values():
            label = nodeLabels[node]
            f.write(struct.pack("<i", label))
        f.write(struct.pack("<i", count))
        for node, label in nodeLabels.iteritems():
            if node.hasChilds() is False:
                continue
            f.write(struct.pack("<i", label))
            f.write(struct.pack("<i", len(node.childs)))
            for sub_node in node.childs.values():
                f.write(struct.pack("<i", nodeLabels[sub_node]))


class Node:
    def __init__(self):
        self.char = None
        self.childs = dict()
        self.depth = 0
        self.freq = 0
        self.eow = False
        self.parent = None

    def addChild(self, node):
        if node.char in self.childs:
            return
        if node.parent is None:
            node.parent = self
        self.childs[node.char] = node

    def removeChild(self, node):
        if node.char not in self.childs:
            return
        del self.childs[node.char]

    def next(self, char):
        return self.childs.get(char)

    def hasChilds(self):
        return len(self.childs)

    def get_descendants(self, stack=None, include_self=False):
        if include_self:
            stack.append(self)
        for node in self.childs.values():
            stack.append(node)
            node.get_descendants(stack, False)


def load(file_name):
    dawg = Dawg()
    with open(file_name, "rb") as f:
        dawg.load(f)
    return dawg