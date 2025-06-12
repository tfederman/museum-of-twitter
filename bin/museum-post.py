#!/usr/bin/env python

import sys
import json
from datetime import datetime

import exception
from pysky import BskyClient
from pysky.posts import Post, Image

# post [idx]th image for today (one-based)
idx = int(sys.argv[1])

bsky = BskyClient(
    bsky_auth_username = os.getenv("BSKY_AUTH_USERNAME"),
    bsky_auth_password = os.getenv("BSKY_AUTH_APP_PASSWORD"),
)

month = datetime.now().month
day = datetime.now().day

year = json.loads(open("./data/dated-tweets.json").read())

images = year[f"{month:02d}-{day:02d}"]

if len(images) < idx:
    exit(0)

img = images[idx-1]
text = open(f"./alt-text/{img}.txt").read().strip()

post = Post()
post.add(Image(filename=f"./images/{img}", alt=text))
bsky.create_post(post=post)
