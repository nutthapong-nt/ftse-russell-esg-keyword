# FTSE ESG Keyword Extractor (Thai / English)

This project is part of my thesis work.  
It provides **FTSE Russell ESG keyword dictionaries** (Thai + English) and tools for extracting and analyzing ESG-related terms from **stakeholder meeting transcripts, Opportunity Day events, and conference presentations**.  

The goal is to make this resource **open source**, so researchers and practitioners can reuse it to measure corporate sustainability communication.

---

## 🎯 Motivation

Listed companies in Thailand present performance and future outlooks at quarterly "Opportunity Day" conferences.  
These meetings contain valuable qualitative insights into **sustainability strategies**.  

By linking transcripts to **FTSE Russell ESG topics**, we can:

- Identify how often ESG themes are discussed
- Compare companies/sectors on ESG communication
- Visualize sustainability trends over time

---

## 🗂️ Data Structure

Keywords are stored in JSON for easy sharing and reuse.  
Each entry includes:

- `keyword`: canonical ESG keyword (variable-like name, uppercase)
- `synonym`: list of synonym words/phrases (Thai + English)
- `topic`: one or more FTSE Russell ESG topics

### Example

```json
[
  {
    "keyword": "CARBON_NEUTRALITY",
    "synonym": [
      "คาร์บอนสุทธิเป็นศูนย์",
      "เป็นกลางทางคาร์บอน",
      "เน็ตซีโร่",
      "net zero",
      "European Green",
      "zero emission"
    ],
    "topic": ["CLIMATE_CHANGE"]
  }
]
