import nltk
import nltk.data
import re

from collections import Counter

FP = "wsj_training/concatstr.txt"

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

print(organizations.most_common(10))
print(people.most_common(10))
print(locations.most_common(10))

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


