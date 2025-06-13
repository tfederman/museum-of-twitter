#!/usr/bin/env python

import os
import shutil
import difflib

path = "./alt-text"

contents = {open(f"{path}/{f}").read().strip():f for f in os.listdir(path)}
contents = {k:v for k,v in contents.items() if len(k) > 48}
strs = list(contents.keys())
seen_image_files = set()

for n, (s, filename) in enumerate(contents.items()):

    if filename in seen_image_files:
        continue

    matches = difflib.get_close_matches(s, strs, n=5, cutoff=0.65)
    if len(matches) > 1:
        tempdir = f"./dupes/{n:04d}"
        os.mkdir(tempdir)
        for match in matches:
            seen_image_files.add(contents[match])
            match_file = contents[match].replace(".txt", "")
            shutil.copy(f"./images/{match_file}", f"{tempdir}/{match_file}")
            print(match_file)
            print("-----------------------")
            print(match)
            print("-----------------------")
        print("\n=====================================\n")
