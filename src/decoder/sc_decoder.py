from math import log2
from typing import Tuple
import numpy as np
from numpy.typing import NDArray
from sc_decoding_tree import DecodingTreeNode


class Decoder(object):
    """
    Class representing basic SC (Successive Cancelation) decoder.

    ...
    Attributes
    ----------
    Q : NDArray[np.uint16]
        Vector where indexes represent realiabilities and values represent polar sequence.

    Methods
    -------
    decode()
        Method for decoding code words.
    """

    def __init__(self, Q: NDArray[np.uint16]):
        """
        Parameters
        ----------
        Q : NDArray[np.uint16]
            Vector where indexes represent realiabilities and values represent polar sequence.
        """
        self.Q = Q

    @staticmethod
    def createDecodingTree(root: DecodingTreeNode, depth: int) -> DecodingTreeNode:
        """"""
        if depth == 0:
            return root

        root.left_child = DecodingTreeNode()
        root.right_child = DecodingTreeNode()
        depth -= 1

        Decoder.createDecodingTree(root.left_child, depth)
        Decoder.createDecodingTree(root.right_child, depth)

        return root
    
    @staticmethod
    def combine(v1: NDArray[np.uint8], v2: NDArray[np.uint8]) -> NDArray[np.uint8]:
        """"""
        sum_mod2 = np.mod(v1 + v2, 2).astype(np.uint8)
        v2_uint8 = v2.astype(np.uint8)
        
        return np.concatenate([sum_mod2, v2_uint8])
    
    

    def decode(self, r: NDArray[np.float64], K: int) -> Tuple[NDArray[np.uint8], NDArray[np.uint8]]:
        """
        Function for decoding code word (polar code).
        
        Parameters
        ----------
        r : NDArray[np.float64]
            Encoded message (code word) after modulation (and channel influence).
        K : int
            Number of information bits.
        
        Returns
        -------
        NDArray[np.uint8]
            Decoded bit sequence.

        """

        N = r.size
        Q = self.Q[self.Q < N]
        frozen_bits_idxes = Q[:N-K]
        message_bits_idxes = Q[N-K:]

        def decodingTreeTraverse(root: DecodingTreeNode, L: NDArray[np.float64], bit_idx: int) -> Tuple[NDArray[np.uint8], NDArray[np.uint8], int]:
            """"""
            if root.left_child is None and root.right_child is None:
                if bit_idx in frozen_bits_idxes:
                    u = 0
                else:
                    u = 0 if L[0] >= 0 else 1
                
                return np.array([u]), np.array([u]), bit_idx + 1
            
            assert root.left_child and root.right_child
            
            left_L = root.f(L)
            u1, v1, bit_idx = decodingTreeTraverse(root.left_child, left_L, bit_idx)
            right_L = root.g(L, u1)
            u2, v2, bit_idx = decodingTreeTraverse(root.right_child, right_L, bit_idx)

            return Decoder.combine(u1, u2), np.concatenate([v1, v2]), bit_idx

        
        root = Decoder.createDecodingTree(root=DecodingTreeNode(), depth=int(log2(r.size)))
        recreated_r, decoded_seq, _ = decodingTreeTraverse(root, r, 0)
        
        return recreated_r, decoded_seq[message_bits_idxes]