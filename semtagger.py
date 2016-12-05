import re
import nltk
import itertools

# TODO: Sort out this list comp <3 
# filenames = ["]

def intersperse(iterable, delimiter):
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter
        yield x

data = ""
split_data = []
header = ""
abstract_word = ""
abstract = ""
with open("s_untagged/364.txt", "r") as f:
    data = f.read()
    split_data = re.split("[Aa]bstract\:", data)
    header = split_data[0]
    abstract_word = split_data[1]
    abstract = split_data[2]

print(abstract)

# Take the abstract and first split it into paragraphs by splitting on '\n\n'
paragraphs = abstract.split('\n\n')

# For each paragraph, tokenise them using the nltk.sent_tokenize() function.
sentences = [nltk.sent_tokenize(s) for s in paragraphs][1:]


