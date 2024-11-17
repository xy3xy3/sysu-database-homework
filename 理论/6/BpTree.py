class BPlusTreeNode:
    def __init__(self, order, leaf=False):
        self.order = order  # 阶数
        self.leaf = leaf    # 是否为叶子节点
        self.keys = []      # 键列表
        self.children = []  # 子节点列表（对于内部节点）
        self.next = None    # 叶子节点的下一个节点（仅叶子节点使用）

    def is_full(self):
        return len(self.keys) >= self.order - 1

class BPlusTree:
    def __init__(self, order):
        self.order = order
        self.root = BPlusTreeNode(order, leaf=True)

    def find_leaf(self, key, verbose=False):
        current = self.root
        while not current.leaf:
            if verbose:
                print(f"Traversing node with keys: {current.keys}")
            i = 0
            while i < len(current.keys) and key >= current.keys[i]:
                i += 1
            current = current.children[i]
        if verbose:
            print(f"Leaf node found with keys: {current.keys}")
        return current

    def insert(self, key):
        root = self.root
        if root.is_full():
            new_root = BPlusTreeNode(self.order)
            new_root.children.append(self.root)
            self.split_child(new_root, 0)
            self.root = new_root
            print(f"Root was split. New root keys: {self.root.keys}")
        self._insert_non_full(self.root, key)

    def _insert_non_full(self, node, key):
        if node.leaf:
            self.insert_in_leaf(node, key)
        else:
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            child = node.children[i]
            if child.is_full():
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key)

    def insert_in_leaf(self, leaf, key):
        leaf.keys.append(key)
        leaf.keys.sort()
        print(f"Inserted {key} into leaf: {leaf.keys}")

    def split_child(self, parent, index):
        node = parent.children[index]
        mid = self.order // 2
        split_key = node.keys[mid]

        if node.leaf:
            # 分裂叶子节点
            new_node = BPlusTreeNode(self.order, leaf=True)
            new_node.keys = node.keys[mid:]
            node.keys = node.keys[:mid]
            new_node.next = node.next
            node.next = new_node

            parent.keys.insert(index, new_node.keys[0])
            parent.children.insert(index + 1, new_node)
            print(f"Split leaf node. Parent keys now: {parent.keys}")
        else:
            # 分裂内部节点
            new_node = BPlusTreeNode(self.order, leaf=False)
            new_node.keys = node.keys[mid + 1:]
            new_node.children = node.children[mid + 1:]
            node.keys = node.keys[:mid]
            node.children = node.children[:mid + 1]

            parent.keys.insert(index, split_key)  # 修正这里的错误
            parent.children.insert(index + 1, new_node)
            print(f"Split internal node. Parent keys now: {parent.keys}")

    def print_tree(self):
        levels = []
        self._collect_levels(self.root, 0, levels)
        for i, level in enumerate(levels):
            level_keys = " | ".join(str(node.keys) for node in level)
            print(f"Level {i}: {level_keys}")

    def _collect_levels(self, node, level, levels):
        if len(levels) <= level:
            levels.append([])
        levels[level].append(node)
        if not node.leaf:
            for child in node.children:
                self._collect_levels(child, level + 1, levels)

    def search(self, key):
        leaf = self.find_leaf(key)
        for item in leaf.keys:
            if item == key:
                return True
        return False

    def range_search(self, start, end):
        results = []
        leaf = self.find_leaf(start)
        while leaf:
            for key in leaf.keys:
                if start <= key <= end:
                    results.append(key)
                elif key > end:
                    return results
            leaf = leaf.next
        return results

if __name__ == "__main__":
    keys = [2, 3, 5, 7, 11, 17, 19, 23, 29, 31]

    orders = [4, 6, 8]

    for order in orders:
        print(f"\n构建B+树，阶数 = {order}:")
        tree = BPlusTree(order=order)
        for key in keys:
            tree.insert(key)
            print(f"插入 {key}:")
            tree.print_tree()
            print("-" * 40)
        print("最终B+树结构:")
        tree.print_tree()
        print("=" * 60)
