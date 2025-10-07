
# Minesweeper with AI Bot 

### YOUTUBE LINK : https://youtu.be/sOBJgqQa5u4

### Description: The project made is an implementation of the classic game Minesweeper, using Python with the Pygame library for graphical representation and interactive gameplay. It features both manual (human) and automated (AI) gameplay. The program consists of multiple classes that handle different aspects of the game, such as the game mechanics, the AI logic, and the graphical user interface (GUI). 

1. Minesweeper Class  
The Minesweeper class handles the core logic of the game, including:
- Board Initialization: The board is represented as a 2D list (self.board), where True indicates a mine and False indicates an empty cell.
- Mine Placement: Mines are placed randomly on the board without overlap.
- Cell Functions: 
  - is_mine(cell): Checks if a specific cell contains a mine.
  - nearby_mines(cell): Counts how many mines are adjacent to a given cell (in all 8 directions).
- Win Condition: The won() method checks if the player has flagged all mines correctly.

2. Sentence Class (Knowledge Representation)
The Sentence class represents logical statements about the game based on the AI’s current knowledge:
- Each sentence contains a set of cells and a count representing how many mines are in those cells.
- Methods: 
  - known_mines() and known_safes() infer which cells are definitely mines or safe based on the count and cells.
  - mark_mine() and mark_safe() update the sentence when new information is known.

This class allows the AI to reason about the game state, making deductions similar to a human player.

 3. MinesweeperAI Class (Artificial Intelligence)
The MinesweeperAI class simulates an intelligent player:
- Knowledge Base: Maintains sets of known safe cells, mines, and the moves already made.
- Deduction Engine: 
  - add_knowledge(cell, count): Adds new information after each move, updating the knowledge base.
  - Inference is made through logical deduction—if certain conditions are met (e.g., all cells in a sentence are mines), the AI updates its beliefs.
- Decision Making: 
  - make_safe_move() picks a cell known to be safe.
  - make_random_move() chooses a move based on probability if no safe move is known.

4. Main Game Loop (Graphical Interface with Pygame)
The main() function manages the entire game loop:
- Initialization: Sets up the game board, AI agent, fonts, and images for flags and mines.
- User Interface: 
  - Instructions Screen: Displays the game rules before gameplay starts.
  - Game Board: Draws the grid, mines, numbers (indicating nearby mines), and flags.
  - Buttons: 
    - "AI Bot Move" Button: Triggers the AI to make a move.
    - "Reset" Button: Resets the game to its initial state.
- Mouse Events: Handles left-clicks (to reveal a cell), right-clicks (to flag a mine), and button clicks.
- Game Logic: Updates the board, checks for win/loss conditions, and updates the AI’s knowledge after each move.

5. AI Decision-Making in Action
- The AI first tries to make a safe move if possible.
- If no safe moves are available, it resorts to a probabilistic guess.
- The AI updates its knowledge with every move, allowing it to make more informed decisions as the game progresses.

6. Key Features
- Human vs. AI Gameplay: Players can either play manually or let the AI make moves.
- Dynamic AI: The AI improves as the game progresses by learning from the current board state.
- Visual Feedback: The GUI provides immediate feedback on player actions (revealed cells, flagged mines, etc.).

This Minesweeper implementation combines classic game mechanics with an intelligent decision-making system. The AI doesn’t rely on brute-force guessing but uses logical inference, making it more like a real player. The Pygame GUI adds an interactive and visually appealing layer to the game.




