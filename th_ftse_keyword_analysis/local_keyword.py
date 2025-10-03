from json import load
import importlib.resources

data = []
with importlib.resources.open_text("th_ftse_keyword_analysis","ftse_keywords.json",encoding="utf-8") as f:
    data = load(f)

LOCAL_KEYWORD = data