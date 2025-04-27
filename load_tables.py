import numpy as np

def load_fixed_interleaving_pattern_table(path: str) -> np.ndarray:
    
    with open(path, "rt") as file:
        lines = file.readlines()

    data = []
    for line in lines:
        space_count = 0
        index = ""
        val = ""
        index_val = []
                
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


    pattern_array = np.zeros(len(data), dtype=np.int16)
    for index, val in data:
        pattern_array[int(index)] = int(val)

    return pattern_array
    

def load_polar_sequence_and_reliability_table(path: str) -> np.ndarray:

    with open(path, "rt") as file:
        table_str = file.read()

    table_list = list(map(int, table_str.strip().split()))
  
    table = [[table_list[i], table_list[i+1]] for i in range(0, len(table_list), 2)]

    table_array = np.zeros(len(table), dtype=np.int16)
    for realiability, index in table:
        table_array[realiability] = index

    return table_array

