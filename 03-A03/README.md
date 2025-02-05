1. Deleting a Leaf Node (No Children)
If the node to be deleted has no children, it can simply be removed from the tree without affecting any other nodes.
2. Deleting a Node with One Child
If the node has only one child, the node is replaced by its child. This ensures the BST properties are maintained while removing the node.
3. Deleting a Node with Two Children
If the node has two children, a replacement value must be found to maintain BST properties. The commonly used approach is to replace the node with its inorder successor (the smallest node in the right subtree).
Why Choose the Inorder Successor?
The inorder successor is chosen because it is the smallest node in the right subtree, ensuring that all values in the left subtree remain smaller, and all values in the right subtree remain larger. This maintains the BST ordering property effectively.

