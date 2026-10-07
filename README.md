# InferIQ MVP

InferIQ is an explainable, adaptive technical interview prototype.  It starts from
resume evidence, chooses the next highest-value question, evaluates concept
evidence in an answer, and maintains a competency graph with an auditable report.

## Run locally — no Docker or installation required

Double-click [ai-engine/web/index.html](ai-engine/web/index.html) to open it in
any modern browser. The browser build contains the interview engine and question
bank locally, so it works without Docker, Python, a server, or an internet
connection (apart from the optional web font).

For the optional FastAPI API version, install Python 3.12+, then run:

```bash
cd ai-engine
py -m pip install -r requirements.txt
py -m uvicorn app:app --reload --port 8000
```

## MVP scope

- Resume text skill extraction and initial competency confidence
- Adaptive question selection using weakness, prerequisite coverage, novelty and
  information-gain scoring
- Concept-level answer evidence and confidence updates
- Explainable final report, including strengths, weak areas and recommendations
- A 44-question bank across Java, Python, SQL, data structures and algorithms,
  web development, system design, cloud and DevOps, and data science and machine learning
- Role-based practice rounds, answer reviews, personalized study plans, progress
  trends, session comparisons, and a concept evidence graph

The engine deliberately uses deterministic lexical evidence matching for the
MVP. This makes local evaluation reproducible; replace it with a
sentence-transformer or hosted embedding provider for production.
