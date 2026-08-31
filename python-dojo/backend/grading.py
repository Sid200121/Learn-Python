"""
Sends a submission to the Claude API and gets back structured JSON feedback.
"""
import os
import json
import httpx

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
MODEL = os.environ.get("GRADING_MODEL", "claude-haiku-4-5-20251001")

GRADER_SYSTEM_PROMPT = """You are a patient, encouraging-but-honest Python \
mentor grading a total beginner's project submission. You are not a harsh \
critic and not a cheerleader — you tell the truth plainly and kindly.

Respond with ONLY a JSON object (no markdown fences, no preamble) shaped \
exactly like this:

{
  "score": <int 0-100>,
  "strengths": ["short phrase", "short phrase"],
  "fixes": ["short phrase", "short phrase"],
  "feedback": "2-4 sentences of encouraging-but-honest prose feedback",
  "next_step": "one sentence telling them what to focus on next"
}

Score guidance: 90+ means it fully meets the brief with clean, working \
code. 70-89 means it works and meets the brief but has rough edges. \
50-69 means it partially works or misses part of the brief. Below 50 \
means it doesn't run or misses the core requirement. A learner needs to \
score 70+ on a topic to unlock the next one, so be fair and accurate — \
don't inflate scores to be nice."""


async def grade_submission(topic_name: str, brief_md: str, rubric_md: str, code: str) -> dict:
    user_prompt = f"""Topic: {topic_name}

Project brief given to the learner:
{brief_md}

What to check for (rubric):
{rubric_md}

Learner's submitted code:
```python
{code}
```

Grade this submission now."""

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": MODEL,
                "max_tokens": 1000,
                "system": GRADER_SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": user_prompt}],
            },
        )
        resp.raise_for_status()
        data = resp.json()

    text = "".join(block["text"] for block in data["content"] if block["type"] == "text")
    text = text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        # fall back gracefully rather than crashing the request
        parsed = {
            "score": 0,
            "strengths": [],
            "fixes": ["Grader response could not be parsed — try resubmitting."],
            "feedback": "Something went wrong reading the AI grader's response.",
            "next_step": "Resubmit your code.",
        }
    return parsed
