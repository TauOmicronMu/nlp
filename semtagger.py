import re
import nltk
import itertools
import wsjtagger

filenames = [310]

def intersperse(iterable, delimiter):
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter
        yield x

def dropWhile(s, f):
    if f(s[0]):
        return dropWhile(s[1:], f)
    return s

def keepWhile(s, f):
    if not s:
        return ""
    if f(s[0]):
        return s[0] + keepWhile(s[1:], f)
    return ""

titles = ["Professor", "Prof", "Dr", "Doctor", "Mr", "Mrs", "Miss", "Ms", "Mx", "prof", "professor", "dr", "doctor", "mr", "mrs", "miss", "ms" "mx"]
person_pattern = re.compile("<ENAMEX\sTYPE='PERSON'>(.*?)</ENAMEX>") 
punct = "!#$%&()*+,-.:;?@[\]^_`{|}~"

for file in filenames:

    data = None
    split_data = None
    header = None
    abstract_word = None
    abstract = None
    stime = None
    etime = None
    speaker = None
    speaker_title = None

    with open("s_untagged/%s.txt"%file, "r") as f:
        data = f.read()
    
        # This next bit is kinda awful but re.split was giving me some issues...
        # Split on newlines
        lines = data.split("\n")
        # Look through to find the start of the abstract   
        abstract_pattern = re.compile("[Aa]bstract\:\s+")
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
    for i in range(len(paragraphs)):
        paragraphs[i] = nltk.sent_tokenize(paragraphs[i])
    #TODO: MAKE SURE THIS ACTUALLY WORKS FOR SENTENCES ^
    #TODO: TOM THIS IS SUPER IMPORTANT... DO THIS!

    header_lines = header.split("\n")

   # Get all matches of a regex pattern on a header (or any string)
    def get_matches(headerl, pattern):
        matches = []
        for line in headerl:
            matches.append(pattern.findall(line))
        return [item for x in matches if x != [] for item in x]

    time_line_pattern = re.compile(r"[Tt]ime\:([\W\w]*)")
    times = get_matches(header_lines, time_line_pattern)    
    if(times): # If the header contains a 'Time' line
        # If our time is in the format '(h)h:mm - (h)h:mm' split it into start time and end time
        time_pattern = re.compile(r"([0-9]{1,2}\:?([0-9]{2})?(([Aa]|[Pp])[Mm])?)")
        # If this matches, it is in the form (1) - (5) ---> i.e. the 1st match is the start time, the 5th is the end time.
        dbl_time_pattern = re.compile(r"([0-9]{1,2}\:?([0-9]{2})?(([Aa]|[Pp])[Mm])?)\W*-\W*([0-9]{1,2}\:?([0-9]{2})?(([Aa]|[Pp])[Mm])?)")
        dbl_time_matches = get_matches(times, dbl_time_pattern)
        if(dbl_time_matches):
            stime = dbl_time_matches[0][0] 
            etime = dbl_time_matches[0][4]

    speaker_pattern = re.compile("[Ww][Hh][Oo]\:([\W\w]*)|[Ss][Pp][Ee][Aa][Kk][Ee][Rr]\:([\W\w]*)")
    speakers = get_matches(header_lines, speaker_pattern)
    if(speakers):
        speaker = speakers[0][0]
   
    if(speaker):
        # Tag the speaker section with NER tags to and check if there's part contained within PERSON tags
        speaker_tag = wsjtagger.tag_phrase(speaker) 
        person_matches = get_matches(speaker_tag, person_pattern)
        if(person_matches):
            speaker = person_matches[0]
    
        speaker = keepWhile(dropWhile(speaker, lambda x: x == " "), lambda x: x not in punct)

        split_speaker = speaker.split(" ")
        for title in titles:
            if title == split_speaker[0]: # If there's a title strip it from the speaker.
                speaker = "".join(intersperse(split_speaker[1:], " ")) 

    # Now we've got the data that we wanted, let's tag and reconstruct the email.
    print(paragraphs)


