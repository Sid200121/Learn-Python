import os
from supabase import create_client, Client

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def seed_content(levels: list[tuple], lessons: list[dict], level_projects: dict):
    """Idempotently make sure levels/lessons/projects/progress rows exist."""
    for level_id, name, description in levels:
        supabase.table("levels").upsert(
            {"id": level_id, "name": name, "description": description}
        ).execute()

    for lesson in lessons:
        supabase.table("lessons").upsert(lesson).execute()
        existing = (
            supabase.table("lesson_progress").select("*").eq("lesson_id", lesson["id"]).execute()
        )
        if not existing.data:
            supabase.table("lesson_progress").insert(
                {"lesson_id": lesson["id"], "completed": False}
            ).execute()

    for level_id, project in level_projects.items():
        supabase.table("level_projects").upsert(
            {"level_id": level_id, **project}
        ).execute()

    for level_id, _, _ in levels:
        existing = (
            supabase.table("level_progress").select("*").eq("level_id", level_id).execute()
        )
        if not existing.data:
            status = "unlocked" if level_id == levels[0][0] else "locked"
            supabase.table("level_progress").insert(
                {"level_id": level_id, "status": status, "attempts": 0}
            ).execute()


def get_dashboard():
    levels = supabase.table("levels").select("*").order("id").execute().data
    progress = {
        p["level_id"]: p for p in supabase.table("level_progress").select("*").execute().data
    }
    lessons = supabase.table("lessons").select("*").order("level_id,position").execute().data
    lesson_progress = {
        p["lesson_id"]: p for p in supabase.table("lesson_progress").select("*").execute().data
    }

    for level in levels:
        p = progress.get(level["id"], {})
        level["status"] = p.get("status", "locked")
        level["best_score"] = p.get("best_score")
        level["attempts"] = p.get("attempts", 0)
        level_lessons = [l for l in lessons if l["level_id"] == level["id"]]
        for l in level_lessons:
            l["completed"] = lesson_progress.get(l["id"], {}).get("completed", False)
        level["lessons"] = level_lessons
        level["lessons_done"] = all(l["completed"] for l in level_lessons) if level_lessons else False

    return {"levels": levels}


def get_level_progress(level_id: int):
    res = supabase.table("level_progress").select("*").eq("level_id", level_id).single().execute()
    return res.data


def mark_lesson_complete(lesson_id: str):
    supabase.table("lesson_progress").update(
        {"completed": True, "completed_at": "now()"}
    ).eq("lesson_id", lesson_id).execute()


def get_level_project(level_id: int):
    res = (
        supabase.table("level_projects").select("*").eq("level_id", level_id).single().execute()
    )
    return res.data


def save_submission_and_progress(level_id: int, code: str, result: dict, next_level_id: int | None):
    supabase.table("submissions").insert(
        {
            "level_id": level_id,
            "code": code,
            "score": result["score"],
            "strengths": result.get("strengths", []),
            "fixes": result.get("fixes", []),
            "next_step": result.get("next_step"),
            "raw_feedback": result,
        }
    ).execute()

    prog = get_level_progress(level_id) or {"attempts": 0, "best_score": None}
    passed = result["score"] >= 70
    new_best = max(result["score"], prog.get("best_score") or 0)

    supabase.table("level_progress").update(
        {
            "attempts": prog.get("attempts", 0) + 1,
            "best_score": new_best,
            "status": "passed" if passed else "unlocked",
        }
    ).eq("level_id", level_id).execute()

    if passed and next_level_id is not None:
        next_prog = get_level_progress(next_level_id)
        if next_prog and next_prog["status"] == "locked":
            supabase.table("level_progress").update({"status": "unlocked"}).eq(
                "level_id", next_level_id
            ).execute()

    return passed
