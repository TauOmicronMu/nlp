import nltk
import nltk.data
import re

from collections import Counter

FP = "wsj_training/concatstr.txt"
UFP = "wsj_untagged/concatstr.txt"
OFP = "output.txt"

tag_map = {
    "ORGANIZATION": "ORG",
    "PERSON": "PER",
    "LOCATION": "LOC"
}

# Load in the tagged data as a single string from the filepath.
data = ""
with open(FP, "r") as f:
    data = f.read()

# Load in extra tagged data.
moredata = ""
with open("more.txt", "r") as f:
    moredata = f.read()

def getAllOfType(t): return Counter ( re.findall(r'<ENAMEX TYPE="'+ t +'">(.*?)<\/ENAMEX>', data) + re.findall(r'' + tag_map[t] + '\W(.*)', moredata) )

organizations = getAllOfType("ORGANIZATION")
people = getAllOfType("PERSON")
locations = getAllOfType("LOCATION")

untagged_data = ""
with open(UFP, "r") as f:
    untagged_data = f.read()

untagged_words = re.findall(r'\w+', untagged_data)

def getScores(phrase):
    return (organizations[phrase], people[phrase], locations[phrase])

'''
    Given a word or list of words, tag them appropriately or 
    return the word(s) if no tags apply to them.
'''
def tag(words):
    concatw = ""
    i = 0
    for word in words:
        # Only add a space if there's >1 word
        if i != 0:
            concatw += word + " " 
        else:
            concatw = word

    scores = getScores(concatw)
    maxs = max(scores)

    if maxs == 0:
        return (word, False) # If it doesn't fit, return untagged text.
    if maxs == scores[0]:
        return ('<ENAMEX TYPE="ORGANIZATION">' + word + '</ENAMEX>', True)
    if maxs == scores[1]:
        return ('<ENAMEX TYPE="PERSON">' + word + '</ENAMEX>', True)
    if maxs == scores[2]:
        return ('<ENAMEX TYPE="LOCATION">' + word + '</ENAMEX>', True)

'''
    Given a list of words, attempt to tag phrases of length n, once
    the end of the list is reached, attempt to tag phrases of length
    n-1 and so on until n == 0.
'''
def ntag(words, n, currpos=0):
    # Terminate if there aren't enough words to form an n-length phrase.
    if currpos >= len(words) - 1 - n:
        print("Only ever got here")
        return ntag(words, n-1, 0)
    # Try to tag everything from [currpos:currpos+n+1] 
        ws = " ".join(words[currpos:currpos + n + 1])
        print("ws: %s" %ws)
        tws = tag(ws)
        if tag(ws)[1]: # If the given words were tagged...
            del words[currpos:currpos + n + 1] # Remove all the used words
            words[currpos] = tws[0] # Update the array with the tagged data
            return ntag(words, n, currpos + n + 1)
        # If the given words weren't tagged...
        return ntag(words, n, currpos + 1) # Just increment currpos
            
tagged_input = ntag(untagged_words, 3)

with open(OFP, "w") as f:
    f.write(" ".join(tagged_input))
