from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from content import LEVELS, LESSONS, LEVEL_PROJECTS
import database as db
from grading import grade_submission

app = FastAPI(title="Python Dojo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://learn-python-sand-chi.vercel.app/"],  # tighten this to your frontend's URL once deployed
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    db.seed_content(LEVELS, LESSONS, LEVEL_PROJECTS)


@app.get("/dashboard")
def dashboard():
    return db.get_dashboard()


@app.post("/lessons/{lesson_id}/complete")
def complete_lesson(lesson_id: str):
    if not any(l["id"] == lesson_id for l in LESSONS):
        raise HTTPException(404, "Lesson not found")
    db.mark_lesson_complete(lesson_id)
    return {"ok": True}


@app.get("/levels/{level_id}/project")
def level_project(level_id: int):
    progress = db.get_level_progress(level_id)
    if not progress or progress["status"] == "locked":
        raise HTTPException(403, "This level is still locked")

    level_lessons = [l for l in LESSONS if l["level_id"] == level_id]
    dashboard = db.get_dashboard()
    level = next((lv for lv in dashboard["levels"] if lv["id"] == level_id), None)
    if level_lessons and not level["lessons_done"]:
        raise HTTPException(403, "Finish all lessons in this level first")

    project = db.get_level_project(level_id)
    if not project:
        raise HTTPException(404, "No project defined for this level")
    project["progress"] = progress
    return project


class SubmitPayload(BaseModel):
    level_id: int
    code: str


def _next_level_id(current_id: int) -> int | None:
    ids = sorted(l[0] for l in LEVELS)
    i = ids.index(current_id)
    return ids[i + 1] if i + 1 < len(ids) else None


@app.post("/submit")
async def submit(payload: SubmitPayload):
    level = next((l for l in LEVELS if l[0] == payload.level_id), None)
    project = db.get_level_project(payload.level_id)
    if not level or not project:
        raise HTTPException(404, "Level or project not found")

    result = await grade_submission(
        topic_name=level[1],
        brief_md=project["brief_md"],
        rubric_md=project["rubric_md"],
        code=payload.code,
    )

    next_id = _next_level_id(payload.level_id)
    passed = db.save_submission_and_progress(payload.level_id, payload.code, result, next_id)

    return {**result, "passed": passed, "next_level_id": next_id if passed else None}


@app.get("/health")
def health():
    return {"status": "ok"}
