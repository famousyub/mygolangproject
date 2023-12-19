import os, re
import requests, shutil
from bs4 import BeautifulSoup
from pathlib import Path

counter = 1
imageFolder = "./Star Wars Images/"
lastName = ""

def downloadURL(url, name):
    """downloadURL: Download URL to name"""
    resp = requests.get(url, stream=True)
    local_file = open(imageFolder + name + ".jpg", "wb")
    resp.raw.decode_content = True
    shutil.copyfileobj(resp.raw, local_file)
    del resp

Path(imageFolder).mkdir(parents=True, exist_ok=True)
r = requests.get('https://www.starwars.com/news/star-wars-backgrounds')
soup = BeautifulSoup(r.text, "html.parser")
for link in soup.findAll('img'):
    image_url = link.get('src')
    image_name = link.get('alt').replace(":"," -")
    if ".jpg" in image_url and "backgrounds" in image_url and "Mosaic" not in image_name:
        if image_name == lastName:
            counter += 1
        else:
            counter = 1
        lastName = image_name
        downloadURL(image_url,image_name + " {0}".format(str(counter)))