# POS-tags the training data, and pickles the resulting array to save time when applying the 
# NER tagger.

import nltk
import pickle
import re

with open("wsj_untagged/concatstr.txt", "r") as f:
    tagged_data = nltk.pos_tag(re.findall(r'\w+', f.read()))
    pickle.dump(tagged_data, open("pos_tagged.p", "wb"))
