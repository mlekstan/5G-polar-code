from math import copysign
import numpy as np
from numpy.typing import NDArray

class DecodingTreeNode(object):
    def __init__(self, left_child: "DecodingTreeNode | None" = None, right_child: "DecodingTreeNode | None" = None):
        self.left_child = left_child
        self.right_child = right_child

    def f(self, L: NDArray[np.float64]) -> NDArray[np.float64]:
        sgn = lambda x: copysign(1, x) # signum function
        new_L = np.zeros(L.size//2, dtype=L.dtype)

        i = 0
        for beliefs in zip(L[:L.size//2], L[L.size//2:]): 
            belief = sgn(beliefs[0]) * sgn(beliefs[1]) * min(abs(beliefs[0]), abs(beliefs[1])) 
            new_L[i] = belief
            i += 1
        
        return new_L 

    def g(self, L: NDArray[np.float64], c: NDArray[np.uint8]) -> NDArray[np.float64]:
        new_L = np.zeros(L.size//2, dtype=L.dtype)

        i = 0
        for beliefs in zip(L[:L.size//2], L[L.size//2:]):
            belief = beliefs[1] + beliefs[0] if c[i] == 0 else beliefs[1] - beliefs[0]
            new_L[i] = belief
            i += 1

        return new_L