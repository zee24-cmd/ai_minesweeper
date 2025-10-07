import pygame
import sys
import time
import random

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height, width, mines):

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

        # Add mines randomly using random library
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

        # Keep count of mines nearby
        count = 0

        # loop over all cells within one row and column
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

        # If count of mines is equal to number of cells (and > 0), all cells are mines:
        if len(self.cells) == self.count and self.count != 0:
            print('Mine Identified! - ', self.cells)
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # If count of mines is zero then all cells in the sentence are safe:
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """

        # If cell is in the sentence, remove it and decrement count by one
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """

        # If cell is in the sentence, remove it, but do not decrement count
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height, width):

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

        # Mark the cell as a move that has been made, and mark as safe:
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # Create set to store undecided cells for KB:
        new_sentence_cells = set()

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # If cells are already safe, ignore them:
                if (i, j) in self.safes:
                    continue

                # If cells are known to be mines, reduce count by 1 and ignore them:
                if (i, j) in self.mines:
                    count = count - 1
                    continue

                # Otherwise add them to sentence if they are in the game board:
                if 0 <= i < self.height and 0 <= j < self.width:
                    new_sentence_cells.add((i, j))

        # Add the new sentence to the AI's Knowledge Base:
        print(f'Next Move : {cell} has added sentence to knowledge {new_sentence_cells} = {count}' )
        self.knowledge.append(Sentence(new_sentence_cells, count))

        # Iteratively mark guaranteed mines and safes, and infer new knowledge:
        knowledge_changed = True

        while knowledge_changed:
            knowledge_changed = False

            safes = set()
            mines = set()

            # Get set of safe spaces and mines from KB
            for sentence in self.knowledge:
                safes = safes.union(sentence.known_safes())
                mines = mines.union(sentence.known_mines())

            # Mark any safe spaces or mines:
            if safes:
                knowledge_changed = True
                for safe in safes:
                    self.mark_safe(safe)
            if mines:
                knowledge_changed = True
                for mine in mines:
                    self.mark_mine(mine)

            # Remove any empty sentences from knowledge base:
            empty = Sentence(set(), 0)

            self.knowledge[:] = [x for x in self.knowledge if x != empty]

            # Try to infer new sentences from the current ones:
            for sentence_1 in self.knowledge:
                for sentence_2 in self.knowledge:

                    # Ignore when sentences are identical
                    if sentence_1.cells == sentence_2.cells:
                        continue

                    if sentence_1.cells == set() and sentence_1.count > 0:
                        print('Error - sentence with no cells and count created')
                        raise ValueError

                    # Create a new sentence if 1 is subset of 2, and not in KB:
                    if sentence_1.cells.issubset(sentence_2.cells):
                        new_sentence_cells = sentence_2.cells - sentence_1.cells
                        new_sentence_count = sentence_2.count - sentence_1.count

                        new_sentence = Sentence(new_sentence_cells, new_sentence_count)

                        # Add to knowledge if not already in KB:
                        if new_sentence not in self.knowledge:
                            knowledge_changed = True
                            print('New Inferred Knowledge: ', new_sentence, 'from', sentence_1, ' and ', sentence_2)
                            self.knowledge.append(new_sentence)

        # Print out AI current knowledge to terminal:
        print('Safe Moves Remaining: ', self.safes - self.moves_made)
        print('====================================================')

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # Get set of safe cells that are not moves already done:
        safe_moves = self.safes - self.moves_made
        if safe_moves:
            print('Making a Safe Move! Safe moves available: ', len(safe_moves))
            return random.choice(list(safe_moves))

        # Otherwise no guaranteed safe moves can be made
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # dictionary to hold possible moves and their mine probability:
        moves = {}
        MINES = 5

        # Calculate basic probability of any cell being a mine with no KB:
        num_mines_left = MINES - len(self.mines)
        spaces_left = (self.height * self.width) - (len(self.moves_made) + len(self.mines))

        # If no spaces are left that are acceptable moves, return no move possible
        if spaces_left == 0:
            return None

        basic_prob = num_mines_left / spaces_left

        # Get list of all possible moves that are not mines
        for i in range(0, self.height):
            for j in range(0, self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    moves[(i, j)] = basic_prob

        # If no moves have been made (nothing in KB) then any is a good option:
        if moves and not self.knowledge:
            move = random.choice(list(moves.keys()))
            print('AI Selecting Random Move With Basic Probability: ', move)
            return move

        # Otherwise can potentially improve random choice using KB:
        elif moves:
            for sentence in self.knowledge:
                num_cells = len(sentence.cells)
                count = sentence.count
                mine_prob = count / num_cells
                # If mine probabilty of each cell is worse than listed, update it:
                for cell in sentence.cells:
                    if moves[cell] < mine_prob:
                        moves[cell] = mine_prob

            # Get and return random move with lowest mine probability:
            move_list = [[x, moves[x]] for x in moves]
            move_list.sort(key=lambda x: x[1])
            best_prob = move_list[0][1]

            best_moves = [x for x in move_list if x[1] == best_prob]
            move = random.choice(best_moves)[0]
            print('AI Selecting Random Move with lowest mine probability using KB: ', move)

            # Return a random choice from the best moves list
            return move
        
def main():
    # Initialize game parameters
    HEIGHT = 5
    WIDTH = 5
    MINES = 5

    # Colors
    BLACK = (0, 0, 0)
    GRAY = (180, 180, 180)
    WHITE = (255, 255, 255)

    # Create game
    pygame.init()
    size = width, height = 1400, 800
    screen = pygame.display.set_mode(size)

    # Fonts
    #OPEN_SANS = "OpenSans-Regular.ttf"
    smallFont = pygame.font.SysFont("Open Sans", 20)
    mediumFont = pygame.font.SysFont("Open Sans", 28)
    largeFont = pygame.font.SysFont("Open Sans", 40)

    # Compute board size
    BOARD_PADDING = 20
    board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
    board_height = height - (BOARD_PADDING * 2)
    cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
    board_origin = (BOARD_PADDING, BOARD_PADDING)

    # Add images
    flag = pygame.image.load("flag.png")
    flag = pygame.transform.scale(flag, (cell_size, cell_size))
    mine = pygame.image.load("mine.png")
    mine = pygame.transform.scale(mine, (cell_size, cell_size))

    # Create game and AI agent
    game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
    ai = MinesweeperAI(height=HEIGHT, width=WIDTH)

    # Keep track of revealed cells, flagged cells, and if a mine was hit
    revealed = set()
    flags = set()
    lost = False

    # Show instructions initially
    instructions = True

    while True:
        # Check if game quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(BLACK)

        # Show game instructions
        if instructions:
            # Title
            title = largeFont.render("Play Minesweeper", True, WHITE)
            titleRect = title.get_rect()
            titleRect.center = ((width / 2), 80)
            screen.blit(title, titleRect)

            # Rules
            rules = [
                "Click a cell to reveal it.",
                "Right-click a cell to mark it as a mine.",
                "Mark all mines successfully to win!"
            ]
            for i, rule in enumerate(rules):
                line = mediumFont.render(rule, True, WHITE)
                lineRect = line.get_rect()
                lineRect.center = ((width / 2), 150 + 30 * i)
                screen.blit(line, lineRect)

            # Play game button
            buttonRect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 80)
            buttonText = mediumFont.render("Play Game", True, BLACK)
            buttonTextRect = buttonText.get_rect()
            buttonTextRect.center = buttonRect.center
            pygame.draw.rect(screen, WHITE, buttonRect)
            screen.blit(buttonText, buttonTextRect)

            # Check if play button clicked
            click, _, _ = pygame.mouse.get_pressed()
            if click == 1:
                mouse = pygame.mouse.get_pos()
                if buttonRect.collidepoint(mouse):
                    instructions = False
                    time.sleep(0.3)

            pygame.display.flip()
            continue

        # Draw board
        cells = []
        for i in range(HEIGHT):
            row = []
            for j in range(WIDTH):
                # Draw rectangle for cell
                rect = pygame.Rect(
                    board_origin[0] + j * cell_size,
                    board_origin[1] + i * cell_size,
                    cell_size, cell_size
                )
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, WHITE, rect, 3)

                # Add a mine, flag, or number if needed
                if game.is_mine((i, j)) and lost:
                    screen.blit(mine, rect)
                elif (i, j) in flags:
                    screen.blit(flag, rect)
                elif (i, j) in revealed:
                    neighbors = smallFont.render(
                        str(game.nearby_mines((i, j))),
                        True, BLACK
                    )
                    neighborsTextRect = neighbors.get_rect()
                    neighborsTextRect.center = rect.center
                    screen.blit(neighbors, neighborsTextRect)

                row.append(rect)
            cells.append(row)

        # AI Move button
        aiButton = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 50,
            (width / 3) - BOARD_PADDING * 2, 50
        )
        buttonText = largeFont.render("AI Bot Move", True, BLACK)
        buttonRect = buttonText.get_rect()
        buttonRect.center = aiButton.center
        pygame.draw.rect(screen, WHITE, aiButton)
        screen.blit(buttonText, buttonRect)

        # Reset button
        resetButton = pygame.Rect(
            (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
            (width / 3) - BOARD_PADDING * 2, 50
        )
        buttonText = largeFont.render("Reset", True, BLACK)
        buttonRect = buttonText.get_rect()
        buttonRect.center = resetButton.center
        pygame.draw.rect(screen, WHITE, resetButton)
        screen.blit(buttonText, buttonRect)

        # Display text
        text = "Lost" if lost else "Won" if game.mines == flags else ""
        text = mediumFont.render(text, True, WHITE)
        textRect = text.get_rect()
        textRect.center = ((5 / 6) * width, (2 / 3) * height)
        screen.blit(text, textRect)

        move = None

        left, _, right = pygame.mouse.get_pressed()

        # Check for a right-click to toggle flagging
        if right == 1 and not lost:
            mouse = pygame.mouse.get_pos()
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                        if (i, j) in flags:
                            flags.remove((i, j))
                        else:
                            flags.add((i, j))
                        time.sleep(0.2)

        elif left == 1:
            mouse = pygame.mouse.get_pos()

            # If AI button clicked, make an AI move
            if aiButton.collidepoint(mouse) and not lost:
                move = ai.make_safe_move()
                if move is None:
                    move = ai.make_random_move()
                    if move is None:
                        flags = ai.mines.copy()
                        print("No moves left to make.")
                    else:
                        print("No known safe moves, AI making random move.")
                else:
                    print("AI making safe move.")
                time.sleep(0.2)

            # Reset game state
            elif resetButton.collidepoint(mouse):
                game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
                revealed = set()
                flags = set()
                lost = False
                continue

            # User-made move
            elif not lost:
                for i in range(HEIGHT):
                    for j in range(WIDTH):
                        if (cells[i][j].collidepoint(mouse)
                                and (i, j) not in flags
                                and (i, j) not in revealed):
                            move = (i, j)

        # Make move and update AI knowledge
        if move:
            if game.is_mine(move):
                lost = True
            else:
                nearby = game.nearby_mines(move)
                revealed.add(move)
                ai.add_knowledge(move, nearby)

        pygame.display.flip()

if __name__ == "__main__":
    main()