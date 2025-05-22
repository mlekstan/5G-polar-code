import numpy as np
from numpy.typing import NDArray

class Modulator(object):
    """
    Class representing modualtor.

    Attributes
    ----------

    Methods
    -------
    bpsk(bit_seq)
        The purpose of this method is to modulate bit sequence using BPSK.
    """
    
    def __init__(self):
        pass

    def bpsk(self, bit_seq: NDArray[np.uint8]) -> NDArray[np.int8]:
        """
        Performs BPSK modulation.

        Parameters
        ----------
        bit_seq : NDArray[np.uint8]
            Input bit seqence.

        Returns
        -------
        bpsk_out_seq : NDArray[np.int8]
            Seqence after BPSK modulation (channel input signal)
        """
        
        size = bit_seq.size
        bpsk_out_seq = np.zeros(size, dtype=np.int8)
        
        for i in range(size):
            bpsk_out_seq[i] = 1 if bit_seq[i] == 0 else -1
        
        return bpsk_out_seq