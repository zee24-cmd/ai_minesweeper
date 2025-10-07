import unittest
import random
from project import Minesweeper, Sentence, MinesweeperAI

class TestMinesweeper(unittest.TestCase):

    def test_minesweeper_initialization(self):
        """
        Checks if height width and number of mines are correctly set
        """
        height = 8
        width = 8
        mines = 10
        game = Minesweeper(height, width, mines)

        self.assertEqual(game.height, height)
        self.assertEqual(game.width, width)
        self.assertEqual(len(game.mines), mines)

    def test_minesweeper_is_mine(self):
        """
        Checks if a cell known to be a mine is identified as a mine
        """
        game = Minesweeper(8, 8, 10)
        mine_cell = random.choice(list(game.mines))
        self.assertTrue(game.is_mine(mine_cell))

    def test_minesweeper_nearby_mines(self):
        """
        Checks if the count of nearby mines is aptly calculated
        """
        game = Minesweeper(8, 8, 10)
        cell = (0, 0)
        nearby_mines = game.nearby_mines(cell)
        self.assertGreaterEqual(nearby_mines, 0)

    def test_minesweeper_won(self):
        """
        Checks if game identifies a win when all mines are flagged
        """
        game = Minesweeper(8, 8, 10)
        game.mines_found = game.mines
        self.assertTrue(game.won())

class TestSentence(unittest.TestCase):

    def test_sentence_initialization(self):
        """
        Checks if cell and count were correctly set
        """
        cells = {(0, 0), (0, 1), (1, 0)}
        count = 1
        sentence = Sentence(cells, count)

        self.assertEqual(sentence.cells, cells)
        self.assertEqual(sentence.count, count)

    def test_sentence_known_mines(self):
        """
        Checks if all cells are identified as mines when the count matches number of cells
        """
        cells = {(0, 0), (0, 1), (1, 0)}
        count = 3
        sentence = Sentence(cells, count)
        self.assertEqual(sentence.known_mines(), cells)

    def test_sentence_known_safes(self):
        """
        Checks if all cells are correctly identified as safe when the count becomes 0
        """
        cells = {(0, 0), (0, 1), (1, 0)}
        count = 0
        sentence = Sentence(cells, count)
        self.assertEqual(sentence.known_safes(), cells)

    def test_sentence_mark_mine(self):
        """
        Checks if cell is correctly marked as mine  and removed from the sentence
        """
        cells = {(0, 0), (0, 1), (1, 0)}
        count = 1
        sentence = Sentence(cells, count)
        sentence.mark_mine((0, 0))
        self.assertEqual(sentence.cells, {(0, 1), (1, 0)})
        self.assertEqual(sentence.count, 0)

    def test_sentence_mark_safe(self):
        """
        Checks if cell is correctly marked as safe and removed from sentence
        """
        cells = {(0, 0), (0, 1), (1, 0)}
        count = 1
        sentence = Sentence(cells, count)
        sentence.mark_safe((0, 0))
        self.assertEqual(sentence.cells, {(0, 1), (1, 0)})
        self.assertEqual(sentence.count, 1)

class TestMinesweeperAI(unittest.TestCase):

    def test_minesweeper_ai_initialization(self):
        """
        Checks if height width and initial knowledge are correctly set
        """
        height = 8
        width = 8
        ai = MinesweeperAI(height, width)

        self.assertEqual(ai.height, height)
        self.assertEqual(ai.width, width)
        self.assertEqual(ai.moves_made, set())
        self.assertEqual(ai.mines, set())
        self.assertEqual(ai.safes, set())
        self.assertEqual(ai.knowledge, [])

    def test_minesweeper_ai_mark_mine(self):
        """
        Checks if cell is marked as mine and updated in the knowledge base 
        """
        ai = MinesweeperAI(8, 8)
        ai.mark_mine((0, 0))
        self.assertIn((0, 0), ai.mines)

    def test_minesweeper_ai_mark_safe(self):
        """
        Checks if cell is marked as safe and updated in the knowledge base 
        """
        ai = MinesweeperAI(8, 8)
        ai.mark_safe((0, 0))
        self.assertIn((0, 0), ai.safes)

    def test_minesweeper_ai_add_knowledge(self):
        """
        Checks if knowledge is corectly added to AI's knowledge base
        """
        ai = MinesweeperAI(8, 8)
        ai.add_knowledge((0, 0), 1)
        self.assertIn((0, 0), ai.moves_made)
        self.assertIn((0, 0), ai.safes)
        self.assertGreater(len(ai.knowledge), 0)

    def test_minesweeper_ai_make_safe_move(self):
        """
        Checks if AI correctly identifies and returns a safe move from the data in AI's knowledge base
        """
        ai = MinesweeperAI(8, 8)
        ai.mark_safe((0, 0))
        move = ai.make_safe_move()
        self.assertEqual(move, (0, 0))

    def test_minesweeper_ai_make_random_move(self):
        """
        Checks if AI makes a random move thats is not a mine or a pre-existing move 
        """
        ai = MinesweeperAI(8, 8)
        move = ai.make_random_move()
        self.assertIsNotNone(move)
        self.assertNotIn(move, ai.moves_made)
        self.assertNotIn(move, ai.mines)

if __name__ == "__main__":
    unittest.main() 