import re
from typing import List


SENTENCE_RE = re.compile(r'(?<=[.!?])\s+|\n+')

def normalize_whitespace(text: str) -> str:
    return re.sub(r'\s+', ' ', text or '').strip()

def split_into_sentences(text: str) -> List[str]:
    text = normalize_whitespace(text)
    if not text:
        return []
    sentences = [s.strip() for s in SENTENCE_RE.split(text) if s.strip()]
    return sentences

def split_into_three_scenes(text: str) -> List[str]:
    """Split text into at least three logical chunks."""
    sentences = split_into_sentences(text)
    if len(sentences) >= 3:
        return sentences

    words = normalize_whitespace(text).split()
    if not words:
        return []
    if len(words) < 3:
        return [text, text, text]

    n = len(words)
    cut1 = max(1, n // 3)
    cut2 = max(cut1 + 1, (2 * n) // 3)
    chunks = [
        ' '.join(words[:cut1]).strip(),
        ' '.join(words[cut1:cut2]).strip(),
        ' '.join(words[cut2:]).strip(),
    ]
    return [c for c in chunks if c]
