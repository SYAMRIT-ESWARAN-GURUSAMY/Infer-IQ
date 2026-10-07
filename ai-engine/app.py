from pathlib import Path
import json, uuid
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from resume_parser import parse_resume
from decision_engine import select_question
from evidence_engine import extract_evidence
from competency_engine import update
from report_generator import generate

ROOT = Path(__file__).parent
QUESTIONS = json.loads((ROOT / "data" / "question_bank.json").read_text())
SESSIONS: dict[str, dict] = {}
app = FastAPI(title="InferIQ Assessment API", version="0.1.0")
app.mount("/app", StaticFiles(directory=ROOT / "web"), name="web")

class StartRequest(BaseModel):
    candidate_name: str = Field(min_length=1, max_length=80)
    resume_text: str = Field(min_length=1)
class AnswerRequest(BaseModel):
    question_id: str
    answer: str = Field(min_length=1)

@app.get("/", include_in_schema=False)
def home(): return FileResponse(ROOT / "web" / "index.html")

@app.get("/api/health")
def health(): return {"status": "ok", "questions": len(QUESTIONS)}

@app.post("/api/interviews")
def start_interview(body: StartRequest):
    parsed = parse_resume(body.resume_text)
    competencies = parsed["competencies"] or {skill: .35 for skill in ("Java", "Python", "SQL", "DSA", "Web Development", "System Design", "Cloud & DevOps", "Data Science & ML")}
    session_id = str(uuid.uuid4())
    session = {"id": session_id, "candidate": body.candidate_name, "competencies": competencies, "asked": set(), "answers": []}
    SESSIONS[session_id] = session
    return {"sessionId": session_id, "resume": parsed, "question": select_question(QUESTIONS, competencies, session["asked"])}

@app.get("/api/interviews/{session_id}/next")
def next_question(session_id: str):
    session = SESSIONS.get(session_id)
    if not session: raise HTTPException(404, "Interview not found")
    if len(session["asked"]) >= len(QUESTIONS): return {"complete": True}
    return select_question(QUESTIONS, session["competencies"], session["asked"])

@app.post("/api/interviews/{session_id}/answers")
def submit_answer(session_id: str, body: AnswerRequest):
    session = SESSIONS.get(session_id)
    question = next((q for q in QUESTIONS if q["id"] == body.question_id), None)
    if not session or not question: raise HTTPException(404, "Interview or question not found")
    if body.question_id in session["asked"]: raise HTTPException(409, "Question already answered")
    evidence = extract_evidence(body.answer, question)
    before = session["competencies"].get(question["skill"], .35)
    update(session["competencies"], question["skill"], evidence)
    session["asked"].add(body.question_id)
    session["answers"].append({"question": question["question"], "skill": question["skill"], "before": before, "after": session["competencies"][question["skill"]], "evidence": evidence})
    return {"evidence": evidence, "competencies": session["competencies"], "next": select_question(QUESTIONS, session["competencies"], session["asked"]) if len(session["asked"]) < len(QUESTIONS) else None}

@app.get("/api/interviews/{session_id}/report")
def report(session_id: str):
    session = SESSIONS.get(session_id)
    if not session: raise HTTPException(404, "Interview not found")
    return generate(session)
