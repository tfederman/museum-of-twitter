#!/usr/bin/env python

import os
import re
import json
import shutil
from datetime import datetime

# usage: ./bin/extract-dates.py > ./data/extracted-dates.json

j = json.loads(open("./data/extracted-text.json").read())

patterns = [
    ("[a-zA-z]{3} [0-9]{1,2}, 20[0-9]{2}", "%b %d, %Y"), # May 25, 2016
    ("[a-zA-z]{3,9} [0-9]{1,2}, 20[0-9]{2}", "%B %d, %Y"), # June 25, 2016
    ("[0-9]{1,2} [a-zA-z]{3} 20[0-9]{2}", "%d %b %Y"), # 15 Apr 2015
    ("20[0-9]{2}-[0-9]{2}-[0-9]{2}", "%Y-%m-%d"), # 2022-03-13
    ("[a-zA-z]{3,4} [a-zA-z]{3,4} [0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} \\+0000 20[0-9]{2}", "%a %b %d %H:%M:%S +0000 %Y"), # Tue Apr 24 14:12:35 +0000 2018
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

def extract_date_from_json(filename):
    m = re.search("([0-9]{10,})", filename)
    if m:
        tweet_id = m.group(1)
    else:
        return None

    json_file = f"./data/tweet-contents/{tweet_id}.json"
    if os.path.exists(json_file):
        j = json.loads(open(json_file).read())
        date_str = j.get("created_at")
        if date_str:
            dt = extract_date(date_str)
            return dt

    return None

for k,v in j.items():
    dt = extract_date(v) or extract_date_from_json(k)

    # adjust dates of feb. 29 images or else they
    # would only get posted once every 4 years
    if dt and dt.month == 2 and dt.day == 29:
        dt = dt.replace(day=28)

    if dt:
        dates[k] = dt.strftime("%Y-%m-%d")
    else:
        print(k)
        if os.path.exists(f"images/{k}"):
            shutil.copy2(f"images/{k}", f"undated/{k}")
        else:
            print("\tDOES NOT EXIST")


#print(json.dumps(dates, indent=4))
