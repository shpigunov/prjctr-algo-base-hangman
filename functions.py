# Shared functions reusable across the project

def filter_words_by_length(words: list, length: int) -> list:
    """Filter word list to a subset only containing words
    of specified length"""

    return [w for w in words if len(w) == length]


def filter_words_by_mask0(words: list, mask: str) -> list:
    """Filter word list to a subset only matching known
    characters in a word mask

    Mask format: 'ch*r*cter'"""

    res = []                # resulting list
    mask_len = len(mask)    # mask length for reuse

    for i in range(0, len(words)):
        include = True
        # Only include words that are the same length as mask
        if len(words[i]) == mask_len:
            for j in range(0, mask_len):
                if mask[j] != words[i][j] and mask[j] != '*':
                    include = False
                    break
        else:
            include = False

        if include:
            res.append(words[i])

    return res


def filter_words_by_mask(words: list, mask: str) -> list:
    """Filter word list to a subset only matching known
    characters in a word mask

    Mask format: 'ch*r*cter'"""

    res = []                # resulting list
    mask_len = len(mask)    # mask length for reuse

    for word in words:
        include = True
        # Only include words that are the same length as mask
        if len(word) == mask_len:
            for j in range(0, mask_len):
                if mask[j] != word[j] and mask[j] != '*':
                    include = False
                    break
        else:
            include = False

        if include:
            res.append(word)

    return res


def calculate_frequency_histogram(histogram) -> dict:
    res = {}

    for key in histogram.keys():
        if key != "_total":
            res[key] = histogram[key] / histogram["_total"]

    del res["-"]

    return res


def find_max_length(words) -> int:
    """Return length of longest word in list"""

    return max([len(w) for w in words])


def build_letter_histogram(words, include_total=False) -> dict:
    """Build frequency histogram for each letter in a list of words
    of specified length.
    :param words: [''] - list of words to build from"""

    histogram = {}
    total = 0

    for word in words:
        word = word.lower()
        for letter in word:
            if not letter in histogram:
                histogram[letter] = 1
            else:
                histogram[letter] += 1
            total += 1
    
    # Optionally include total letter tally
    # (e.g. to compute percentages)
    if include_total:
        histogram["_total"] = total

    return histogram


def build_ngram_histogram(words, n=1, include_total=False) -> dict:
    """Build frequency histogram for each n-gram in a list of words
    of specified length.
    :param words: [''] - list of words to build from
    :param n: int - length of n-gram. Monograms=single letters (default)
    :param include_total: bool - include totals in the histogram"""
    
    histogram = {}
    total = 0
    
    for word in words:
        for ngram in [word[i:i+n] for i in range(len(word)-1)]:
            if ngram not in histogram:
                histogram[ngram] = 1
            else:
                histogram[ngram] += 1
    
    # Optionally include total letter tally
    # (e.g. to compute percentages)
    if include_total:
        histogram["_total"] = total

    return histogram


def build_letter_queue(histogram) -> list:
    queue = []

    for key, value in sorted(histogram.items(), key=lambda x: x[1]):
        queue.append(key)

    return queue[::-1]


def build_ngram_histogram(words, n=1, include_total=False) -> dict:
    
    histogram = {}
    total = 0
    
    for word in words:
        for ngram in [word[i:i+n] for i in range(len(word)-1)]:
            if ngram not in histogram:
                histogram[ngram] = 1
            else:
                histogram[ngram] += 1
    
    # Optionally include total letter tally
    # (e.g. to compute percentages)
    if include_total:
        histogram["_total"] = total

    return histogram


def calculate_letter_difficulty(word_dict) -> dict:
    """Calculate letter difficulty map"""
    
    letter_diff = {}
    letter_freq = {}
    weighted_letter_diff = {}
    
    # Since we observe that the shorter the word is, 
    # the harder it's to guess,
    # letter difficulty is reverse to word length
    
    for word in word_dict.keys():
        avg_letter_diff = int(word_dict[word]) * len(word)
        
        # Assuming that "difficult" letters show up 
        # more often in difficult words
        for c in word:
            # Count summary difficulty
            if c not in letter_diff:
                letter_diff[c] = avg_letter_diff
            else:
                letter_diff[c] += avg_letter_diff
            
            # Count letter occurrence
            if c not in letter_freq:
                letter_freq[c] = 1
            else:
                letter_freq[c] += 1          
    
    for c in letter_diff.keys():
        weighted_letter_diff[c] = letter_diff[c] / letter_freq[c]
    
    return weighted_letter_diff
        
        
def assess_word_difficulty(word, dic) -> int:
    """Evaluate word difficulty level"""
    return sum([dic[c] for c in word]) / len(word)


def build_scorecard(filename) -> dict:
    
    f = open('play3.csv', 'r')
    scorecard = {}
    for line in f.readlines():
        word, difficulty = line.split(',')
        scorecard[word.lower()] = int(difficulty)
    f.close()
    
    return scorecard

def print_frequency_histogram(words):
    h = build_letter_histogram(words)
    f = calculate_frequency_histogram(h)
    sorted_by_value = sorted(f.items(), key=lambda kv: kv[1])[::-1]
    try:
        pp(sorted_by_value)
    except NameError:
        print(sorted_by_value)