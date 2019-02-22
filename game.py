import random
import functions


class Game(object):
    """Hangman game class. Contains game properties, round information
    and rules for handling player guesses."""

    def __init__(self, 
                 word_list, 
                 max_attempts=8, 
                 max_word_length=24, 
                 print_progress=False):
        
        # Immutable game properties - these should not be changed
        # during the game
        self.word_list = word_list
        self.max_attempts = max_attempts
        self.max_word_length = max_word_length
        self.print_progress = print_progress
        
        # Round info
        self.num_attempts = 0
        self.__word = ''
        self.word_mask = ''
        self.word_length = 0
        
        # Scores - they should persist throughout the lifetime 
        # of the game object
        self.player_score = 0
        self.adversary_score = 0

    def reset_round(self):
        """Start new round with a new word and reset # of attempts"""
        self.word_length = len(self.__word)
        self.word_mask = '*' * self.word_length
        self.num_attempts = 0

    def set_word(self, word):
        """Set arbitrary word to play against"""
        self.__word = word
        self.reset_round()

    def print_word(self):
        """Print current word to console. For debug use."""
        print(self.__word)
        
    def process_guess(self, letter):
        """Process player guess"""

        letters_guessed = 0
        for i in range(0, len(self.__word)):
            if letter == self.__word[i]:
                self.word_mask = self.word_mask[:i] + letter + self.word_mask[i+1:]
                if self.print_progress:
                    print("Correct! ", self.word_mask)
                letters_guessed += 1
        if letters_guessed == 0:
            self.num_attempts += 1
            if self.print_progress:
                print("Incorrect. Attempts left: %s" % str(self.max_attempts - self.num_attempts))
        if '*' not in self.word_mask:
            self.player_score += 1
        
        # Return bool value to inform player of successful/failed guess
        if letters_guessed > 0:
            return True
        else:
            return False

