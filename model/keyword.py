from typing import List

from model.local_keyword import LOCAL_KEYWORD


class Keyword:
    
    mainword: str
    word: str
    topic: List[str]

    def __init__(self, mainword: str, word: str, topic: List[str]):
        self.mainword = mainword   # the variable name e.g. CARBON_NEUTRALITY
        self.word = word           # one synonym word
        self.topic = topic         # list of topics

    def __repr__(self):
        return f"Keyword(mainword='{self.mainword}', word='{self.word}', topic={self.topic})"
    
def get_keyword_list(data=LOCAL_KEYWORD):
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