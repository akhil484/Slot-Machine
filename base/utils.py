from myproject.config_params import char_values, frequency
import random

def create_grid_of_chars():
    char_list = []
    grid = []
    for key, value in frequency.items():
        for _ in range(value):
            char_list.append(key)
    
    random.shuffle(char_list)
    for _ in range(3):
        row = []
        for _ in range(3):
            number = random.randrange(0, 24)
            row.append(char_list[number])
        grid.append(row)

    return grid

    
        