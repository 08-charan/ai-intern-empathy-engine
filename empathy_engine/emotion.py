from dataclasses import dataclass
import re
from typing import Dict, Tuple

POSITIVE = {
    'good', 'great', 'awesome', 'amazing', 'happy', 'love', 'excellent', 'nice',
    'thank', 'thanks', 'congrats', 'congratulations', 'win', 'winner', 'success',
    'successful', 'pleased', 'excited', 'delight', 'delighted', 'wonderful', 'best',
    'fantastic', 'brilliant', 'positive', 'enjoy', 'glad', 'relieved', 'support'
}
NEGATIVE = {
    'bad', 'sad', 'angry', 'frustrated', 'upset', 'hate', 'terrible', 'awful',
    'poor', 'worse', 'worst', 'problem', 'issue', 'error', 'failure', 'failed',
    'annoyed', 'disappointed', 'concerned', 'worry', 'worried', 'slow', 'late',
    'broken', 'damage', 'urgent', 'complaint', 'frustration', 'stress', 'stressed'
}
NEUTRAL_HINTS = {'update', 'status', 'information', 'details', 'note', 'summary', 'request'}

WORD_RE = re.compile(r"[A-Za-z']+")

@dataclass
class EmotionResult:
    label: str
    confidence: float
    polarity: float
    subjectivity: float
    details: Dict[str, float]

def _score_lexicon(text: str) -> Tuple[float, float]:
    words = [w.lower() for w in WORD_RE.findall(text or '')]
    if not words:
        return 0.0, 0.0
    pos = sum(1 for w in words if w in POSITIVE)
    neg = sum(1 for w in words if w in NEGATIVE)
    total = len(words)
    polarity = (pos - neg) / max(1, total)
    subjectivity = min(1.0, (pos + neg) / max(1, total / 3))
    return polarity, subjectivity

def analyze_emotion(text: str) -> EmotionResult:
    text = (text or '').strip()
    if not text:
        return EmotionResult('Neutral', 1.0, 0.0, 0.0, {'positive': 0, 'negative': 0})

    polarity, subjectivity = _score_lexicon(text)
    words = [w.lower() for w in WORD_RE.findall(text)]

    pos = sum(1 for w in words if w in POSITIVE)
    neg = sum(1 for w in words if w in NEGATIVE)
    negation = any(w in {'not', "don't", "cannot", "can't", "won't", 'never'} for w in words)

    if pos > neg + 1 and polarity > 0.01:
        label = 'Happy'
        confidence = min(0.99, 0.55 + 0.08 * pos + 0.2 * abs(polarity))
    elif neg > pos + 1 or (polarity < -0.01 and neg >= 1):
        if any(w in {'frustrated', 'annoyed', 'complaint', 'issue', 'error', 'late', 'urgent'} for w in words):
            label = 'Frustrated'
        elif any(w in {'worried', 'concerned', 'stress', 'stressed', 'careful'} for w in words):
            label = 'Concerned'
        else:
            label = 'Negative'
        confidence = min(0.99, 0.55 + 0.08 * neg + 0.2 * abs(polarity))
    elif negation and pos >= 1:
        label = 'Concerned'
        confidence = 0.68
        polarity = -0.15
    else:
        label = 'Neutral'
        confidence = 0.72 if any(w in NEUTRAL_HINTS for w in words) else 0.62
        polarity = 0.0

    return EmotionResult(
        label=label,
        confidence=round(confidence, 3),
        polarity=round(polarity, 3),
        subjectivity=round(subjectivity, 3),
        details={'positive': float(pos), 'negative': float(neg), 'negation': float(bool(negation))},
    )

def emotion_to_voice(emotion: EmotionResult) -> Dict[str, float]:
    intensity = min(1.0, max(0.0, abs(emotion.polarity) * 4 + emotion.subjectivity * 0.2))
    base_rate = 175
    base_volume = 0.9
    base_pitch = 1.0

    if emotion.label == 'Happy':
        rate = base_rate + 20 + 20 * intensity
        volume = min(1.0, base_volume + 0.05 + 0.05 * intensity)
        pitch = base_pitch + 0.08 + 0.12 * intensity
    elif emotion.label in {'Frustrated', 'Negative'}:
        rate = base_rate - 25 - 18 * intensity
        volume = max(0.5, base_volume - 0.12 - 0.1 * intensity)
        pitch = base_pitch - 0.08 - 0.12 * intensity
    elif emotion.label == 'Concerned':
        rate = base_rate - 10 - 8 * intensity
        volume = max(0.55, base_volume - 0.06)
        pitch = base_pitch - 0.04
    else:
        rate = base_rate
        volume = base_volume
        pitch = base_pitch

    return {
        'rate': int(rate),
        'volume': round(volume, 2),
        'pitch': round(pitch, 2),
        'intensity': round(intensity, 3),
    }
