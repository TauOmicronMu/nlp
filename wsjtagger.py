import nltk
import nltk.data
import re
import pickle

from itertools import * 
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
    firstw = True
    for word in words:
        # Only add a space if there's >1 word
        if firstw:
            concatw += word[0]
            firstw = False
        else:
            concatw += " " + word[0]

    scores = getScores(concatw)
    maxs = max(scores)

    if maxs == 0:
        return (concatw, False) # If it doesn't fit, return untagged text.
    if maxs == scores[0]:
        return ('<ENAMEX TYPE="ORGANIZATION">' + concatw + '</ENAMEX>', True)
    if maxs == scores[1]:
        return ('<ENAMEX TYPE="PERSON">' + concatw + '</ENAMEX>', True)
    if maxs == scores[2]:
        return ('<ENAMEX TYPE="LOCATION">' + concatw + '</ENAMEX>', True)

def ntag(words, n):
    if n < 0:
        return words
    currpos = 0
    # If there aren't enough words to form an n-length phrase,
    # Terminate and run ntag on words and n-1.
    while not (currpos >= len(words) -1 - n):
        print("In while loop, currpos: %s, n: %s" %(currpos, (len(words)-1-n)))
        # Try to tag everything from [currpos:currpos+n+1]
        tws = tag(words[currpos:currpos+n+1])
        if tws[1]: 
            del words[currpos:currpos + n + 1] # Remove the used words
            words[currpos] = tws[0] # Replace them with the tagged words
        currpos += 1 # Just increment currpos
    return ntag(words, n-1) # Termination step

def chunk(cdata):
    currpos = 0 # This is where we are in our data.
    while(currpos != len(cdata)):
        if cdata[currpos][1] == "NNP": # If we're at the start of a noun phrase...
            iphrase = takewhile(lambda x: x[1] == "NNP", cdata) 
            phrase = "<ENAMEX type='none'>".join(iphrase) + "</ENAMEX" # Chunk all successive NNPs with this one and empty-tag
            del cdata[currpos:currpos+len(listify(iphrase))] # Remove the chunked words
            cdata[currpos] = phrase # Replace the chunked words with the amalgamated phrase
            currpos += 1
        currpos += 1
    return cdata

# First, chunk the pos-tagged data
pos_tagged_data = pickle.load(open("pos_tagged.p", "rb"))
chunked_data = chunk(pos_tagged_data)

tagged_input = ntag(chunked_data, 5)

with open(OFP, "w") as f:
    f.write(" ".join(tagged_input))
