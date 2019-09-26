# Python program to introduce Binary Tree

# A class that represents an individual node in a
# Binary Tree
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key


# A function to do inorder tree traversal
# def printInorder(root):
#     if root:
#         # First recur on left child
#         printInorder(root.left)
#
#         # then print the data of node
#         print(root.val),
#
#         # now recur on right child
#         printInorder(root.right)

#root left right
def printPreorder(root, number):
    if root:
        check = "not null"
    else:
        check = "null"
    print("{0} - {1}".format(number, check))

    number = number+1
    if root:
        print("ignore ", root.val)

        printPreorder(root.left, number)

        printPreorder(root.right, number)



# Driver code
number = 0
root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)
"""
                            1
                          /   \
                        2      3
                      /  \
                     4    5      
                     

Inorder  : 4 2 5 1 3  (left - root - right)
Preorder : 1 2 4 5 3  (root - left - right)
"""



print("Preorder traversal of binary tree is")
printPreorder(root, number)

print("Inorder traversal of binary tree is")
#printInorder(root)

print("Postorder traversal of binary tree is")
#printPostorder(root)
