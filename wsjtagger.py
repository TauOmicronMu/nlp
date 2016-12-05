import nltk
import nltk.data
import re
import requests
import pickle
import sys

from itertools import * 
from collections import Counter

FP = "wsj_training/concatstr.txt"
UFP = "wsj_untagged/concatstr.txt"
OFP = "output.txt"

OTAG = '<ENAMEX TYPE="ORGANIZATION">%s</ENAMEX>'
PTAG = '<ENAMEX TYPE="PERSON">%s</ENAMEX>'
LTAG = '<ENAMEX TYPE="LOCATION">%s</ENAMEX>'

tag_map = {
    "ORGANIZATION": "ORG",
    "PERSON": "PER",
    "LOCATION": "LOC"
}

def intersperse(iterable, delimiter):
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter
        yield x

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

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

def getScores(phrase):
    return (organizations[phrase], people[phrase], locations[phrase])

'''
    Given a word or list of words, tag them appropriately or 
    return the word(s) if no tags apply to them.
'''
def tag(words):
    enamex_pattern = re.compile("<ENAMEX\WTYPE='untagged'>(.*?)<\/ENAMEX>$")
    concatw = "".join(intersperse(words, " "))
    enamex_match = enamex_pattern.match(concatw)

    # If this isn't a proper noun phrase - ignore it to save time.
    if(enamex_match == None):
        return (concatw, False) 
    
    lookup_phrase = enamex_match.groups()[0] # We only care about what's inside the tags

    scores = getScores(lookup_phrase)
    maxs = max(scores)

    if maxs != 0: # If we've seen the phrase before, tag it based on where we've seen it most
        if maxs == scores[0]:
            return (OTAG %lookup_phrase, True)
        if maxs == scores[1]:
            return (PTAG %lookup_phrase, True)
        if maxs == scores[2]:
            return (LTAG %lookup_phrase, True)
 
    # If we've never seen the whole phrase before, see if we've seen individual parts of it
    powerlist = ["".join(list(intersperse(x, " "))) for x in list(powerset(lookup_phrase.split(" ")))][1:-1] 
    pscores = [] 
    maxes = []
    
    for part in powerlist:
        tempscores = getScores(part)
        pscores.append(tempscores)
        maxes.append(max(tempscores))
   
    mscore = 0
    try:
        mscore = max(maxes)
    except:    
        pass
 
    if mscore != 0:
        max_scores = pscores[maxes.index(mscore)] # Get our three "max scores". 

        if mscore == max_scores[0]:
            return (OTAG %lookup_phrase, True)
        if mscore == max_scores[1]:
            return (PTAG %lookup_phrase, True)
        if mscore == max_scores[2]:
            return (LTAG %lookup_phrase, True)

    # If we still have no idea what it is... make a GET request to the DBPedia API
    query = requests.get("http://lookup.dbpedia.org/api/search.asmx/KeywordSearch?MaxHits=1&QueryString=%s"%lookup_phrase).text  
    # Check if the data contains any labels for organization, location or person
    org_labels = re.findall(r'<Label>.*?organization.*?</Label>', query) 
    loc_labels = re.findall(r'<Label>.*?place.*?</Label>', query)
    per_labels = re.findall(r'<Label>.*?person.*?</Label>', query)
    print(org_labels)
    print(loc_labels)
    print(per_labels)
    return (lookup_phrase, True) # We weren't able to tag it, so 'untag' it and pretend it was tagged.
    
def ntag(words, n=0):
    if n < 0:
        return words
    currpos = 0
    
    # If there aren't enough words to form an n-length phrase,
    # Terminate and run ntag on words and n-1.
    while not (currpos >= len(words) -1 - n):
        # print("In while loop, currpos: %s, n: %s" %(currpos, (len(words)-1-n)))
        # Try to tag everything from [currpos:currpos+n+1]
        tws = tag(words[currpos:currpos+n+1])
        if tws[1]: 
            del words[currpos:currpos+n] # Remove the used words
            words[currpos] = tws[0] # Replace them with the tagged words
        currpos += 1 # Just increment currpos
    return ntag(words, n-1) # Termination step

def chunk(cdata):
    currpos = 0 # This is where we are in our data.
    while(currpos < len(cdata)):
        if cdata[currpos][1] == "NNP": # If we're at the start of a noun phrase...
            chunk = takewhileNNP(cdata, currpos)
            phrase = "<ENAMEX TYPE='untagged'>%s</ENAMEX>" %chunk[0] # Chunk all successive NNPs with this one and empty-tag
            del cdata[currpos:currpos+chunk[1]-1] # Remove the chunked words
            cdata[currpos] = phrase # Replace the chunked words with the amalgamated phrase
        else:
            cdata[currpos] = cdata[currpos][0] # Just take the string part of the tuple.
        currpos += 1
    return cdata

def takewhileNNP(tdata, currpos):
    op = currpos
    acc = ""
    while(tdata[currpos][1] == "NNP"):
        if(op != currpos):
            acc += " "
        acc += tdata[currpos][0] 
        currpos += 1
        
        if(currpos >= len(tdata)-1):
            return (acc, currpos-op)
    return (acc, currpos-op)

TOTAL = 1
filenames = ["wsj_%s.txt" %str(n).zfill(4) for n in range(1,TOTAL+1)]

for file in filenames:
    if(file != "wsj_1296.txt"): # This one breaks stuff so just ignore it for now.
        print(file)
        fdata = ""
        with open("wsj_untagged/"+file, "r") as f:
            fdata = f.read() # Grab the contents of the file
        pos_tagged_fdata = nltk.pos_tag(re.findall(r'\w+', fdata)) # pos-tag the contents
        chunked_data = chunk(pos_tagged_fdata) # Chunk the pos-tagged data
        tagged_data = ntag(chunked_data) # Tag the chunked data
        with open("wsj_tagged/"+file, "w") as f:
            f.write(" ".join(tagged_data)) # Append the tagged data to the output file.
    else:
        with open("wsj_tagged/"+file, "w") as f:
            f.write(open("wsj_untagged/"+file,"r").read())
