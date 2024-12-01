import numpy as np
import pandas as pd


class Die:
    """
    A class representing a die with customizable faces and weights.
    """

    def __init__(self, faces):
        """
        Initialize the die with unique faces and default weights of 1.0.

        :param faces: A list or array of unique faces.
        """
        self.faces = np.array(faces)
        self.weights = np.ones(len(faces), dtype=float)
        self._die_df = pd.DataFrame({'Face': self.faces, 'Weight': self.weights})

    def change_weight(self, face, new_weight):
        """
        Change the weight of a specific face.

        :param face: The face of the die to update.
        :param new_weight: The new weight (must be numeric).
        """
        if face not in self.faces:
            raise ValueError("Face not found in die.")
        if not isinstance(new_weight, (int, float)):
            raise ValueError("Weight must be a numeric value.")
        self._die_df.loc[self._die_df['Face'] == face, 'Weight'] = float(new_weight)

    def roll(self, n_rolls=1):
        """
        Roll the die n times.

        :param n_rolls: The number of rolls.
        :return: A list of outcomes.
        """
        return self._die_df['Face'].sample(n=n_rolls, weights=self._die_df['Weight'], replace=True).tolist()

    def show(self):
        """
        Show the current state of the die.

        :return: A DataFrame showing faces and weights.
        """
        return self._die_df.copy()


class Game:
    """
    A class representing a game involving one or more dice.
    """

    def __init__(self, dice):
        """
        Initialize the game with a list of dice.

        :param dice: A list of Die objects.
        """
        if not all(isinstance(die, Die) for die in dice):
            raise ValueError("All elements must be instances of the Die class.")
        self.dice = dice
        self._results = None

    def play(self, n_rolls):
        """
        Play the game by rolling all dice n times.

        :param n_rolls: The number of rolls.
        """
        results = {f"Die {i+1}": die.roll(n_rolls) for i, die in enumerate(self.dice)}
        self._results = pd.DataFrame(results)

    def show(self, form="wide"):
        """
        Show the results of the most recent game.

        :param form: "wide" for wide format, "narrow" for narrow format.
        :return: A DataFrame of results.
        """
        if self._results is None:
            raise ValueError("No results available. Play the game first.")
        if form == "wide":
            return self._results
        elif form == "narrow":
            return self._results.melt(var_name="Die", value_name="Outcome")
        else:
            raise ValueError("Form must be 'wide' or 'narrow'.")


class Analyzer:
    """
    A class for analyzing the results of a game.
    """

    def __init__(self, game):
        """
        Initialize the analyzer with a game object.

        :param game: A Game object.
        """
        if not isinstance(game, Game):
            raise ValueError("Input must be an instance of the Game class.")
        self.game = game
        self.results = game.show("wide")

    def jackpot(self):
        """
        Count how many rolls resulted in all dice showing the same face.

        :return: An integer count of jackpots.
        """
        return (self.results.nunique(axis=1) == 1).sum()

    def face_counts_per_roll(self):
        """
        Count the occurrences of each face in each roll.

        :return: A DataFrame of face counts.
        """
        return self.results.apply(pd.Series.value_counts, axis=1).fillna(0).astype(int)

    def combo_count(self):
        """
        Count distinct combinations of faces rolled.

        :return: A DataFrame of combinations and their counts.
        """
        combos = self.results.apply(lambda x: tuple(sorted(x)), axis=1)
        return combos.value_counts().reset_index(name="Count").rename(columns={"index": "Combination"})

    def permutation_count(self):
        """
        Count distinct permutations of faces rolled.

        :return: A DataFrame of permutations and their counts.
        """
        perms = self.results.apply(tuple, axis=1)
        return perms.value_counts().reset_index(name="Count").rename(columns={"index": "Permutation"})

    def valid_words(self, scrabble_words_file):
        """
        Count valid Scrabble words formed by letter permutations.

        :param scrabble_words_file: Path to the Scrabble words file.
        :return: A DataFrame of valid words and their counts.
        """
        # Load valid words
        with open(scrabble_words_file, 'r') as file:
            valid_words = set(word.strip().upper() for word in file.readlines())

        # Check permutations
        def find_valid_words(row):
            return [word for word in set(row) if word in valid_words]

        permutations = self.results.apply(tuple, axis=1)
        valid = permutations.apply(find_valid_words).explode()
        return valid.value_counts().reset_index(name="Count").rename(columns={"index": "Valid Word"})


# Example: Loading `english_letters.txt` and creating a weighted alphabet die
def load_alphabet_die(file_path):
    """
    Create a Die instance for the English alphabet weighted by letter frequency.

    :param file_path: Path to the `english_letters.txt` file.
    :return: A Die object.
    """
    letter_weights = pd.read_csv(file_path, sep=" ", header=None, names=["Letter", "Frequency"])
    letter_weights["Weight"] = letter_weights["Frequency"] / letter_weights["Frequency"].sum()
    alphabet_die = Die(letter_weights["Letter"].values)
    for letter, weight in zip(letter_weights["Letter"], letter_weights["Weight"]):
        alphabet_die.change_weight(letter, weight)
    return alphabet_die
