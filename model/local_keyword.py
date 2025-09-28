from json import load
from os import path

from setting import PROJECT_PATH

data = []
with open(path.join(PROJECT_PATH,"ftse_keywords.json"),"r",encoding="utf-8") as f:
    data = load(f)

LOCAL_KEYWORD = data