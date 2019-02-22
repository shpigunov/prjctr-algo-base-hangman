"""
Module containing re-usable testing routines.
"""
import game
import matplotlib.pyplot as plt

def test(player_function, adv_function, word_list, n=1, verbose=False) -> int:
    """Test player strategy `player_function`
    against adversary strategy `adv_function`
    using wordlist `word_list` for `n` iterations.
    `verbose` enables verbose output to console."""
    
    g = game.Game(word_list, print_progress=verbose)
    
    for i in range(0, n):
        w = adv_function(g)
        g.set_word(w)
        player_function(g)
        
        if verbose:
            print(g.word_mask)
    
    return g.player_score

def plot(player_function, adv_function, word_list, 
              num_trials=1,
              max_attempts=8,
              max_word_length=8):
    
    # Initialize result matrix
    a = [[0 for c in range(0, max_attempts+1)] for r in range(1, max_word_length+1)]
    
    for m in range(1, max_attempts):
        for n in range(1, max_word_length):
            # New game
            g = game.Game(word_list, 
                          max_attempts=max_attempts, 
                          max_word_length=max_word_length,
                          print_progress=False)
            
            # Play num_trials rounds
            for i in range(0, num_trials):
                w = adv_function(g)
                g.set_word(w)
                player_function(g)
            
            a[m][n] = g.player_score
            del g
    
    a[0][0] = num_trials
    plt.imshow(a, cmap='hot', interpolation='nearest')
    plt.show()
            