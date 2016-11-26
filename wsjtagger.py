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

# We can use this to tag new data in the following way:
#
# FOR WORD Wn in UNTAGGED_DATA
# IF Wn is the member of no dicts
#     IF Wn ++ W(n+1) is in a dict
#         Pass Wn ++ W(n+1) to the tagging function
#     ELSE
#         
# ELSE
#     IF Wn is the member of more than one dict
#         Tag Wn with the occurence with the highest value
#     ELSE
#          Tag Wn with the only tag it is assigned to. 

# Load in untagged data
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
        return word # If it doesn't fit, return untagged text.
    if maxs == scores[0]:
        return '<ENAMEX TYPE="ORGANIZATION">' + word + '</ENAMEX>'
    if maxs == scores[1]:
        return '<ENAMEX TYPE="PERSON">' + word + '</ENAMEX>'
    if maxs == scores[2]:
        return '<ENAMEX TYPE="LOCATION">' + word + '</ENAMEX>'

tagged_input = ""
for word in untagged_words:
       tagged_input += tag([word]) + " "

with open(OFP, "w") as f:
    f.write(tagged_input)
