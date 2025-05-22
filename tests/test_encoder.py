import unittest     # https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug
import sys
sys.path.append("e:\\Studia_Teleinformatyka_2022_2023\\VI_semestr\\KiK\\5G-polar-code\\")

import numpy as np
from numpy.typing import NDArray
from numpy.testing import assert_array_equal
from encoder import Encoder
from load_tables import load_fixed_interleaving_pattern_table, load_polar_sequence_and_reliability_table



def stndard_encoding(msg: NDArray[np.uint8], encoder: Encoder) -> NDArray[np.uint8]:
    """
    Function that impelemnts polar encoding directly according to 5G standard.

    Parameters
    ----------
    msg : NDArray[np.uint8]
        Message bits sequence to be encoded.
    encoder : encoder.Encoder
        Encoder object
    
    Returns
    -------
    NDArray[np.uint8]
        Encoded bits sequence.
    """

    K = msg.size
    n = encoder.determine_n(K=K, E=10, n_max=9)
    N = pow(2, n)
    
    # permutation_pattern = self.interleave(K=K, i_il=False, pi_max_il=self.pi_max_il)
    Q = encoder.Q[encoder.Q < N]
    message_bits_idxes = Q[N-K:]
    u = np.zeros(N, dtype=np.int8)
    u[message_bits_idxes] = msg

    
    G2 = np.array([[1,0], [1,1]])           # base kernel
    Gn = G2
    
    for _ in range(n-1):
        Gn = np.kron(G2, Gn)                # calculating generator matrix Gn

    d = np.mod(u @ Gn, 2)                   # encoded message (code word)
    
    return d




def suite() -> unittest.TestSuite:
    suite = unittest.TestSuite()
    suite.addTest(TestEncoder("test_encode"))
    return suite


class TestEncoder(unittest.TestCase):
    
    def setUp(self):
        super(TestEncoder, self).setUp()
        
        path_1 = "tables\\fixed_interleaving_pattern_table.txt"
        path_2 = "tables\\polar_sequence_and_its_corresponding_reliability.txt"
        
        self.encoder = Encoder(
                pi_max_il=load_fixed_interleaving_pattern_table(path_1), 
                Q=load_polar_sequence_and_reliability_table(path_2)
            )
        
        self.msg_samples = [ np.random.randint(low=0, high=2, size=np.random.randint(low=5, high=30)) for _ in range(1000) ] 

    
    def test_encode(self):
        for msg in self.msg_samples:
            with self.subTest(msg=msg):
                assert_array_equal(self.encoder.encode(msg), stndard_encoding(msg, self.encoder))



if __name__ == "__main__":
    # unittest.main()
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite())