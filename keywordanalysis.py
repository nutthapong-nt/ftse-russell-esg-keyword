from dataclasses import dataclass, field
import re
from typing import Dict, List
from model.keyword import Keyword, get_keyword_list
from model.local_keyword import LOCAL_KEYWORD
from noise import CONJUNCTION, STOPWORD


def cleaning(text: str):
    # remove noise word
    pattern = r'\b(?:' + '|'.join(map(re.escape,
                                      STOPWORD + list(CONJUNCTION))) + r')\b'
    cleaned = re.sub(pattern, '', text, flags=re.IGNORECASE)
    # remove space
    cleaned = re.sub(r'\s+', '', cleaned)
    return cleaned


def keyword_count(text: str, keywords: List[Keyword]):
    clean_text = cleaning(text)
    result = [0] * len(keywords)
    for index, keyword in enumerate(keywords):
        clean_keyword = cleaning(keyword.word)
        if not clean_keyword:
            continue
        result[index] = clean_text.count(clean_keyword)
        clean_text = clean_text.replace(clean_keyword, "")
    return result


@dataclass
class KeywordResult:
    keyword: Keyword
    count: int

    def __init__(self,
                 keyword: Keyword,
                 count: int):
        self.keyword = keyword
        self.count = count


@dataclass
class AnalysisResult:
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


def ftse_analysis(text: str, raw_keywords: List[dict] = LOCAL_KEYWORD):
    keywords = get_keyword_list(raw_keywords)
    result = AnalysisResult()
    for index, count in enumerate(keyword_count(text, keywords)):
        if not count:
            continue
        result.keywords.append(KeywordResult(keywords[index], count))
        for topic in keywords[index].topic:
            result.increment_topic(topic, count)
    return result
