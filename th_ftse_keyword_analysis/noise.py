# I try from https://github.com/PyThaiNLP/pythainlp/blob/dev/pythainlp/corpus/stopwords_th.txt 
# But it is not suitable for this case; it crashes many keywords.
# So I try to create a stop word list from Oppday manually.

STOPWORD = [
    "สำหรับ",
    "นะครับ",
    "นะคะ",
    "ครับ",
    "ค่ะ",
    "คะ",
    "ของ"
]

CONJUNCTION = (
    "เรื่อง",
    "และ",
    "หรือ",
    "จาก",
    "ของ",
    "กลุ่ม",
    "การใช้",
    "ที่เป็น",
    "อย่าง"
)
