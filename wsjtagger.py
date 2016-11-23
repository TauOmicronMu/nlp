import nltk
import nltk.data

FP = "wsj_training/concatstr.txt"

# Load in the tagged data as a single string from the filepath.
data = ""
with open(FP, "r") as f:
    data = f.read()


