import re
from embedding_service import similarity

def _contains_concept(answer: str, concept: str) -> bool:
    if concept.lower() == "@":
        return "@" in answer
    if concept.lower() == "map":
        return bool(re.search(r"\b(?:map|hashmap)\b", answer, re.IGNORECASE))
    pattern = r"(?<![a-z0-9])" + re.escape(concept.lower()) + r"(?![a-z0-9])"
    return bool(re.search(pattern, answer, re.IGNORECASE))

def extract_evidence(answer: str, question: dict) -> dict:
    detected = [c for c in question["concepts"] if _contains_concept(answer, c)]
    # Include semantically close rubric evidence only when direct concept matching is sparse.
    score = len(detected) / len(question["concepts"])
    semantic = similarity(answer, " ".join(question["concepts"]))
    evidence_score = round(min(1.0, .8 * score + .2 * semantic), 2)
    return {"detected": detected, "missing": [c for c in question["concepts"] if c not in detected], "similarity": round(semantic, 2), "score": evidence_score}
