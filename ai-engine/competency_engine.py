def update(competencies: dict[str, float], skill: str, evidence: dict) -> dict:
    old = competencies.get(skill, .35)
    # Bayesian-style smoothing: evidence has more effect early, but cannot cause abrupt swings.
    learning_rate = .38 * (1 - old / 2)
    new = old + learning_rate * (evidence["score"] - old)
    competencies[skill] = round(max(.05, min(.95, new)), 2)
    return competencies

def graph(competencies: dict[str, float]) -> list[dict]:
    return [{"skill": skill, "confidence": value, "status": "strong" if value >= .7 else "developing" if value >= .45 else "weak"} for skill, value in sorted(competencies.items())]
