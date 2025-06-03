from node import Node
import sys

class HashTreeModel:
    MAX_SIZE = 10
    current_seed = 31

    def __init__(self):
        self.parentNode = None
        self.size = 0

    def hashValue(self, value, seed):
        x = value ^ seed
        x = (x ^ (x >> 30)) * 0xbf58476d1ce4e5b9  # mix constant from SplitMix64
        x = (x ^ (x >> 27)) * 0x94d049bb133111eb
        x = x ^ (x >> 31)
        return x % self.MAX_SIZE

    def rehash(self):
        if self.parentNode is None:
            print("cant rehash i am empty")
            return
        self.MAX_SIZE *= 2
        new_seed = (self.current_seed * 2 + 1) % 400
        new_parent = Node(
            self.hashValue(self.parentNode.key, new_seed), self.parentNode.value
        )
        for key, value in self.parentNode.iterate():
            
            new_parent.addChild(Node(self.hashValue(value, new_seed), value))
        self.parentNode = new_parent
        self.current_seed = new_seed
        # print(f"Rehashed to new seed: {self.current_seed}, new max size: {self.MAX_SIZE}")

    def add(self, value):
        if self.size >= self.MAX_SIZE:
            # print("Hash table is full, rehashing...")
            self.rehash()
        if self.parentNode is None:
            self.parentNode = Node(self.hashValue(value, self.current_seed), value)
            self.size += 1
        else:
            if not self.parentNode.contains(self.hashValue(value, self.current_seed)):
                self.parentNode.addChild(
                    Node(self.hashValue(value, self.current_seed), value)
                )
                self.size += 1
            else:
                if (
                    self.parentNode.getByKey(self.hashValue(value, self.current_seed))
                    == value
                ):
                    print(
                        f"Value {value} already exists with key {self.hashValue(value, self.current_seed)}."
                    )
                    return
                self.rehash()
                self.add(value)

    def contains(self, value):
        if self.parentNode is None:
            print("bruh i am empty tf did you expect")
            return False
        return self.parentNode.contains(self.hashValue(value, self.current_seed))


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
    print("imbalance of parentNode:", hash_table.parentNode.imbalance())
