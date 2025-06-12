#!/usr/bin/env python

import os
import json

import pytesseract
from PIL import Image

# usage: ./bin/extract-text.py > ./data/extracted-text.json

image_path = "./images"

output = {}
images = sorted(os.listdir(image_path))

for n,img in enumerate(images):
    text = pytesseract.image_to_string(Image.open(f"{image_path}/{img}"))
    text = text.strip()
    output[img] = text

print(json.dumps(output))
