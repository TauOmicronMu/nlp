import re
import nltk

# TODO: Sort out this list comp <3 
# filenames = ["]

data = ""
split_data = []
abstract = ""
with open("s_untagged/364.txt", "r") as f:
    data = f.read()
    split_data = re.split("[Aa]bstract\:", data)
    abstract = split_data[2]

print(abstract)

# Take the abstract and first split it into paragraphs by splitting on '\n\n'
paragraphs = abstract.split('\n\n')

# For each paragraph, tokenise them using the nltk.sent_tokenize() function.
sentences = [nltk.sent_tokenize(s) for s in paragraphs][1:]
print(sentences)
