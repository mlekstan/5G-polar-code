import numpy as np

from decoder import Decoder
from encoder import Encoder
from load_tables import load_fixed_interleaving_pattern_table, load_polar_sequence_and_reliability_table


def bpsk(bit_seq: np.ndarray) -> np.ndarray:
    size = bit_seq.size
    bpsk_out_seq = np.zeros(size, dtype=np.int8)
    
    for i in range(size):
        bpsk_out_seq[i] = 1 if bit_seq[i] == 0 else -1
    
    return bpsk_out_seq


path_1 = "tables\\fixed_interleaving_pattern_table.txt"
path_2 = "tables\\polar_sequence_and_its_corresponding_reliability.txt"

encoder = Encoder(pi_max_il=load_fixed_interleaving_pattern_table(path_1), 
                Q=load_polar_sequence_and_reliability_table(path_2))
decoder = Decoder()

msg = np.array([1,1,1,1,1])
code_word = encoder.encode(msg)

bpsk_out = bpsk(code_word)

decoded_seq = decoder.decode(bpsk_out)


print(f"encoded: {code_word}, bpsk: {bpsk_out}, decoded: {decoded_seq}")