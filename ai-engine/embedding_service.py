"""Small deterministic embedding utility used when no model service is configured."""
import math
import re
from collections import Counter

def tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z][a-zA-Z+#.]*", text.lower())

def similarity(left: str, right: str) -> float:
    a, b = Counter(tokens(left)), Counter(tokens(right))
    if not a or not b:
        return 0.0
    dot = sum(a[key] * b[key] for key in a.keys() & b.keys())
    return dot / math.sqrt(sum(x*x for x in a.values()) * sum(x*x for x in b.values()))
