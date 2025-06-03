"""binary tree with hashes as keys for automatic balance"""
import sys
from node import Node

class HashTreeModel:
    """binary tree with hashes as keys for automatic balance"""
    max_size = 10
    current_seed = 31

    def __init__(self):
        self.parent_node = None
        self.size = 0

    def hash_value(self, value, seed):
        """hashes value using a random hash function i stole somewhere"""
        x = value ^ seed
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9  # mix constant from SplitMix64
        x = (x ^ (x >> 27)) * 0x94d049bb133111eb
        x = x ^ (x >> 31)
        return x % self.max_size

    def rehash(self):
        """rehashes the tree using a new seed and doubles the max size"""
        if self.parent_node is None:
            print("cant rehash i am empty")
            return
        self.max_size *= 2
        new_seed = (self.current_seed * 2 + 1) % 400
        new_parent = Node(
            self.hash_value(self.parent_node.key, new_seed), self.parent_node.value
        )
        for _, value in self.parent_node.iterate():
            new_parent.add_child(Node(self.hash_value(value, new_seed), value))
        self.parent_node = new_parent
        self.current_seed = new_seed
        # print(f"Rehashed to new seed: {self.current_seed}, new max size: {self.MAX_SIZE}")

    def add(self, value):
        """adds a value to the tree"""
        if self.size >= self.max_size:
            # print("Hash table is full, rehashing...")
            self.rehash()
        if self.parent_node is None:
            self.parent_node = Node(self.hash_value(value, self.current_seed), value)
            self.size += 1
        else:
            if not self.parent_node.contains(self.hash_value(value, self.current_seed)):
                self.parent_node.add_child(
                    Node(self.hash_value(value, self.current_seed), value)
                )
                self.size += 1
            else:
                if (
                    self.parent_node.get_by_key(self.hash_value(value, self.current_seed))
                    == value
                ):
                    print(
                        f"""Value {value}
                        already exists with key
                        {self.hash_value(value, self.current_seed)}."""
                    )
                    return
                self.rehash()
                #TODO remove recursion
                self.add(value)

    def contains(self, value):
        """checks if the value already exists in the tree"""
        if self.parent_node is None:
            print("bruh i am empty tf did you expect")
            return False
        return self.parent_node.contains(self.hash_value(value, self.current_seed))


if __name__ == "__main__":
    sys.setrecursionlimit(10)
    hash_table = HashTreeModel()
    for i in range(0, 200000):
        hash_table.add(i)
    errors = []
    for i in range(0, 200000):
        if not hash_table.contains(i):
            errors.append(i)
    print("Errors found:", errors)
    print("imbalance of parentNode:", hash_table.parent_node.imbalance())
