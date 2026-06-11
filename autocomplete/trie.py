class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word:str):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, prefix:str):
        self.results = []
        current = self.root

        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]
        self._collect(current, prefix, self.results)
        return self.results

    def _collect(self, node, prefix, results:list):
        if node.is_end:
            results.append(prefix)
        for char, child_node in node.children.items():
            self._collect(child_node, prefix + char, results)
            node = child_node
        return results
    
trie = Trie()
trie.insert("Liverpool")
trie.insert("Liver")
print(trie.search("Liv"))