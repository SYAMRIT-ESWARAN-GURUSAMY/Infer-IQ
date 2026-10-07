def rank_questions(questions: list[dict], competencies: dict[str, float], asked: set[str]) -> list[dict]:
    ranked = []
    for q in questions:
        if q["id"] in asked:
            continue
        confidence = competencies.get(q["skill"], .35)
        weakness = 1 - confidence
        prerequisite_gap = sum(1 - competencies.get(p, .35) for p in q["prerequisites"]) / max(1, len(q["prerequisites"]))
        difficulty_fit = 1 - abs((q["difficulty"] / 3) - confidence)
        information_gain = .52 * weakness + .28 * difficulty_fit + .20 * prerequisite_gap
        ranked.append((information_gain, q, {"weakness": round(weakness, 2), "difficultyFit": round(difficulty_fit, 2), "prerequisiteGap": round(prerequisite_gap, 2)}))
    return sorted(ranked, key=lambda item: item[0], reverse=True)

def select_question(questions, competencies, asked):
    score, question, factors = rank_questions(questions, competencies, asked)[0]
    return {**question, "selection": {"informationGain": round(score, 2), "factors": factors, "reason": f"Targets {question['skill']} at {round(competencies.get(question['skill'], .35)*100)}% confidence."}}
