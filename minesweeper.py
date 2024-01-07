import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count


    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # following the logic in the description, if a set of cells equal to the number of mines, then all cells must be mines
        mines = set()
        if len(self.cells) == self.count:
                mines.update(self.cells)
        return mines
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # reversely, if no mines are in the a set of cells, then those cells are safe.

        safes=set()
        if self.count == 0:
            safes.update(self.cells)
        return safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # if a cell is known to be a mine, then removing it from the cell will reduce total number of mines by 1


        if cell in self.cells: 
            self.cells.remove(cell)  
            self.count -= 1 
                    



    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        #likeweise, if a cell is known to be safe, then we can safely remove it without affecting the total number of mines

        if cell in self.cells:
            self.cells.remove(cell)

class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

        #adding get neighbors fucntion to return neighbors that are inside the boundaries of the board
    def get_neighbors(self, cell):
        i, j = cell
        neighbors = [
        (i-1, j-1), (i-1, j), (i-1, j+1),
        (i, j-1),           (i, j+1),
        (i+1, j-1), (i+1, j), (i+1, j+1),
        ]
        
        good_neighbors = []
        for ni, nj in neighbors:
            if 0 <= ni < self.height and 0 <= nj < self.width:
                good_neighbors.append((ni, nj))

        return good_neighbors
    

    def frontier (self,cell):
    #adding frontier cell so that we know what cells are unexplored
        i,j = cell
        frontier_cell=[]
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made:
                    frontier_cell.append((i,j))
        
        return frontier_cell


    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #1
        self.moves_made.add(cell)
        #2
        self. mark_safe(cell)
        #3
        neighbors = self.get_neighbors(cell)  
        new_sentence = Sentence(neighbors, count)
        self.knowledge.append(new_sentence)
        removing = []
        #4  adding neighbors
        for sentence in self.knowledge:
            for mine in sentence.known_mines():
                self.mark_mine(mine)
            for safe in sentence.known_safes():
                self.mark_safe(safe)
        


        #5 continue to loop to infer on subset,  set2 - set1 = count2 - count2
            for sentence2 in self.knowledge:
                if sentence != sentence2 and sentence.cells.issubset(sentence2.cells):
                    new_cells = sentence2.cells - sentence.cells
                    new_count = sentence2.count - sentence.count
                    new_sentence2 = Sentence(new_cells, new_count)
                    if new_sentence2 not in self.knowledge:
                            self.knowledge.append(new_sentence2)



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
       
        for safe_cell in self.safes:
        # If the cell has not been clicked yet, return it
            if safe_cell not in self.moves_made:
             return safe_cell

        return None





    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        random_move = []
        
        for i in range (self.height):
            for j in range (self.width):
                cell = (i,j)
                if cell not in self.mines and cell not in self.moves_made:
                        random_move.append(cell)

        if random_move:
            return random.choice(random_move)
        return None

        