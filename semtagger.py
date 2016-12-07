import re
import nltk
import nltk.data
import itertools
import wsjtagger

# Just ignore the ones with the \t tab issue...
filenames = [n for n in range(301,485)]
bad_filenames= [352, 357, 364, 379]
for file in bad_filenames:
    filenames.remove(file)

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
    print(file)

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
        abstract_pattern = re.compile("[Aa]bstract\:.*?$")
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

    # For each paragraph, tokenise them into sentences
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    paragraphs_sentences = list(map(sent_detector.tokenize, paragraphs))

    header_lines = header.split("\n")

   # Get all matches of a regex pattern on a header (or any string)
    def get_matches(headerl, pattern):
        matches = []
        for line in headerl:
            matches.append(pattern.findall(line))
        return [item for x in matches if x != [] for item in x]

    time_line_pattern = re.compile(r"[TtWw][IiHh][MmEe][EeNn]\:([\W\w]*)")
    times = get_matches(header_lines, time_line_pattern)    
    if(times): # If the header contains a 'Time' line
        # If our time is in the format '(h)h:mm - (h)h:mm' split it into start time and end time
        time_pattern = re.compile(r"([0-9]{1,2}\:?([0-9]{2})?(([Aa]|[Pp])[Mm])?)")
        # If this matches, it is in the form (1) - (5) ---> i.e. the 1st match is the start time, the 5th is the end time.
        dbl_time_pattern = re.compile(r"([0-9]{1,2}\:?([0-9]{2})?\s*(([Aa]|[Pp])[Mm])?)\W*-\W*([0-9]{1,2}\:?([0-9]{2})?\s*(([Aa]|[Pp])[Mm])?)")
        dbl_time_matches = get_matches(times, dbl_time_pattern)
        if(dbl_time_matches):
            stime = dbl_time_matches[0][0] 
            etime = dbl_time_matches[0][4]
        else:
            time_matches = get_matches(times, time_pattern)
            stime = time_matches[0][0]
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
    # Tag the sentences, and then the paragraphs.
    for p in paragraphs_sentences:
        for s in p: 
            p[p.index(s)] = "<sentence>%s</sentence>"%s
        paragraphs_sentences[paragraphs_sentences.index(p)] = "<paragraph>%s</paragraph>" %("".join(p))

    lines = paragraphs_sentences
  
    # TODO: Refactor this into a single function 
    if(stime): # If we have a start time, tag it in the data
        stime_pattern = re.compile("([\W\w]*)(%s)([\W\w]*)"%stime, re.IGNORECASE)
        for line in lines:
            stime_matches = stime_pattern.findall(line)
            if(stime_matches):
                lines[lines.index(line)] = "%s<stime>%s</stime>%s"%stime_matches[0]
    if(etime): # If we have an end time, tag it in the data
        etime_pattern = re.compile("([\W\w]*)(%s)([\W\w]*)"%etime, re.IGNORECASE)
        for line in lines:
            etime_matches = etime_pattern.findall(line)
            if(etime_matches):
                lines[lines.index(line)] = "%s<etime>%s</etime>%s"%etime_matches[0]
    if(speaker): # If we have a speaker, tag them in the data
        speaker_pattern = re.compile("([\W\w]*)(%s)([\W\w]*)"%speaker, re.IGNORECASE)
        for line in lines:
            speaker_matches = speaker_pattern.findall(line)
            if(speaker_matches):
                lines[lines.index(line)] = "%s<speaker>%s</speaker>%s"%speaker_matches[0]

    # Now reconstruct the email one final time
    tagged_data = "".join(intersperse(lines, "\n\n"))
    
    # Write to the tagged data file.
    with open("s_tagged/%s.txt"%file, "w") as f:
        f.write(tagged_data)

for file in bad_filenames:
    with open("s_untagged/%s.txt"%file, "r") as f:
        with open("s_tagged/%s.txt"%file, "w") as f2:
            f2.write(f.read())
