import sys
import re
for line in sys.stdin:
    line = line.strip()
    items = line.split('\t')
    text = items[8]
    if len(re.findall("china|chinese|China|Chinese|CHINA|CHINESE|CHN",text)) == 0 :
        print line.replace('\r','')
