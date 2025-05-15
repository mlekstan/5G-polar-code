import numpy as np
from math import log2, ceil
from load_tables import load_fixed_interleaving_pattern_table, load_polar_sequence_and_reliability_table


class Encoder:
    """
    Class representing encoder.

    ...
    Attributes
    ----------
    pi_max_il : np.ndarray
        Vector representing fixed interleaving pattern table.
    Q : np.ndarray
        Vector where indexes represent realiabilities and values represent polar sequence.

    Methods
    -------
    determine_n(K, E, n_max)
        The purpose of this function is to determine n.
    interleave(K, i_il, pi_max_il)
        Function is doing interleaving to distribute errors on the output of decoder and increase efficiency of coding.
    encode(msg)
        Function for encoding using polar code, function does not anticipate the presence of parity bits in message.
    """
    
    def __init__(self, pi_max_il: np.ndarray, Q: np.ndarray):
        """
        Parameters
        ----------
        pi_max_il : np.ndarray
            Vector representing fixed interleaving pattern table.
        Q : np.ndarray
            Vector where indexes represent realiabilities and values represent polar sequence.
        """
        
        self.pi_max_il = pi_max_il
        self.Q = Q


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
            n1 = ceil(log2(E))
        
        R_min = 1/8
        n2 = ceil(log2(K / R_min))

        n_min = 3
        n = max(min(n1, n2, n_max), n_min)

        return n
    

    def interleave(self, K: int, i_il: bool, pi_max_il: np.ndarray) -> np.ndarray:
        """
        Function is doing interleaving to distribute errors on the output of decoder and increase efficiency of coding.
        
        Parameters
        ----------
        K : int
            Number of bits in input bit sequence.
        i_il : bool
            When set to False no interleaving is occuring.
        pi_max_il : np.ndarray
            Representing fixed interleaving pattern (table) stated in 5G standard.
        
        Returns
        -------
        np.ndarray
            The created interleaving pattern.
        """

        K_max_il = pi_max_il.size     # number of entries in table of fixed interleaving pattern
        pi = np.empty(K, dtype=np.int16)

        if not i_il:
            pi = np.arange(K)
        else:
            k = 0
            for m in range(K_max_il):
                if pi_max_il[m] >= K_max_il - K:
                    pi[k] = pi_max_il[m] - (K_max_il - K)
                    k += 1

        return pi

    
    def encode(self, msg: np.ndarray) -> np.ndarray:
        """
        Function for encoding using polar code, function does not anticipate the presence of parity bits in message.

        Parameters
        ----------
        m : np.ndarray
            Message bits sequence to be encoded.
        
        Returns
        -------
        np.ndarray
            Encoded bits sequence.
        """
        
        K = msg.size
        n = self.determine_n(K=K, E=10, n_max=9)
        N = pow(2, n)
        
        # permutation_pattern = self.interleave(K=K, i_il=False, pi_max_il=self.pi_max_il)
        Q = self.Q[self.Q < N]
        frozen_bits_idxes = Q[:N-K]
        message_bits_idxes = Q[N-K:]
        u = np.zeros(N, dtype=np.int8)
        u[message_bits_idxes] = msg

        k = 1
        while k < N:
            for i in range(0, N, 2*k):
                u[i:i+k] = np.mod(u[i:i+k] + u[i+k:i+2*k], 2)
            k *= 2
    
        return u


if __name__ == "__main__":

    path_1 = "tables\\fixed_interleaving_pattern_table.txt"
    path_2 = "tables\\polar_sequence_and_its_corresponding_reliability.txt"

    encoder = Encoder(pi_max_il=load_fixed_interleaving_pattern_table(path_1), 
                    Q=load_polar_sequence_and_reliability_table(path_2))

    message = np.array([1,0,1,1]) # np.random.randint(0, 2, 10, dtype=np.int8)

    print(encoder.encode(msg=message))