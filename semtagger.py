import re
import nltk
import itertools
import wsjtagger

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
stime = ""
etime = ""
speaker = ""

with open("s_untagged/362.txt", "r") as f:
    data = f.read()
    
    # This next bit is kinda awful but re.split was giving me some issues...
    # Split on newlines
    lines = data.split("\n")
    # Look through to find the start of the abstract   
    abstract_pattern = re.compile("[Aa]bstract\:\W+")
    for line in lines:
        matches = abstract_pattern.findall(line)
        if matches != []: # Yay, we found the abstract!
            pos = lines.index(matches[0])
            # Reconstruct the initial strings by interposing newlines etc.
            header = "".join(intersperse(lines[:pos], "\n"))
            abstract_word = "".join(lines[pos])
            abstract = "".join(intersperse(lines[pos+1:], "\n"))
    
# Take the abstract and first split it into paragraphs by splitting on '\n\n'
paragraphs = abstract.split('\n\n')

# For each paragraph, tokenise them using the nltk.sent_tokenize() function.
sentences = [nltk.sent_tokenize(s) for s in paragraphs][1:]

header_lines = header.split("\n")

# Get all matches of a regex pattern on a header (or any string)
def get_matches(headerl, pattern):
    matches = []
    for line in headerl:
        matches.append(pattern.findall(line))
    return [item for x in matches if x != [] for item in x]

time_line_pattern = re.compile("[Tt]ime\:([\W\w]*)")
times = get_matches(header_lines, time_line_pattern)    
if(times): # If the header contains a 'Time' line
    # If our time is in the format '(h)h:mm - (h)h:mm' split it into start time and end time
    time_pattern = re.compile("([0-9]{1,2}\:?([0-9]{2})?(([Aa]|[Pp])[Mm])?)")
    # If this matches, it is in the form (1) - (5) ---> i.e. the 1st match is the 1st time, the 5th is the 2nd time.
    dbl_time_pattern = re.compile("([0-9]{1,2}\:?([0-9]{2})?(([Aa]|[Pp])[Mm])?)\W*?([0-9]{1,2}\:?([0-9]{2})?(([Aa]|[Pp])[Mm])?)")
    dbl_time_matches = get_matches(times, dbl_time_pattern)
    if(dbl_time_matches):
        stime = dbl_time_matches[0][0] 
        etime = dbl_time_matches[0][4]

print(stime)
print(etime)   
speaker_pattern = re.compile("[Ww][Hh][Oo]\:([\W\w]*)|[Ss][Pp][Ee][Aa][Kk][Ee][Rr]\:([\W\w]*)")
speakers = get_matches(header_lines, speaker_pattern)
print(speakers)
