from typing import List
import sys
sys.path.append("e:\\Studia_Teleinformatyka_2022_2023\\VI_semestr\\KiK\\5G-polar-code\\")
sys.path.append("e:\\Studia_Teleinformatyka_2022_2023\\VI_semestr\\KiK\\5G-polar-code\\decoder\\")

import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt

from encoder import Encoder
from modulator import Modulator
from transmission_simulation import Channel
from sc_decoder import Decoder
from load_tables import load_fixed_interleaving_pattern_table, load_polar_sequence_and_reliability_table



def BER(input: NDArray[np.uint8], output: NDArray[np.uint8]) -> float:
    return (input != output).sum()/input.size


def test_BER(EbN0dB_values: NDArray[np.int8], K_values: NDArray[np.uint16]) -> List:
    path_1 = "tables\\fixed_interleaving_pattern_table.txt"
    path_2 = "tables\\polar_sequence_and_its_corresponding_reliability.txt"

    pi_max_il = load_fixed_interleaving_pattern_table(path_1)
    Q = load_polar_sequence_and_reliability_table(path_2)

    ### actors
    encoder = Encoder(pi_max_il, Q)
    modulator = Modulator()
    channel = Channel("gwn")
    decoder = Decoder(Q)
    ###

    msg_list = list()
    for K in K_values:
        msg_list.append(np.random.randint(low=0, high=2, size=K, dtype=np.uint8)) # creating random messages of various length
        

    avg_ber_list = list()
    for EbN0dB in EbN0dB_values:
        avg_ber = 0
        for msg in msg_list:
            code_word = encoder.encode(msg, msg.size) # encoding
            bpsk_out = modulator.bpsk(code_word) # BPSK modulating 
            channel_out = channel.send_through(mod_seq=bpsk_out, EbN0dB=EbN0dB, K=msg.size) # adding white noise
            _, decoded_seq = decoder.decode(r=channel_out, K=msg.size) # decoding

            avg_ber += BER(msg, decoded_seq)/len(msg_list) # calculating average BER for defined Eb/N0 [dB]
        
        avg_ber_list.append(avg_ber) # creating list with values of BER for different Eb/N0 [dB]
    
    return avg_ber_list


if __name__ == "__main__":

    EbN0dB_values = np.array([0,1,2,3,4,5,6,7,8,9])
    K_values = np.array([i for i in range(10, 500, 10)])
    avg_ber_list = test_BER(EbN0dB_values, K_values)

    fig, ax = plt.subplots()
    ax.plot(EbN0dB_values, avg_ber_list)
    plt.show()