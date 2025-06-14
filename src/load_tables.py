from typing import List
import numpy as np
from numpy.typing import NDArray

def load_fixed_interleaving_pattern_table(path: str) -> NDArray[np.uint8]:
    """
    Function for loading fixed interleaving pattern table.

    Parameters
    ----------
    path : str
        Path to .txt file which represents fixed interleaving table.
    
    Returns
    -------
    NDArray[np.uint8]
        Vector representing fixed interleaving pattern table.
    """
    
    with open(path, "rt") as file:
        lines: List[str] = file.readlines()

    data: List[List[str]] = []
    for line in lines:
        space_count: int = 0
        index: str = ""
        val: str = ""
        index_val: List[str] = []
                
        for char in line:
            if char == " " or char == "\n":
                index_val.append(str(val if val != "" else index))
                space_count += 1
                
                if space_count % 2 == 0:
                    data.append(index_val)
                    index_val = []
                    index = ""
                    val = ""

            else:
                if space_count % 2 == 0:
                    index += char
                else:
                    val += char


    pattern_array = np.zeros(len(data), dtype=np.uint8)
    for index, val in data:
        pattern_array[int(index)] = int(val)

    return pattern_array
    

def load_polar_sequence_and_reliability_table(path: str) -> NDArray[np.uint16]:
    """
    Function for loading polar sequence and its corresponding reiablity table.

    Parameters
    ----------
    path : str
        Path to .txt file representing polar seqence and its reliability table.
    
    Returns
    -------
    NDArray[np.uint16]
        Vector where indexes represent realiabilities and values represent polar sequence.
    """

    with open(path, "rt") as file:
        table_str = file.read()

    table_list = list(map(int, table_str.strip().split()))
  
    table = [[table_list[i], table_list[i+1]] for i in range(0, len(table_list), 2)]

    table_array = np.zeros(len(table), dtype=np.uint16)
    for realiability, index in table:
        table_array[realiability] = index

    return table_array

