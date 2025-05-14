from math import log2, copysign
import numpy as np

class Decoder(object):
    """
    Class representing basic SC (Successive Cancelation) decoder.

    ...
    Attributes
    ----------


    Methods
    -------
    decode()
        Method for decoding code words.
    """
    
    def __init__():
        pass
    


    def decode(r: np.ndarray) -> np.ndarray:
        """
        Function for decoding code word (polar code).
        
        Paramenters
        -----------
        r : np.ndarray
            Encoded message (code word)
        
        Returns
        -------
        np.ndarray

        """



        # the node of decoding binary tree
        class TreeNode(object):
            def __init__(self, L: np.ndarray, left_child=None, right_child=None):
                self.left_child = left_child
                self.right_child = right_child
                self.L = L

            def f(self, L: np.ndarray):
                sgn = lambda x: copysign(1, x)
                new_L = np.empty(L.size/2, dtype=np.int8)

                i = 0
                for beliefs in zip(L[:L.size/2], L[L.size/2:]):
                    belief = sgn(beliefs[0]) * sgn(beliefs[1]) * min(abs(beliefs[0]), abs(beliefs[1]))
                    new_L[i] = belief
                    i += 1

                return new_L

            def g(self, L: np.ndarray, c: np.ndarray):
                new_L = np.empty(L.size/2, dtype=np.int8)

                i = 0
                for beliefs in zip(L[:L.size/2], L[L.size/2:]):
                    belief = beliefs[1] + beliefs[0] if c[i] == 0 else beliefs[1] - beliefs[0]
                    new_L[i] = belief
                    i += 1

                return new_L
        

        def createDecodingTree(root: TreeNode, depth: int) -> TreeNode:
            if depth == 0:
                return root

            root.left_child = TreeNode()
            root.right_child = TreeNode()
            depth -= 1

            createDecodingTree(root.left_child, depth)
            createDecodingTree(root.right_child, depth)

            return root
        
        
        root = TreeNode(L=r)
        createDecodingTree(root=root, depth=log2(r.size))

