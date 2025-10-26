from dataclasses import dataclass, field
from typing import List

from th_ftse_keyword_analysis.local_keyword import LOCAL_KEYWORD


@dataclass
class Keyword:

    mainword: str
    word: str
    topic: List[str] = field(default_factory=list)

    def __init__(self, mainword: str, word: str, topic: List[str]):
        self.mainword = mainword  # the variable name e.g. CARBON_NEUTRALITY
        self.word = word  # one synonym word
        self.topic = topic  # list of topics

    def __repr__(self):
        return f"Keyword(mainword='{self.mainword}', word='{self.word}', topic={self.topic})"
    
    def __eq__(self, value):
        if not isinstance(value,Keyword):
            return False
        return self.word == value.word

def validate_keyword_list(data):
    if not isinstance(data, list):
        raise TypeError("keyword list be array")
    for entry in data:
        validate_keyword_object(entry)

def validate_keyword_object(entry):
    if not isinstance(entry, dict):
        raise TypeError("data in keyword list must be object")
    if "keyword" not in entry or "topic" not in entry or "synonym" not in entry:
        raise TypeError("keyword object must contain keyword, topic, and synonym keys")
    if not isinstance(entry["synonym"], list):
        raise TypeError("synonym must be array")
    for synonym in entry["synonym"]:
        if not isinstance(synonym, str):
            raise TypeError("synonym word must be string")


def get_keyword_list(data=LOCAL_KEYWORD):
    validate_keyword_list(data)
    keywords: List[Keyword] = []
    for entry in data:
        mainword = entry["keyword"]
        topics = entry["topic"]
        # each synonym gets its own Keyword object
        for word in entry["synonym"]:
            keywords.append(Keyword(mainword=mainword, word=word, topic=topics))
    # sort by word length (longest first)
    keywords.sort(key=lambda k: -len(k.word))
    return keywords
