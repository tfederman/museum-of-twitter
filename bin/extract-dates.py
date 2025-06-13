#!/usr/bin/env python

import re
import json
from datetime import datetime

# usage: ./bin/extract-dates.py > ./data/extracted-dates.json

j = json.loads(open("./data/extracted-text.json").read())

patterns = [
    ("[a-zA-z]{3} [0-9]{1,2}, 20[0-9]{2}", "%b %d, %Y"), # May 25, 2016
    ("[a-zA-z]{3,9} [0-9]{1,2}, 20[0-9]{2}", "%B %d, %Y"), # June 25, 2016
    ("[0-9]{1,2} [a-zA-z]{3} 20[0-9]{2}", "%d %b %Y"), # 15 Apr 2015
    ("20[0-9]{2}-[0-9]{2}-[0-9]{2}", "%Y-%m-%d"), # 2022-03-13
]

dates = {}

def extract_date(s):
    for p,f in patterns:
        m = re.search(f"({p})", s)
        if m:
            try:
                dt = datetime.strptime(m.group(1), f)
                return dt
            except ValueError:
                pass

    return None

for k,v in j.items():
    dt = extract_date(v)

    # ignore dates of feb. 29 images or else they
    # would only get posted once every 4 years
    if dt and dt.month == 2 and dt.day == 29:
        continue

    if dt:
        dates[k] = dt.strftime("%Y-%m-%d")


print(json.dumps(dates, indent=4))
