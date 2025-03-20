import random
import matplotlib.pyplot as plt
import numpy as np

# TreeNode structure
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

# Binary Search Tree Implementation
class BST:
    def __init__(self):
        self.root = None
        self.use_successor = True  # Track whether to use successor or predecessor in symmetric deletion

    def insert(self, val):
        self.root = self._insert(self.root, val)

    def _insert(self, node, val):
        if node is None:
            return TreeNode(val)
        if val < node.val:
            node.left = self._insert(node.left, val)
        else:
            node.right = self._insert(node.right, val)
        return node

    def find_successor(self, node):
        current = node.right
        while current and current.left:
            current = current.left
        return current

    def find_predecessor(self, node):
        current = node.left
        while current and current.right:
            current = current.right
        return current

    def asymmetric_delete(self, val):
        self.root = self._asymmetric_delete(self.root, val)

    def _asymmetric_delete(self, node, val):
        if not node:
            return None
        if val < node.val:
            node.left = self._asymmetric_delete(node.left, val)
        elif val > node.val:
            node.right = self._asymmetric_delete(node.right, val)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            successor = self.find_successor(node)
            node.val = successor.val
            node.right = self._asymmetric_delete(node.right, successor.val)
        return node

    def symmetric_delete(self, val):
        self.root = self._symmetric_delete(self.root, val, self.use_successor)
        self.use_successor = not self.use_successor  # Toggle for next deletion

    def _symmetric_delete(self, node, val, use_successor):
        if not node:
            return None
        if val < node.val:
            node.left = self._symmetric_delete(node.left, val, use_successor)
        elif val > node.val:
            node.right = self._symmetric_delete(node.right, val, use_successor)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            if use_successor:
                replacement = self.find_successor(node)
                node.right = self._symmetric_delete(node.right, replacement.val, not use_successor)
            else:
                replacement = self.find_predecessor(node)
                node.left = self._symmetric_delete(node.left, replacement.val, not use_successor)
            node.val = replacement.val
        return node

    def compute_ipl(self):
        return self._compute_ipl(self.root, 0)

    def _compute_ipl(self, node, depth):
        if not node:
            return 0
        return depth + self._compute_ipl(node.left, depth + 1) + self._compute_ipl(node.right, depth + 1)

# Expected IPL for a random BST of size n
def expected_ipl(n):
    return 1.386 * n * np.log2(n) - 2.846 * n

# Run experiment and collect normalized IPL data
def run_experiment(tree_size, num_trials):
    num_id_pairs = tree_size * 100  # Set I/D pairs to n^2
    asymmetric_results = []
    symmetric_results = []

    for _ in range(num_trials):
        bst_asym = BST()
        bst_sym = BST()
        values = random.sample(range(10000), tree_size)
        for val in values:
            bst_asym.insert(val)
            bst_sym.insert(val)

        norm_ipl_asym = [bst_asym.compute_ipl() / expected_ipl(tree_size)]
        norm_ipl_sym = [bst_sym.compute_ipl() / expected_ipl(tree_size)]

        for _ in range(num_id_pairs):
            del_val = random.choice(values)
            values.remove(del_val)

            bst_asym.asymmetric_delete(del_val)
            bst_sym.symmetric_delete(del_val)

            new_val = random.randint(10000, 20000)
            values.append(new_val)
            bst_asym.insert(new_val)
            bst_sym.insert(new_val)

            norm_ipl_asym.append(bst_asym.compute_ipl() / expected_ipl(tree_size))
            norm_ipl_sym.append(bst_sym.compute_ipl() / expected_ipl(tree_size))

        asymmetric_results.append(norm_ipl_asym)
        symmetric_results.append(norm_ipl_sym)

    return asymmetric_results, symmetric_results, num_id_pairs

# Experiment setup
tree_sizes = [64, 128, 256, 512, 1024, 2048]
num_trials = 2

fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 10))  # Subplots for each tree size
fig.suptitle("IPL Trends in BST Deletion Strategies (n^2 I/D Pairs)", fontsize=16)

# Run experiment and plot for each tree size
for i, size in enumerate(tree_sizes):
    asym_results, sym_results, num_id_pairs = run_experiment(size, num_trials)

    # Compute mean IPL trends across trials
    asym_avg = [sum(x) / num_trials for x in zip(*asym_results)]
    sym_avg = [sum(x) / num_trials for x in zip(*sym_results)]
    
    # Get corresponding subplot
    ax = axes[i // 3, i % 3]  # 2x3 grid placement

    # Plot individual tree size trends
    ax.plot(range(num_id_pairs + 1), asym_avg, label=f"Asymmetric {size}", color='red')
    ax.plot(range(num_id_pairs + 1), sym_avg, label=f"Symmetric {size}", linestyle="dashed", color='blue')
    ax.axhline(y=1, color='black', linestyle="dotted", label="Threshold IPL = 1")  # Mark threshold

    ax.set_xlabel("Number of I/D Pairs")
    ax.set_ylabel("Normalized IPL")
    ax.set_title(f"Tree Size: {size}")
    ax.legend()

# Comparison Plot
fig, ax_compare = plt.subplots(figsize=(10, 6))

for size in tree_sizes:
    asym_results, sym_results, num_id_pairs = run_experiment(size, num_trials)

    asym_avg = [sum(x) / num_trials for x in zip(*asym_results)]
    sym_avg = [sum(x) / num_trials for x in zip(*sym_results)]
    
    ax_compare.plot(range(num_id_pairs + 1), asym_avg, label=f"Asymmetric {size}")
    ax_compare.plot(range(num_id_pairs + 1), sym_avg, linestyle="dashed", label=f"Symmetric {size}")

ax_compare.axhline(y=1, color='black', linestyle="dotted", label="Threshold IPL = 1")
ax_compare.set_xlabel("Number of I/D Pairs")
ax_compare.set_ylabel("Normalized IPL")
ax_compare.set_title("Comparison of IPL Across Different Tree Sizes")
ax_compare.legend()

plt.show()
