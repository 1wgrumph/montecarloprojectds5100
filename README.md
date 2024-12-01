# montecarloprojectds5100
Final Project

Monte Carlo Simulation Project
Overview
This project implements a Monte Carlo simulation package designed for a variety of use cases, including dice games, statistical analysis, and word validation. It is structured as a Python package with three core classes: Die, Game, and Analyzer. The project also includes unit tests and supporting documentation.

Features
Die Class: Represents a customizable die with user-defined faces and weights.
Game Class: Manages multiple dice and rolls them in a game setting.
Analyzer Class: Provides statistical analysis on game outcomes, such as jackpots, face counts, and valid Scrabble words.
Integration with External Data:
english_letters.txt: Used for creating a weighted alphabet die.
scrabble_words.txt: Used for validating permutations of rolled letters against a Scrabble word list.
Unit Tests: Comprehensive tests for all classes and methods using Python's unittest framework.

Die Class
from montecarlo import Die

# Create a die with faces A, B, C
die = Die(['A', 'B', 'C'])

# Change the weight of face 'A'
die.change_weight('A', 2.5)

# Roll the die 10 times
rolls = die.roll(10)

# Show the current state of the die
print(die.show())

Game Class 
from montecarlo import Game, Die

# Create three dice
dice = [Die(['A', 'B', 'C']) for _ in range(3)]

# Initialize the game
game = Game(dice)

# Play the game with 10 rolls
game.play(10)

# Show the results in wide format
print(game.show('wide'))

# Show the results in narrow format
print(game.show('narrow'))

Analyzer
from montecarlo import Analyzer, Game, Die

# Create a game with three dice
dice = [Die(['A', 'B', 'C']) for _ in range(3)]
game = Game(dice)
game.play(10)

# Analyze the game
analyzer = Analyzer(game)

# Calculate jackpots
print("Number of jackpots:", analyzer.jackpot())

# Get face counts per roll
print(analyzer.face_counts_per_roll())

# Get combination counts
print(analyzer.combo_count())

# Get permutation counts
print(analyzer.permutation_count())

Valid Words Analysis 
from montecarlo import load_alphabet_die, Analyzer, Game

# Create an alphabet die using english_letters.txt
alphabet_die = load_alphabet_die('english_letters.txt')

# Create a game with five alphabet dice
dice = [alphabet_die for _ in range(5)]
game = Game(dice)
game.play(10)

# Analyze valid words using scrabble_words.txt
analyzer = Analyzer(game)
valid_words = analyzer.valid_words('scrabble_words.txt')
print(valid_words)

Unit Testing 
python -m unittest montecarlo_test.py
