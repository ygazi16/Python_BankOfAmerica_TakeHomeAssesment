__all__ = ['Node', 'Trie']
import os


class Node(object):
    __slots__ = ('value', 'marks_end', 'children', 'parent')

    def __init__(self, char='', end=False, parent=None):
        self.value = char
        self.marks_end = end
        self.children = dict()
        self.parent = parent

    def add_child(self, char, end=False):
        self.children[char] = Node(char, end, self)

    def remove_child(self, char):
        del self.children[char]

    @property
    def num_children(self):
        return len(self.children)

    def is_root(self):
        return not self.parent

    def __repr__(self):
        if self.is_root():
            strings = ['Root rode']
        else:
            strings = [f'Char: {self.value}']
            strings.append(f'Parent: {self.parent.value}')
        if self.num_children > 0:
            strings.append('Children: ' + ', '.join(self.children.keys()))
        return '. '.join(strings)

    def __getitem__(self, char):
        return self.children[char]


class Trie(object):
    def __init__(self, dict_file=None):
        self._root = Node()
        self.count = 0
        if dict_file is not None:
            if not os.path.isfile(dict_file):
                raise ValueError(f"{dict_file} doesn't exist")
            lines = open(dict_file, 'r').readlines()
            words = [line.strip() for line in lines]
            for word in words:
                self.insert(word)

    def insert(self, word):
        curr = self._root
        for char in word:
            if char not in curr.children:
                curr.add_child(char)
            curr = curr[char]

        if curr.marks_end:
            print(f'{word} already exists.')
        else:
            curr.marks_end = True
            self.count += 1

    def remove(self, word):
        found, node = self._find_end_node(word)
        if found and node.marks_end:
            node.marks_end = False
            self._remove_nodes(node)
            self.count -= 1
        else:
            print(f"{word} doesn't exist")

    def has_prefix(self, prefix):
        found, _ = self._find_end_node(prefix)
        return found

    def has_word(self, word):
        found, node = self._find_end_node(word)
        return found and node.marks_end

    def get_children(self, prefix):
        found, node = self._find_end_node(prefix)
        if not found or not node:
            return []
        return list(node.children.keys())

    def words_with_prefix(self, prefix):
        found, node = self._find_end_node(prefix)
        if not found:
            print(f'Prefix {prefix} does not exist.')
            return []
        return list(self._iter(node, prefix))

    def __len__(self):
        return self.count

    def __iter__(self):
        yield from self._iter(self._root, '')

    def _iter(self, node, prefix):
        if node.marks_end:
            yield prefix
        for child in node.children:
            yield from self._iter(node[child], prefix + child)

    def _find_end_node(self, token):
        curr = self._root
        for char in token:
            if char not in curr.children:
                return False, curr
            curr = curr[char]
        return True, curr

    def _remove_nodes(self, curr):
        while curr:
            if curr.is_root or curr.num_children > 1 or curr.marks_end:
                return
            curr.parent.remove_child(curr.value)
            curr = curr.parent


def test_main():
    trie = Trie()
    trie = Trie('dictionary.txt')
    


if __name__ == '__main__':
    test_main()