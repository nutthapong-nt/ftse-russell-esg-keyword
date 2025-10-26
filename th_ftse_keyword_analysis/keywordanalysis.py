from dataclasses import dataclass, field
import re
from typing import Dict, List

import pythainlp
from th_ftse_keyword_analysis.keyword import Keyword, get_keyword_list
from th_ftse_keyword_analysis.local_keyword import LOCAL_KEYWORD
from th_ftse_keyword_analysis.noise import CONJUNCTION, STOPWORD


def cleaning(text: str):
    # remove noise word
    pattern = r"\b(?:" + "|".join(map(re.escape, STOPWORD + list(CONJUNCTION))) + r")\b"
    cleaned = re.sub(pattern, "", text, flags=re.IGNORECASE)
    # remove space
    cleaned = re.sub(r"\s+", "", cleaned)
    # keep only charector
    cleaned = re.sub(r"[^0-9a-zA-Zก-๙]", "", cleaned)
    return cleaned


class KeywordCount:
    count: int
    length: int

    def __init__(self, count: int, length: int):
        self.count = count
        self.length = length


def keyword_count(text: str, keywords: List[Keyword]):
    result: List[KeywordCount] = []
    keywords_count = 0
    for keyword in keywords:
        clean_keyword = cleaning(keyword.word)
        if not clean_keyword:
            continue
        word_count = text.count(clean_keyword)
        keywords_count += word_count
        result.append(KeywordCount(word_count, len(clean_keyword)))
        text = text.replace(clean_keyword, " ")
    text_word_count = (
        len(pythainlp.word_tokenize(text, engine="newmm")) + keywords_count
    )
    return result, text_word_count


@dataclass
class KeywordResult:
    keyword: Keyword
    count: int
    keyword_length: int

    def __init__(self, keyword: Keyword, count: int, keyword_length: int):
        self.keyword = keyword
        self.count = count
        self.keyword_length = keyword_length

    def dump_json(self):
        return {
            "main": self.keyword.mainword,
            "keyword": self.keyword.word,
            "count": self.count,
            "keyword_length": self.keyword_length,
        }

    def dump_csv(self):
        return f"{self.keyword.word}={self.count}"
    
    def copy(self):
        return KeywordResult(keyword=self.keyword,count=self.count,keyword_length=self.keyword_length)


def merge_keyword_lists(list1: List[KeywordResult], list2: List[KeywordResult]) -> List[KeywordResult]:
    merged: Dict[str, KeywordResult] = {}

    # Combine all keywords and sum counts
    for kr in list1 + list2:
        if kr.keyword.word in merged:
            merged[kr.keyword.word].count += kr.count
        else:
            merged[kr.keyword.word] = kr.copy()

    # Convert back to list of KeywordResult
    return [merged[k] for k in merged]


@dataclass
class AnalysisResult:
    name: str = ""
    biodiversity: int = 0
    climate_change: int = 0
    pollution_resources: int = 0
    water_security: int = 0
    customer_responsibility: int = 0
    health_safety: int = 0
    human_rights_community: int = 0
    labor_standard: int = 0
    anti_corruption: int = 0
    corporate_governance: int = 0
    risk_management: int = 0
    tax_transparency: int = 0
    supply_chain_environmental: int = 0
    supply_chain_social: int = 0
    keywords: List[KeywordResult] = field(default_factory=list)
    text_length: int = 0
    text_word_count: int = 0

    def _topic_fields(self) -> Dict[str, str]:
        # map topic keys (used in Keyword.topic) to attribute names on this dataclass
        return {
            "BIODIVERSITY": "biodiversity",
            "CLIMATE_CHANGE": "climate_change",
            "POLLUTION_RESOURCES": "pollution_resources",
            "WATER_SECURITY": "water_security",
            "CUSTOMER_RESPONSIBILITY": "customer_responsibility",
            "HEALTH_SAFETY": "health_safety",
            "HUMAN_RIGHTS_COMMUNITY": "human_rights_community",
            "LABOR_STANDARD": "labor_standard",
            "ANTI_CORRUPTION": "anti_corruption",
            "CORPORATE_GOVERNANCE": "corporate_governance",
            "RISK_MANAGEMENT": "risk_management",
            "TAX_TRANSPARENCY": "tax_transparency",
            "SUPPLY_CHAIN_ENVIRONMENTAL": "supply_chain_environmental",
            "SUPPLY_CHAIN_SOCIAL": "supply_chain_social",
        }

    def increment_topic(self, topic_key: str, delta: int = 1) -> None:
        """Safely increment a topic counter if mapped; ignores unknown topics."""
        mapping = self._topic_fields()
        attr = mapping.get(topic_key)
        if attr:
            current = getattr(self, attr, 0)
            setattr(self, attr, current + delta)
        else:
            # unknown topic: optionally store or ignore; here we ignore
            pass

    def dump_json(self):
        return {
            "name": self.name,
            "biodiversity": self.biodiversity,
            "climate_change": self.climate_change,
            "pollution_resources": self.pollution_resources,
            "water_security": self.water_security,
            "customer_responsibility": self.customer_responsibility,
            "health_safety": self.health_safety,
            "human_rights_community": self.human_rights_community,
            "labor_standard": self.labor_standard,
            "anti_corruption": self.anti_corruption,
            "corporate_governance": self.corporate_governance,
            "risk_management": self.risk_management,
            "tax_transparency": self.tax_transparency,
            "supply_chain_environmental": self.supply_chain_environmental,
            "supply_chain_social": self.supply_chain_social,
            "keywords": [keyword.dump_json() for keyword in self.keywords],
            "text_length": self.text_length,
            "text_word_count": self.text_word_count,
        }

    def dump_csv(self):
        keywords = "\n".join(keyword.dump_csv() for keyword in self.keywords)
        return ",".join(
            [
                f'"{self.name}"',
                f'"{self.text_length}"',
                f'"{self.text_word_count}"',
                f'"{self.biodiversity}"',
                f'"{self.climate_change}"',
                f'"{self.pollution_resources}"',
                f'"{self.water_security}"',
                f'"{self.customer_responsibility}"',
                f'"{self.health_safety}"',
                f'"{self.human_rights_community}"',
                f'"{self.labor_standard}"',
                f'"{self.anti_corruption}"',
                f'"{self.corporate_governance}"',
                f'"{self.risk_management}"',
                f'"{self.tax_transparency}"',
                f'"{self.supply_chain_environmental}"',
                f'"{self.supply_chain_social}"',
                f'"{keywords}"',
            ]
        )
    
    def __add__(self,other):
        if not isinstance(other,AnalysisResult):
            raise TypeError(f"AnalysisResult can add with AnalysisResult but detect {type(other)}")
        new_result = AnalysisResult(name=self.name+","+other.name)
        new_result.biodiversity = other.biodiversity + self.biodiversity
        new_result.climate_change = other.climate_change + self.climate_change
        new_result.pollution_resources = other.pollution_resources + self.pollution_resources
        new_result.water_security = other.water_security + self.water_security
        new_result.customer_responsibility = other.customer_responsibility + self.customer_responsibility
        new_result.health_safety = other.health_safety + self.health_safety
        new_result.human_rights_community = other.human_rights_community + self.human_rights_community
        new_result.labor_standard = other.labor_standard + self.labor_standard
        new_result.anti_corruption = other.anti_corruption + self.anti_corruption
        new_result.corporate_governance = other.corporate_governance + self.corporate_governance
        new_result.risk_management = other.risk_management + self.risk_management
        new_result.tax_transparency = other.tax_transparency + self.tax_transparency
        new_result.supply_chain_environmental = other.supply_chain_environmental + self.supply_chain_environmental
        new_result.supply_chain_social = other.supply_chain_social + self.supply_chain_social
        new_result.text_length = other.text_length+ self.text_length
        new_result.text_word_count = other.text_word_count+ self.text_word_count
        new_result.keywords = merge_keyword_lists(self.keywords,other.keywords)
        return new_result


def ftse_analysis(
    text: str,
    name: str = "untitle",
    raw_keywords: List[dict] = LOCAL_KEYWORD,
    distinct: bool = False,
) -> AnalysisResult:
    text = cleaning(text)
    keywords = get_keyword_list(raw_keywords)
    result = AnalysisResult(name=name, text_length=len(text))
    list_keyword_count, total_word_count = keyword_count(text, keywords)
    result.text_word_count = total_word_count
    for index, count in enumerate(list_keyword_count):
        if not count.count:
            continue
        result.keywords.append(
            KeywordResult(keywords[index], count.count, count.length)
        )
        for topic in keywords[index].topic:
            if distinct:
                result.increment_topic(topic, 1)
            else:
                result.increment_topic(topic, count.count)
    return result


def convert_to_csv(results: List[AnalysisResult]):
    buffer = '\ufeff"name","text_length","text_word_count","biodiversity","climate_change","pollution_resources","water_security","customer_responsibility","health_safety","human_rights_community","labor_standard","anti_corruption","corporate_governance","risk_management","tax_transparency","supply_chain_environmental","supply_chain_social","keyword"\n'
    return buffer + "\n".join(result.dump_csv() for result in results)


def convert_to_json(results: List[AnalysisResult]):
    return [result.dump_json() for result in results]
