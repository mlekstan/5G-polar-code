import sys
sys.path.append("e:\\Studia_Teleinformatyka_2022_2023\\VI_semestr\\KiK\\5G-polar-code\\decoder\\")

from math import sqrt
from types import FunctionType, MethodType
import numpy as np
from numpy.typing import NDArray

from encoder import Encoder
from modulator import Modulator
from decoder import Decoder

from load_tables import load_fixed_interleaving_pattern_table, load_polar_sequence_and_reliability_table


class Channel(object):
    """
    Class that is representation of the channel.

    Attributes
    ----------
    noise_type : str
        Type of noise in channel.
    
    Methods
    -------
    gwn()
        Function returns samples of gaussian white noise.
    """

    def __init__(self, noise_type: str):
        self.noise_type = noise_type


    def gwn(self, EbN0dB: float, K: int, N: int) -> NDArray[np.float64]:
        N0Eb = 10 ** (-EbN0dB/10)
        std_dev = sqrt(0.5 * N/K * N0Eb)
        
        return np.random.randn(N) * std_dev


    def send_through(self, mod_seq: NDArray[np.int8], EbN0dB: float, K: int) -> NDArray[np.float64]:
        N = mod_seq.size
        noise_method = getattr(self, self.noise_type)
        #if isinstance(noise_method, (FunctionType, MethodType)):
        return mod_seq + noise_method(EbN0dB, K, N)
    


if __name__ == "__main__":

    path_1 = "tables\\fixed_interleaving_pattern_table.txt"
    path_2 = "tables\\polar_sequence_and_its_corresponding_reliability.txt"

    pi_max_il=load_fixed_interleaving_pattern_table(path_1)
    Q=load_polar_sequence_and_reliability_table(path_2)

    ### create actors
    encoder = Encoder(pi_max_il, Q)
    modulator = Modulator()
    channel = Channel("gwn")
    decoder = Decoder(Q)
    ###


    ### transmit
    msg = np.random.randint(low=0, high=2, size=15, dtype=np.uint8)
    #msg = np.array([0,1,0,1,1,0], dtype=np.uint8)
    K = msg.size
    
    code_word = encoder.encode(msg)

    bpsk_out = modulator.bpsk(code_word)

    channel_out = channel.send_through(mod_seq=bpsk_out, EbN0dB=9, K=K)
    #channel_out = bpsk_out

    recreated_encoded, decoded_seq = decoder.decode(r=channel_out, K=K)
    ###


    print(f"input_bits: {msg}\nencoded: {code_word}\nbpsk: {bpsk_out}\nchannel_out: {channel_out}\nrecreated_encoded: {recreated_encoded}\ndecoded: {decoded_seq}") # results