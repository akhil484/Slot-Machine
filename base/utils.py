from myproject.config_params import char_values, frequency
import random

def create_grid_of_chars():
    char_list = []
    grid = []
    for key, value in frequency.items():
        for _ in range(value):
            char_list.append(key)
    
    random.shuffle(char_list)
    i = 100
    for _ in range(3):
        row = []
        for _ in range(3):
            number = random.randrange(0, i)
            row.append(char_list[number])
            i = i-1
            char_list.pop(number)
        grid.append(row)

    return grid

def calculate_winning_points(grid):
    score = 0
    for row in grid:
        if row[0] == row[1] == row[2]:
            score = score + char_values[row[0]]

    return score

    
        