import sys
sys.path.append("e:\\Studia_Teleinformatyka_2022_2023\\VI_semestr\\KiK\\5G-polar-code\\")
sys.path.append("e:\\Studia_Teleinformatyka_2022_2023\\VI_semestr\\KiK\\5G-polar-code\\src\\decoder\\")
from typing import Generator

import numpy as np
from numpy.typing import NDArray
import matplotlib.pyplot as plt

from src.encoder import Encoder
from src.modulator import Modulator
from src.transmission_simulation import Channel
from src.decoder.sc_decoder import Decoder
from src.load_tables import load_fixed_interleaving_pattern_table, load_polar_sequence_and_reliability_table



def BER(input: NDArray[np.uint8], output: NDArray[np.uint8]) -> float:
    """
    Calculating BER (Bit Error Rate) for two seqences of bits.

    Parameters
    ----------
    input : NDArray[np.uint8]
        Sent bits (not yet affected by noise in channel).
    output : NDArray[np.uint8]
        Received bits after transmission.

    Returns
    -------
    float
        BER value.
    """

    return (input != output).sum()/input.size


def generate_messages(K_values: NDArray[np.uint16]) -> Generator[NDArray[np.uint16], None, None]:
    """
    Generates random messages of sizes provided by K_values parameter.

    Parameters
    ----------
    K_values : NDArray[np.uint16]
        Sizes of messages arrays that will be generated.

    Yields
    ------
    Generator[NDArray[np.uint16], None, None]
        Messages of sizes defined in K_values parameter.
    """

    for K in K_values:
        yield np.random.randint(low=0, high=2, size=K, dtype=np.uint8)


def avg_BER(EbN0dB_values: NDArray[np.float64], K_values: NDArray[np.uint16]) -> NDArray[np.float64]:
    """
    Calculating average BER values for different Eb/N0 [dB].

    Parameters
    ----------
    EbN0dB_values : NDArray[np.float64]
        Array with various Eb/N0 [dB] values. 
    K_values : NDArray[np.uint16]
        Array with various sizes of messages. 

    Returns
    -------
    NDArray[np.float64]
        Values of average BER for different Eb/N0 [dB] values.
    """

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

    avg_ber_arr = np.zeros(EbN0dB_values.size, dtype=np.float64)
    for msg in generate_messages(K_values):
        code_word = encoder.encode(msg, E=msg.size) # encoding
        bpsk_out = modulator.bpsk(code_word) # BPSK modulating 
        
        for i, EbN0dB in enumerate(EbN0dB_values):     
            channel_out = channel.send_through(mod_seq=bpsk_out, EbN0dB=EbN0dB, K=msg.size) # adding white noise
            _, decoded_seq = decoder.decode(r=channel_out, K=msg.size) # decoding

            avg_ber_arr[i] += BER(msg, decoded_seq)/K_values.size # calculating average BER for next Eb/N0 [dB] values
    
    return avg_ber_arr



if __name__ == "__main__":
    """Testing BER and drawing BER vs Eb/N0 plot."""
    
    EbN0dB_values = np.array([i for i in np.arange(0, 11, 1)])
    K_values = np.array([i for i in range(10, 500, 5)])
    avg_ber_arr = avg_BER(EbN0dB_values, K_values)
    print(avg_ber_arr)

    fig, ax = plt.subplots()
    ax.plot(EbN0dB_values, avg_ber_arr)
    ax.set_title("Bit Error Rate")
    ax.set_xlabel("E$_b$/N$_0$ [dB]")
    ax.set_ylabel("BER")
    plt.show()