import numpy as np
from math import log2, ceil
from load_tables import load_fixed_interleaving_pattern_table


class Encoder:
    def __init__(self):
        pass


    def determine_n(self, K: int, E, n_max: int) -> int:
        """ 
        The bit sequence input for a given code block to channel coding is denoted by c[0], c[1], c[2], c[3], ..., c[K-1] where K is the
        number of bits to encode. After encoding the bits are denoted by d[0], d[1], d[2], ..., d[N-1], where N = 2^n and the purpose of 
        this function is to determine n.

        Parameters
        ----------
        K : int
            Number of bits in input bit sequence.
        E : 
            Rate matching output length. It is stated by the higher layers (MAC, scheduler) before channel encoding - in the transmission planning phase.
        n_max : int
            In polar encoding is the maximum exponent of 2 for the encoded block length N. It limits how large a single block can be. In 5G NR for user data: n_max = 11, for control info: n_max = 9.

        Returns
        -------
        int
            The predcited n.
        """
        
        if ( E <= (9/8) * pow(2, ceil(log2(E))-1) ) and ( (K / E) < 9/16 ):
            n1 = ceil(log2(E)) - 1
        else:
            n1 = log2(E)
        
        R_min = 1/8
        n2 = ceil(log2(K / R_min))

        n_min = 5
        n = max(min(n1, n2, n_max), n_min)

        return n
    

    def interleave(self, K: int, do_interleaving: bool, fixed_interleaving_pattern: np.ndarray) -> np.ndarray:
        """
        Function is doing interleaving to distribute errors on the output of decoder and increase efficiency of coding.
        
        Parameters
        ----------
        K : int
            Number of bits in input bit sequence.
        do_interleaving : bool
            When set to False no interleaving is occuring.
        param fixed_interleaving_pattern : np.ndarray
            Representing fixed interleaving pattern (table) stated in 5G standard.
        
        Returns
        -------
        np.ndarray
            The created interleaving pattern.
        """

        K_max = fixed_interleaving_pattern.size     # number of entries in table of fixed interleaving pattern
        interleaving_pattern = np.empty(K, dtype=np.int16)

        if not do_interleaving:
            interleaving_pattern = np.arange(K)
        else:
            k = 0
            for m in range(K_max):
                if fixed_interleaving_pattern[m] >= K_max - K:
                    interleaving_pattern[k] = fixed_interleaving_pattern[m] - (K_max - K)
                    k += 1

        return interleaving_pattern

    
    def encode(self, input_bit_sequence: np.ndarray) -> np.ndarray:
        """
        Function for encoding.

        Parameters
        ----------
        input_bit_sequence : np.ndarray
            Bits sequence to be encoded.
        
        Returns
        -------
        np.ndarray
            Encoded bits sequence.
        """







input_bit_seq = np.random.randint(0, 2, 100, dtype=np.int8)