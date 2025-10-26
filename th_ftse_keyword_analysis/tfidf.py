from dataclasses import dataclass, field
import math
from typing import Any, Dict, List

from th_ftse_keyword_analysis.keywordanalysis import AnalysisResult


@dataclass
class TFIDFResult:
    document_name: str
    tfidf_scores: Dict[str, float] = field(default_factory=dict)

    def dump_json(self):
        return [
            {"name": self.document_name, "word": word, "tfidf": self.tfidf_scores[word]}
            for word in self.tfidf_scores
        ]

    def dump_csv(self):
        return "\n".join(
            [
                f'"{self.document_name}","{word}","{self.tfidf_scores[word]}"'
                for word in self.tfidf_scores
            ]
        )


def tfidf_to_json(results: List[TFIDFResult]) -> List[Dict[str, Any]]:
    """
    Convert a list of TFIDFResult to JSON.
    """
    buffer = []
    for result in results:
        buffer += result.dump_json()
    return buffer


def tfidf_to_csv(results: List[TFIDFResult]) -> str:
    """
    Convert a list of TFIDFResult to CSV.
    """
    buffer = '\ufeff"name","word","tfidf-score"\n'
    for result in results:
        buffer += result.dump_csv() + "\n"
    return buffer


def calculate_tfidf(
    results: List[AnalysisResult], use_keyword_count: bool = False
) -> List[TFIDFResult]:
    """
    Calculate TF-IDF for each keyword in each AnalysisResult.
    - If use_keyword_count=True, TF = count / a_keyword_in_document
    - Else, TF = count / total_word_in_document
    Returns a list of TFIDFResult objects.
    """
    total_document = len(results)

    # --- Step 1: Compute document frequency for each keyword ---
    df = {}
    for result in results:
        seen = set()
        for kr in result.keywords:
            kname = kr.keyword.mainword
            if kname not in seen:
                df[kname] = df.get(kname, 0) + 1
                seen.add(kname)

    # --- Step 2: Compute TF-IDF for each document ---
    tfidf_results = []
    for result in results:
        if use_keyword_count:
            base = sum(kr.count for kr in result.keywords) or 1
        else:
            base = result.text_word_count or 1

        tfidf_scores = {}

        for kr in result.keywords:
            keyword = kr.keyword.mainword
            tf = kr.count / base
            idf = math.log(total_document / (1 + df.get(keyword, 0)))
            tfidf_scores[keyword] = tf * idf

        tfidf_results.append(
            TFIDFResult(document_name=result.name, tfidf_scores=tfidf_scores)
        )

    return tfidf_results
