import re
import nltk
import itertools

def intersperse(iterable, delimiter):
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter
        yield x

tag_pattern = re.compile('<ENAMEX\WTYPE=.*?>.*?<\/ENAMEX>')

# First, evaluate the tagger given the whole tagged data for the untagged data.
exemplar_tagged = ""
my_tagged_whole = ""
punct = " !#$%&()*+,-.:;?@[\]^_`{|}~"

total = 0
correctly_tagged_whole = 0
correctly_tagged_half = 0
correctly_tagged_quarter = 0 

filenames = ["wsj_%s.txt" %str(n).zfill(4) for n in range(1,2001)]

def strip(s):
    return "".join([c for c in s if c not in punct])

for file in filenames:
    with open("wsj_training/%s"%file, "r") as f:
        exemplar_tagged = f.read()
    with open("wsj_tagged_whole/%s"%file, "r") as f:
        my_tagged_whole = f.read()
    with open("wsj_tagged_half/%s"%file, "r") as f:
        my_tagged_half = f.read()
    with open("wsj_tagged_quarter/%s"%file, "r") as f:
        my_tagged_quarter = f.read()

    exemplar_tags = list(map(strip, tag_pattern.findall(exemplar_tagged)))
    my_tags_whole = list(map(strip, tag_pattern.findall(my_tagged_whole)))
    my_tags_half = list(map(strip, tag_pattern.findall(my_tagged_half)))
    my_tags_quarter = list(map(strip, tag_pattern.findall(my_tagged_quarter)))

    if(file != "wsj_1296.txt"):
        for tag in exemplar_tags:
            total += 1
            if tag in my_tags_whole:
                correctly_tagged_whole += 1
            if tag in my_tags_half:
                correctly_tagged_half += 1
            if tag in my_tags_quarter:
                correctly_tagged_quarter += 1

accuracy_whole = (correctly_tagged_whole/total)*100 
accuracy_half = (correctly_tagged_half/total)*100
accuracy_quarter = (correctly_tagged_quarter/total)*100

with open("evalresults.txt", "w") as f:
    f.write("")

with open("evalresults.txt", "a") as f:
    f.write("Accuracy (100 Trained): %s" %accuracy_whole + "\n") 
    f.write("Accuracy (50 Trained): %s" %accuracy_half + "\n")
    f.write("Accuracy (25 Trained): %s" %accuracy_quarter + "\n")

