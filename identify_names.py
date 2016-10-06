import nltk

def get_names(text):
    tokenized_text = nltk.word_tokenize(text)
    print(tokenized_text)

print(get_names("Tom, Bede and Aran"))
