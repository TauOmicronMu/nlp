from collections import Counter

import re
import string

def words(text):
    return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

TOTAL = sum(WORDS.values())

ALPHABET = list(string.ascii_lowercase)

def P(word):
    return WORDS[word]/TOTAL

"""
    Returns all words that have a manhattan distance of 1 from the initial word
    This is achieved by inserting each letter from the alphaber into each position
    in the word, as well as replacing each letter with it.
"""
def edits1(word):
    word = word.lower() # Normalise everything to lowercase
    
    words = set()

    for letter in ALPHABET:
        # First, generate the words that are the result of directly replacing letters
        for i in range(len(word)):
            words.add(word[:i] + letter + word[i+1:])
        # Now generate the words that are the result of adding letters to the start or end
            words.add(letter + word)
            words.add(word + letter)
        # Now generate the words that are the result of inserting letters into the word
            words.add(word[:i] + letter + word[i:])

    print(len(words))
