import re

from collections import Counter

def tags(text): return re.findall(r'<ENAMEX TYPE="(.*?)">', text)


def main():
    FP = "wsj_training/concatstr.txt"

    data = ""

    with open(FP, "r") as f:
        data = f.read()

    TAGS = Counter(tags(data))

    print(len(TAGS))
    print(TAGS.most_common(100))

main()
