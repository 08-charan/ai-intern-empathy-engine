from collections import Counter
import re

STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'if', 'then', 'else', 'when', 'while',
    'of', 'for', 'to', 'in', 'on', 'at', 'by', 'with', 'from', 'as', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'this', 'that', 'these', 'those', 'it',
    'its', 'they', 'them', 'their', 'we', 'our', 'you', 'your', 'i', 'me', 'my',
    'he', 'she', 'his', 'her', 'there', 'here', 'into', 'about', 'over', 'under',
    'after', 'before', 'during', 'again', 'ever', 'just', 'very', 'more', 'most',
    'can', 'could', 'should', 'would', 'will', 'shall', 'may', 'might', 'must',
    'not', 'no', 'yes', 'do', 'does', 'did', 'done'
}

WORD_RE = re.compile(r"[A-Za-z][A-Za-z'-]{1,}")

def extract_keywords(text: str, limit: int = 6):
    words = [w.lower() for w in WORD_RE.findall(text or '') if w.lower() not in STOPWORDS]
    counts = Counter(words)
    return [w for w, _ in counts.most_common(limit)]
