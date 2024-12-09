import unittest
import pandas as pd
import numpy as np
from montecarlo import Die, Game, Analyzer, load_alphabet_die


class TestDie(unittest.TestCase):

    def setUp(self):
        self.die = Die(['A', 'B', 'C'])

    def test_initial_weights(self):
        self.assertTrue((self.die._die_df['Weight'] == 1.0).all())
        print("TestDie: test_initial_weights passed")

    def test_change_weight(self):
        self.die.change_weight('A', 2.5)
        self.assertEqual(self.die._die_df.loc[self.die._die_df['Face'] == 'A', 'Weight'].values[0], 2.5)
        print("TestDie: test_change_weight passed")

    def test_invalid_weight_change(self):
        with self.assertRaises(ValueError):
            self.die.change_weight('D', 2.0)
        print("TestDie: test_invalid_weight_change passed")

    def test_roll(self):
        rolls = self.die.roll(5)
        self.assertEqual(len(rolls), 5)
        self.assertTrue(set(rolls).issubset({'A', 'B', 'C'}))
        print("TestDie: test_roll passed")

    def test_show(self):
        df = self.die.show()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)
        print("TestDie: test_show passed")


class TestGame(unittest.TestCase):

    def setUp(self):
        self.dice = [Die(['A', 'B', 'C']) for _ in range(3)]
        self.game = Game(self.dice)

    def test_play(self):
        self.game.play(10)
        self.assertEqual(len(self.game._results), 10)
        print("TestGame: test_play passed")

    def test_show_wide(self):
        self.game.play(5)
        results = self.game.show('wide')
        self.assertEqual(results.shape[0], 5)
        print("TestGame: test_show_wide passed")

    def test_show_narrow(self):
        self.game.play(5)
        results = self.game.show('narrow')
        self.assertEqual(len(results), 15)  # 5 rolls * 3 dice
        print("TestGame: test_show_narrow passed")


class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        dice = [Die(['A', 'B', 'C']) for _ in range(3)]
        self.game = Game(dice)
        self.game.play(10)
        self.analyzer = Analyzer(self.game)

    def test_jackpot(self):
        jackpots = self.analyzer.jackpot()
        self.assertGreaterEqual(jackpots, 0)
        print("TestAnalyzer: test_jackpot passed")

    def test_face_counts_per_roll(self):
        face_counts = self.analyzer.face_counts_per_roll()
        self.assertIsInstance(face_counts, pd.DataFrame)
        self.assertEqual(face_counts.shape[0], 10)
        print("TestAnalyzer: test_face_counts_per_roll passed")

    def test_combo_count(self):
        combos = self.analyzer.combo_count()
        self.assertIsInstance(combos, pd.DataFrame)
        print("TestAnalyzer: test_combo_count passed")

    def test_permutation_count(self):
        permutations = self.analyzer.permutation_count()
        self.assertIsInstance(permutations, pd.DataFrame)
        print("TestAnalyzer: test_permutation_count passed")


class TestIntegration(unittest.TestCase):

    def test_alphabet_die_creation(self):
        alphabet_die = load_alphabet_die('english_letters.txt')
        self.assertIsInstance(alphabet_die, Die)
        self.assertEqual(len(alphabet_die.show()), 26)
        print("TestIntegration: test_alphabet_die_creation passed")

    def test_valid_words(self):
        alphabet_die = load_alphabet_die('english_letters.txt')
        dice = [alphabet_die for _ in range(5)]
        game = Game(dice)
        game.play(10)
        analyzer = Analyzer(game)
        valid_words = analyzer.valid_words('scrabble_words.txt')
        self.assertIsInstance(valid_words, pd.DataFrame)
        print("TestIntegration: test_valid_words passed")


if __name__ == '__main__':
    unittest.main()
