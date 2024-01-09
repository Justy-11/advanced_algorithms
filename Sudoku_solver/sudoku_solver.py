import sys
import time

def read_puzzle(filename):
    # reads each line, splits it into numbers, converts them to integers, and constructs a 2D list
    with open(filename, 'r') as file:
        puzzle = [[int(num) for num in line.split()] for line in file]
    return puzzle

def possible_values(puzzle, row, col, size):
    values = set(range(1, size + 1))
    block_size = int(size ** 0.5)

    # possible values for specific cell (row,col) by discarding the values in values set which already present in that row and column of puzzle
    for i in range(size):
        values.discard(puzzle[row][i])
        values.discard(puzzle[i][col])

    # Check values in the same block
    # find top-left corner of the block (starting position) containng cell (row, col)
    start_row, start_col = block_size * (row // block_size), block_size * (col // block_size)
    for i in range(start_row, start_row + block_size):
        for j in range(start_col, start_col + block_size):
            values.discard(puzzle[i][j])

    return values

def initialize_empty_cells_and_possible_values(puzzle, size):
    empty_cells = []
    possible_values_dict = {}

    for row in range(size):
        for col in range(size):
            if puzzle[row][col] == 0:
                empty_cells.append((row, col))
                possible_values_dict[(row, col)] = possible_values(puzzle, row, col, size)

    return empty_cells, possible_values_dict

def forward_check(puzzle, row, col, value, size):
    block_size = int(size ** 0.5)

    for i in range(size):
        # check other empty cells in the same row
        if puzzle[row][i] == 0 and i != col:
            if value in possible_values(puzzle, row, i, size):
                puzzle[row][col] = 0  # Revert the current cell
                return False  # Wrong assignment, backtrack
            
        # check other empty cells in the same column
        if puzzle[i][col] == 0 and i != row:
            if value in possible_values(puzzle, i, col, size):
                puzzle[row][col] = 0  # Revert the current cell
                return False  # Wrong assignment, backtrack

    # check other empty cells in the same block
    start_row, start_col = block_size * (row // block_size), block_size * (col // block_size)
    for r in range(start_row, start_row + block_size):
        for c in range(start_col, start_col + block_size):
            if puzzle[r][c] == 0 and (r != row or c != col):
                if value in possible_values(puzzle, r, c, size):
                    puzzle[row][col] = 0  # Revert the current cell
                    return False  # Wrong assignment, backtrack

    return True  # Assignment is valid

def mrv_with_degree_heuristic(empty_cells, possible_values_dict, size):
    if not empty_cells:
        return None
    
    # cell with the Minimum Remaining Values (MRV) - cell with the fewest possible values
    mrv_cell = min(empty_cells, key=lambda cell: len(possible_values_dict[cell]))
    # number of possible values for the MRV cell 
    min_possible_values = len(possible_values_dict[mrv_cell])
    # identify all other empty cells with the same number of possible values
    candidates = [cell for cell in empty_cells if len(possible_values_dict[cell]) == min_possible_values]

    if len(candidates) == 1:
        return candidates[0]

    # multiple candidates - select the cell with the maximum degree 
    # more constraints being satisfied in the early stages of the search 
    return max(candidates, key=lambda cell: degree_heuristic(cell, empty_cells, size))

def degree_heuristic(cell, empty_cells, size):
    row, col = cell
    block_size = int(size ** 0.5)
    # count of other empty cells in the same row, column, and block
    degree = 0

    for i in range(size):
        if (row, i) in empty_cells:
            degree += 1
        if (i, col) in empty_cells:
            degree += 1

    # find starting position of the block and iterates over the block, incrementing the degree for each empty cell found in the same block
    start_row, start_col = block_size * (row // block_size), block_size * (col // block_size)
    for r in range(start_row, start_row + block_size):
        for c in range(start_col, start_col + block_size):
            if (r != row or c != col) and (r, c) in empty_cells:
                degree += 1

    return degree

def solve_sudoku(puzzle, size):
    empty_cells, possible_values_dict = initialize_empty_cells_and_possible_values(puzzle, size)
    if not empty_cells:
        return True  # Puzzle solved

    row, col = mrv_with_degree_heuristic(empty_cells, possible_values_dict, size)
    if row is None:
        return False

    # fill the selected cell with possible values one by one
    for num in possible_values_dict[(row, col)]:
        puzzle[row][col] = num
        forward_check(puzzle, row, col, num, size)

        # recursive trying to solve the remaining puzzle
        if solve_sudoku(puzzle, size):
            return True

        # if current assignment leads to an unsolvable state
        puzzle[row][col] = 0  # Backtrack

    return False

def write_solution(puzzle, input_filename, solved):
    output_filename = input_filename.split('.')[0] + "_output.txt"
    with open(output_filename, 'w') as file:
        if solved:
            for row in puzzle:
                file.write(' '.join(map(str, row)) + '\n')
        else:
            file.write("No Solution")

def main():
    if len(sys.argv) != 2:
        print("Usage: ./sudoku_solver <input_file>")
        return

    input_filename = sys.argv[1]
    puzzle = read_puzzle(input_filename)
    size = len(puzzle)

    # if size not in [9, 16]:
    #     print("Invalid puzzle size")
    #     return

    start_time = time.time()
    solved = solve_sudoku(puzzle, size)
    end_time = time.time()

    elapsed_time = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"Sudoku puzzle solved in {elapsed_time:.4f} milliseconds")

    write_solution(puzzle, input_filename, solved)

if __name__ == "__main__":
    main()