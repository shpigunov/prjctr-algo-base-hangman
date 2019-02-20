"""
Player strategies.

Each strategy takes a `Game` object as a parameter in order to have access 
to the game's word list and other parameters.
"""

import random
import functions

# For debug only
from pprint import pprint as pp

def play0(game):
    """Drunken player - just pick random letters"""
    
    queue = [chr(x) for x in range(97, 123)]
    random.shuffle(queue)
    
    for c in queue:
        game.process_guess(c)
        
        if game.num_attempts >= game.max_attempts:
            break
            
        if '*' not in game.word_mask:
            break
            
def play1(game):
    """Computer player using fixed letter frequency in all words"""
    
    # Build histogram & queue of monograms, i.e. letters
    histogram = functions.build_ngram_histogram(game.word_list, n=1)
    queue = functions.build_letter_queue(histogram)
    
    while game.num_attempts < game.max_attempts:
        
        c = queue.pop(0)
        game.process_guess(c)
        
        if '*' not in game.word_mask:
            break
        
def play2(game):
    """Computer player using frequencies for words of known length"""
    
    # Filter word pool by length
    word_pool = functions.filter_words_by_length(
                                    words=game.word_list,
                                    length=game.word_length)
    
    # Build histogram & queue of monograms, i.e. letters
    histogram = functions.build_ngram_histogram(word_pool, n=1)
    queue = functions.build_letter_queue(histogram)

    while game.num_attempts < game.max_attempts:
        
        c = queue.pop(0)
        game.process_guess(c)

        if '*' not in game.word_mask:
            break

            
def play3(game):
    """Word list bisect-based player using only correct letters"""
    
    letter_inventory = [chr(x) for x in range(97, 123)]
    
    # Filter word pool by (empty) mask
    word_pool = functions.filter_words_by_mask(
                                    words=game.word_list,
                                    mask=game.word_mask)
    
    while game.num_attempts < game.max_attempts:
        
        # Since each correct guess updates the mask, rebuild letter frequency histogram & queue
        histogram = functions.build_letter_histogram(word_pool)
        queue = [c for c in functions.build_letter_queue(histogram) if c in letter_inventory]
        
        c = queue.pop(0)
        letter_inventory.remove(c)
        game.process_guess(c)
        
        # Re-filter by updated mask
        word_pool = functions.filter_words_by_mask(
                                words=game.word_list,
                                mask=game.word_mask)
        
        if '*' not in game.word_mask:
            break

            
def play9(game):
    """n-gram based computer player
    Reference: http://norvig.com/mayzner.html"""
    
    # Filter word pool by length
    word_pool = functions.filter_words_by_length(
                                    words=game.word_list,
                                    length=game.word_length)
    
    # Create and populate index of ngrams
    ngrams = {}
    for n in range(1, game.word_length):
        ngrams[n] = functions.build_ngram_histogram(word_pool, n)
    
    pp(ngrams)
    
    # TODO: Further elaborate this solver