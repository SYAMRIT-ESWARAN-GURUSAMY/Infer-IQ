from competency_engine import graph

def generate(session: dict) -> dict:
    nodes = graph(session["competencies"])
    strengths = [n["skill"] for n in nodes if n["confidence"] >= .7]
    weak = [n["skill"] for n in nodes if n["confidence"] < .5]
    return {"sessionId": session["id"], "overallConfidence": round(sum(x["confidence"] for x in nodes) / max(1, len(nodes)), 2), "competencies": nodes, "strengths": strengths, "weakAreas": weak, "recommendations": [f"Practice {skill} with focused exercises and explain your reasoning aloud." for skill in weak], "evidence": session["answers"]}
