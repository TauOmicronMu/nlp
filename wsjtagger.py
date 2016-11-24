import nltk
import nltk.data
import re

from collections import Counter

FP = "wsj_training/concatstr.txt"
UFP = "wsj_untagged/concatstr.txt"

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

def tag(text):
    organizations_score = organizations[text]
    people_score = people[text]
    locations_score = locations[text]

    maxs = max(organizations_score, people_score, locations_score)
    
    if maxs == 0:
        return text # If it doesn't fit, return untagged text.

    if maxs == organizations_score:
        return '<ENAMEX TYPE="ORGANIZATION">' + text + '</ENAMEX>'
    if maxs == people_score:
        return '<ENAMEX TYPE="PERSON">' + text + '</ENAMEX>'
    if maxs == locations_score:
        return '<ENAMEX TYPE="LOCATION">' + text + '</ENAMEX>'

tagged_input = ""
for word in untagged_words:
       tagged_input += tag(word) + " "

print(tagged_input)
