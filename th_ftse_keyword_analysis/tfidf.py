from dataclasses import dataclass, field
import math
from typing import Any, Dict, List

from th_ftse_keyword_analysis.keywordanalysis import AnalysisResult

from dataclasses import dataclass, field
import math
from typing import Any, Dict, List


@dataclass
class WordStat:
    frequency: int
    tfidf: float


@dataclass
class TFIDFResult:
    document_name: str
    document_word_count: int
    words: Dict[str, WordStat] = field(default_factory=dict)

    def dump_json(self) -> List[Dict[str, Any]]:
        """Return TF-IDF and frequency data in JSON-friendly format."""
        return [
            {
                "name": self.document_name,
                "word": word,
                "frequency": stat.frequency,
                "document_word_count":self.document_word_count,
                "tfidf": stat.tfidf,
            }
            for word, stat in self.words.items()
        ]

    def dump_csv(self) -> str:
        """Return TF-IDF and frequency data in CSV format (without header)."""
        return "\n".join(
            f'"{self.document_name}","{word}",{stat.frequency},{self.document_word_count},{stat.tfidf:.6f}'
            for word, stat in self.words.items()
        )


def tfidf_to_json(results: List[TFIDFResult]) -> List[Dict[str, Any]]:
    """Convert a list of TFIDFResult to JSON."""
    return [row for result in results for row in result.dump_json()]


def tfidf_to_csv(results: List[TFIDFResult]) -> str:
    """Convert a list of TFIDFResult to CSV."""
    header = '\ufeff"name","word","frequency","document_word_count","tfidf-score"\n'
    return header + "\n".join(result.dump_csv() for result in results)


def calculate_tfidf(
    results: List[AnalysisResult], use_keyword_count: bool = False
) -> List[TFIDFResult]:
    """
    Calculate TF-IDF for each keyword in each AnalysisResult.
    - If use_keyword_count=True, TF = count / sum(keyword counts)
    - Else, TF = count / total_word_count
    """
    total_docs = len(results)
    if total_docs == 0:
        return []

    # Step 1: Compute document frequency (df)
    df: Dict[str, int] = {}
    for r in results:
        for k in {kr.keyword.mainword for kr in r.keywords}:
            df[k] = df.get(k, 0) + 1

    log = math.log
    tfidf_results: List[TFIDFResult] = []

    # Step 2: Compute TF-IDF per document
    for r in results:
        if not r.keywords:
            continue

        base = (
            sum(kr.count for kr in r.keywords)
            if use_keyword_count
            else r.text_word_count or 1
        )

        words: Dict[str, WordStat] = {}
        for kr in r.keywords:
            word = kr.keyword.mainword
            freq = kr.count
            tf = freq / base
            idf = log(total_docs / (1 + df[word]))
            words[word] = WordStat(frequency=freq, tfidf=tf * idf)

        tfidf_results.append(
            TFIDFResult(
                document_name=r.name, document_word_count=r.text_word_count, words=words
            )
        )

    return tfidf_results
