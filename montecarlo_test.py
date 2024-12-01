import unittest
import pandas as pd
import numpy as np
from montecarlo import Die, Game, Analyzer, load_alphabet_die


class TestDie(unittest.TestCase):

    def setUp(self):
        self.die = Die(['A', 'B', 'C'])

    def test_initial_weights(self):
        self.assertTrue((self.die._die_df['Weight'] == 1.0).all())

    def test_change_weight(self):
        self.die.change_weight('A', 2.5)
        self.assertEqual(self.die._die_df.loc[self.die._die_df['Face'] == 'A', 'Weight'].values[0], 2.5)

    def test_invalid_weight_change(self):
        with self.assertRaises(ValueError):
            self.die.change_weight('D', 2.0)

    def test_roll(self):
        rolls = self.die.roll(5)
        self.assertEqual(len(rolls), 5)
        self.assertTrue(set(rolls).issubset({'A', 'B', 'C'}))

    def test_show(self):
        df = self.die.show()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)


class TestGame(unittest.TestCase):

    def setUp(self):
        self.dice = [Die(['A', 'B', 'C']) for _ in range(3)]
        self.game = Game(self.dice)

    def test_play(self):
        self.game.play(10)
        self.assertEqual(len(self.game._results), 10)

    def test_show_wide(self):
        self.game.play(5)
        results = self.game.show('wide')
        self.assertEqual(results.shape[0], 5)

    def test_show_narrow(self):
        self.game.play(5)
        results = self.game.show('narrow')
        self.assertEqual(len(results), 15)  # 5 rolls * 3 dice


class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        dice = [Die(['A', 'B', 'C']) for _ in range(3)]
        self.game = Game(dice)
        self.game.play(10)
        self.analyzer = Analyzer(self.game)

    def test_jackpot(self):
        jackpots = self.analyzer.jackpot()
        self.assertGreaterEqual(jackpots, 0)

    def test_face_counts_per_roll(self):
        face_counts = self.analyzer.face_counts_per_roll()
        self.assertIsInstance(face_counts, pd.DataFrame)
        self.assertEqual(face_counts.shape[0], 10)

    def test_combo_count(self):
        combos = self.analyzer.combo_count()
        self.assertIsInstance(combos, pd.DataFrame)

    def test_permutation_count(self):
        permutations = self.analyzer.permutation_count()
        self.assertIsInstance(permutations, pd.DataFrame)


class TestIntegration(unittest.TestCase):

    def test_alphabet_die_creation(self):
        alphabet_die = load_alphabet_die('english_letters.txt')
        self.assertIsInstance(alphabet_die, Die)
        self.assertEqual(len(alphabet_die.show()), 26)

    def test_valid_words(self):
        alphabet_die = load_alphabet_die('english_letters.txt')
        dice = [alphabet_die for _ in range(5)]
        game = Game(dice)
        game.play(10)
        analyzer = Analyzer(game)
        valid_words = analyzer.valid_words('scrabble_words.txt')
        self.assertIsInstance(valid_words, pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
