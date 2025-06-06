"""binary tree node implementation"""
class Node:
    """node in binary tree with keyvalue pair"""
    child_left = None
    child_right = None

    def __init__(self, key: int, value):
        self.key = key
        self.value = value
        self.next = None

    def add_child(self, node):
        """adds a child node according to key"""
        if self.key == node.key:
            print(f"Trying to add {node}, but {self} exists")
            return
        current = self
        while current is not None:
            if node.key < current.key:
                if current.child_left is None:
                    current.child_left = node
                    return
                else:
                    current = current.child_left
            else:
                if current.child_right is None:
                    current.child_right = node
                    return
                else:
                    current = current.child_right

    def contains(self, key):
        """checks if any connected node or self contains key"""
        if self.key == key:
            return True
        current = self
        while current is not None:
            if key < current.key:
                current = current.child_left
            elif key > current.key:
                current = current.child_right
            else:
                return True
        return False

    def iterate(self):
        """returns a generator yielding all key-value pairs of the node and children"""
        nodes_to_visit = [self]
        while nodes_to_visit:
            current = nodes_to_visit.pop()
            yield current.key, current.value
            if current.child_left is not None:
                nodes_to_visit.append(current.child_left)
            if current.child_right is not None:
                nodes_to_visit.append(current.child_right)

    def __str__(self):
        return f"Node(value={self.value}, key={self.key})"

    def imbalance(self):
        """calculates the difference between the amount of left and right nodes"""
        nodes_to_visit = [self]
        derivation = 0
        while nodes_to_visit:
            current = nodes_to_visit.pop()
            if current.child_left is not None:
                nodes_to_visit.append(current.child_left)
                derivation += 1
            if current.child_right is not None:
                nodes_to_visit.append(current.child_right)
                derivation -= 1
        return derivation

    def get_by_key(self, key):
        """returns the value of the node by given key or None if not found"""
        if self.key == key:
            return self.value
        current = self
        while current is not None:
            if key < current.key:
                current = current.child_left
            elif key > current.key:
                current = current.child_right
            else:
                return current.value
