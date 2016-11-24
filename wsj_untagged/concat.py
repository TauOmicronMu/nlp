OUTPUT= "concatstr.txt"
TOTAL = 2000

filenames = ["wsj_%s.txt" %str(n).zfill(4) for n in range(1,TOTAL)]

concatstr = ""
for fn in filenames:
    with open(fn, "r") as f:
        concatstr += f.read();

with open(OUTPUT, "w") as f:
    f.write(concatstr)    
