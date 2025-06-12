#!/usr/bin/env python

import os
import json
import random
from datetime import datetime, timedelta

# usage: ./bin/assign-to-dates.py > ./data/dated-tweets.json

images = os.listdir("./images")
dates = json.loads(open("./data/extracted-dates.json").read())
dates = {k:v for k,v in dates.items() if os.path.exists(f"./images/{k}")}

images = [i for i in images if not i in dates.keys()]
random.shuffle(images)

dt = datetime(2025,1,1)

year = {}

while dt < datetime(2026,1,1):

    dt_str = dt.strftime("%m-%d")
    year[dt_str] = [k for k,v in dates.items() if v[5:] == dt_str]
    images = [i for i in images if i not in year[dt_str]]

    while len(year[dt_str]) < 4 and images:
        year[dt_str].append(images.pop())

    dt += timedelta(days=1)

print(json.dumps(year, indent=4))
