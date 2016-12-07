import re 

# get a list of all the filenames to test on
filenames = [n for n in range(301,485)]
bad_filenames= [352, 357, 364, 379]
for file in bad_filenames:
    filenames.remove(file)

tag_pattern = re.compile("(<.*?>.*?<\/.*?>)")
speaker_tag_pattern = re.compile("(<speaker>.*?</speaker>)")
stime_tag_pattern = re.compile("<stime>.*?</stime>")
etime_tag_pattern = re.compile("<etime>.*?</etime>")
location_tag_pattern = re.compile("<location>.*?</location>")
paragraph_tag_pattern = re.compile("<paragraph>.*?</paragraph>")
sentence_tag_pattern = re.compile("<sentence>.*?</sentence>")

total_tags = 1
t_speak_tags = 1
t_stime_tags = 1
t_etime_tags = 1
t_loc_tags = 1
t_para_tags = 1
t_sent_tags = 1
speak_tagged = 1
stime_tagged = 1
etime_tagged = 1
loc_tagged = 1
para_tagged = 1
sent_tagged = 1

def rem_empt(l):
    return [x for x in l if x != []]

for file in filenames:
    exemplar_data = None
    tagged_data = None
    with open("s_test_tagged/%s.txt"%file, "r") as f:
        exemplar_data = f.read()
    with open("s_tagged/%s.txt"%file, "r") as f:
        tagged_data = f.read()
    e_lines = exemplar_data.split("\n") 
    t_lines = tagged_data.split("\n") 
    e_tags = []
    e_speak = []
    e_stime = []
    e_etime = []
    e_loc = []
    e_para = []
    e_sent = [] 
    t_speak = []
    t_stime = []
    t_etime = []
    t_loc = []
    t_para = []
    t_sent = []
    # TODO: For the love of god clean this up... To anyone reading this - I was in a rush...
    for line in e_lines:
        e_tags.append(tag_pattern.findall(line))
        e_speak.append(speaker_tag_pattern.findall(line))
        e_stime.append(stime_tag_pattern.findall(line))
        e_etime.append(etime_tag_pattern.findall(line))
        e_loc.append(location_tag_pattern.findall(line))
        e_para.append(paragraph_tag_pattern.findall(line))
        e_sent.append(sentence_tag_pattern.findall(line))
       
    for line in t_lines:
        t_speak.append(speaker_tag_pattern.findall(line))
        t_stime.append(stime_tag_pattern.findall(line))
        t_etime.append(etime_tag_pattern.findall(line))
        t_loc.append(location_tag_pattern.findall(line))
        t_para.append(paragraph_tag_pattern.findall(line))
        t_sent.append(sentence_tag_pattern.findall(line))
    e_tags = rem_empt(e_tags)
    e_speak = rem_empt(e_speak)
    e_stime = rem_empt(e_stime)
    e_etime = rem_empt(e_etime)
    e_loc = rem_empt(e_loc)
    e_para = rem_empt(e_para)
    e_sent = rem_empt(e_sent)
 
    for tag in e_speak:
        if tag in t_speak:
            speak_tagged += 1
    for tag in e_stime:
        if tag in t_stime:
            stime_tagged += 1
    for tag in e_etime:
        if tag in t_etime:
            etime_tagged += 1
    for tag in e_loc:
        if tag in t_loc:
            loc_tagged += 1
    for tag in e_para:
        if tag in t_para:
            para_tagged += 1
    for tag in e_sent:
        if tag in t_sent:
            sent_tagged += 1


    t_speak_tags += len(e_speak)
    t_stime_tags += len(e_stime)
    t_etime_tags += len(e_etime)
    t_loc_tags += len(e_loc)
    t_para_tags += len(e_para)
    t_sent_tags += len(e_sent)
     

num_tagged = speak_tagged +  stime_tagged +  etime_tagged
'''
print(speak_tagged)
print(stime_tagged)
print(etime_tagged)
print(loc_tagged)
print(para_tagged)
print(sent_tagged)

print(t_speak_tags)
print(t_stime_tags)
print(t_etime_tags)
print(t_loc_tags)
print(t_para_tags)
print(t_sent_tags)
'''
accuracy = 100* num_tagged/(t_speak_tags + t_stime_tags + t_etime_tags)
speak_acc = 100* speak_tagged/t_speak_tags
stime_acc = 100* stime_tagged/t_stime_tags
etime_acc = 100* etime_tagged/t_etime_tags
# loc_acc = 100* loc_tagged/t_loc_tags 
# para_acc = 100* para_tagged/t_para_tags
# sent_acc = 100* sent_tagged/t_sent_tags

with open("semevalresults.txt", "w") as f:
    f.write("")
with open("semevalresults.txt", "a") as f:
    f.write("overall accuracy: %s\n" %accuracy) 
    f.write("speaker accuracy: %s\n" %speak_acc)
    f.write("start time accuracy: %s\n" %stime_acc)
    f.write("end time accuracy: %s\n" %etime_acc)
