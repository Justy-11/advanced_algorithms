#### 1. Introduction
Sudoku is a logic-based number-placement puzzle. This report gives the implementation of an efficient
algorithm with minimal time complexity thatsolves both standard 9 × 9 Sudoku puzzles and the variant 
Hexadoku puzzles (16 ×16). The algorithm, implemented in Python and uses backtracking with 
Minimum Remaining Values (MRV), degree heuristic, and forward checking.

#### 2. Background and constraints
##### 2.1 Standard Sudoku Puzzle Rules
The standard Sudoku puzzle has a 9 × 9 grid, divided into nine 3 × 3 blocks (sub-grids). The rules 
are as follows:
• Each cell can contain a number from 1 to 9. 
• No repetition of numbers in rows, columns, or blocks.
##### 2.2 Hexadoku Puzzle Rules
Hexadoku is a variant which has a 16 × 16 grid, divided into sixteen 4 × 4 blocks. The numbers 
range from 1 to 16. The rest of the rules remain the same as in the standard Sudoku puzzle.
##### 2.3 Input and Output Format
Input: a text file containing the puzzle which should be located in the root directory of the 
program, lines in the file representing the rows of the puzzle (9 rows with 9 numbers (space 
separated) in each row in case of a standard Sudoku puzzle), and zeros denoting empty cells. 
Output: a text file with the solution (space separated values) or "No Solution" if unsolvable. The
output text file is named as input file name with suffix “_output” added.

#### 3. Implementation of the Algorithm
##### 3.1 Running Python Code from command line
Navigate to the directory containing the Python script and the Sudoku puzzle text files. Then run
the Python script by using the following command:
python sudoku_solver.py <file_name>.txt
##### 3.2 Reading puzzle
Reading puzzle is done by reading each line in the text file given, splitting the lines into numbers, 
and converting numbers to integers and then creating a 2D list that contains the puzzle.
##### 3.3 Initialize empty cells and possible values
From the 2D list created from reading the puzzle, the algorithm is iterating over each cell in the 
2D list, finding out the cells that are empty (those contains the value 0), and saving the coordinates
(row, column) of the empty cells to a list. At the same time, its saving possible values that can be 
placed in those empty cells as a dictionary. The possible values are determined for each empty cell
as a set by first creating a set that contains integers from 1 to size of the puzzle, then iterating over 
the corresponding row, column, and block of the empty cell, discarding values from the set that 
are already present in these regions. Iteration over the block is done by finding the top-left corner’s 
coordinates of the block which contains the specific empty cell. If there are no empty cells, the 
puzzle is solved.
##### 3.4 MRV with Degree Heuristic
From the possible values for each empty cell (which is a dictionary), the algorithm is finding the 
cell coordinates of the one with the Minimum Remining value (MRV) (cell with fewest possible
values). Then it is finding other empty cells which having the same number of possible values as 
the MRV cell. If there is only one cell with the same number of fewest possible values as MRV 
cell, that cell’s coordinates of that cell are returned. If there are multiple candidates with same 
number of fewest possible values as MRV cell, then algorithm is selecting the cell with maximum 
degree from the candidates using the degree heuristic. In degree heuristic, for every candidate 
(empty cells which has fewest possible values) selected, the algorithm is counting the number of 
other empty cells (degree) in the same row, column and block as the candidate by iterating over 
the row, column, and block of the candidate. The algorithm is then selecting the candidate with the 
maximum degree. Using this MRV with degree heuristic, the algorithm is selecting the empty cell
that needs to be filled with possible values in the 2D list (puzzle).
##### 3.5 Backtracking with Forward Checking
Then the algorithm is starting to fill the selected empty cell with the possible values one by one
(in a loop) with forward checking. In forward checking, it is checking whether the possible values 
set for other empty cells in the same row, column, and block contain the same filled value as the 
assigned cell’s value. This is done by iterating through row, column, and block of the empty cell 
with assigned value. If any of the empty cell in same row, column, or bock contains the same value
as the assigned cell’s value, the algorithm reverts and backtrack the assignment for the current cell, 
setting it back to 0. It backtracks because there should be no repetition of numbers in rows, 
columns, and blocks. After forward checking, the algorithm is recursively trying to solve the 
puzzle by trying out different possible values for empty cells by calling ‘solve_sudoku’ function.
This function returns a boolean indicating whether the puzzle is solved or not. It contained the 
initializing empty and possible values, MRV with degree heuristic, and backtracking with forward 
checking. When the 'solve_sudoku' function is recursively called, if the puzzle is successfully 
solved, it returns true. But, if the puzzle remains unsolved, the algorithm backtracks the assignment 
of the current cell, setting it back to 0. Because the previous assignment made the puzzle 
unsolvable (if solve_sudoku returns false), so need to backtrack. So the algorithm recursively tries
different possible values for selected empty cells until a solution is found (‘solve_sudoku’ function 
returns true).
##### 3.6 Write solution
Finally, if the ‘solve_sudoku’ function returns true, the solution is printed to an output text file 
with the input file name and the ‘_output’ suffix added. If the 'solve_sudoku' function returns false, 
'No Solution' is printed to the output text file.

##### 4. Optimization techniques
###### 4.1 MRV (Minimum Remaining Values)
The MRV gives priority to empty cells with the fewest possible values. By selecting empty cells 
with a fewest number of possibilities first, the algorithm reduces the search space more quickly. 
The number of possibilities for each cell will be reduced by this.
###### 4.2 Degree heuristic
The degree heuristic takes the count of other empty cells in the same row, column, and block. From 
these counts, selecting the cell that has a higher count (degree) determinesthe order in which empty
cells are filled. Also, it leads to more constraints being satisfied in the early stages of the search.
###### 4.3 Forward checking
Forward checking is applied during the assignment of values to empty cells. Immediately after an 
assignment, it checks for conflicts in the same row, column, and block (prevent the repetition of 
same value in rows, columns, and blocks). Identifying and backtracking the invalid possibilities 
early in the process helps to reduce the number of possibilities for each cell and guides the order 
in which the algorithm explores the solution space.
###### 4.4 Efficient data structures
Sets are used for storing possible values and dictionaries for tracking empty cells and their possible 
values. So, during the Sudoku puzzle solving process, it helps for efficient lookups and updates.

##### 5. Challenges faced
- Initially, I used the numpy library for the puzzle grid. The use of numpy took more processing time 
for the Sudoku puzzles than using Python lists. By doing a reevaluation, I came to a conclusion 
that, the overhead introduced by numpy because of small scale puzzle grids. So, its efficient to use 
numpy for large-scale numerical operations.
- Adapting the algorithm (initially the algorithm worked for 9 by 9 with minimum time complexity) 
to handle Sudoku variant Hexadoku, required additional logic and testing to make sure the correct 
functionality and to reduce time complexity.

6. Limitations
- The algorithm ties to find a single solution. Some puzzles might have multiple valid solutions, and 
the algorithm may not explore all of them.
- The algorithm is for general standard 9x9 and 16x16 Sudoku puzzles. Adapting it to handle nonstandard puzzle sizes (rules might differ) might need significant modifications.
- C++ implementation of this algorithm might be better in terms of time complexity and efficiency.

7. Future Improvements
- Parallelizing Sudoku solving process for efficient solving.
- Small adjustments to the heuristics used in the algorithm based on experimentation.
- Adding techniques to handle puzzles with multiple solutions
