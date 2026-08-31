# Python Dojo — Workshop

A self-hosted, AI-graded Python learning app. Each level has a few short
lessons, then one combined project that Claude grades against a rubric.
Score 70+ to unlock the next level.

## Structure

```
python-dojo/
├── backend/        FastAPI app — talks to Supabase + the Claude API
├── frontend/        React (Vite) app — the UI
└── supabase/
    └── schema.sql   Run this once in your Supabase project
```

## 1. Set up Supabase (the database)

1. Create a free project at https://supabase.com
2. Go to **SQL Editor → New query**, paste the contents of
   `supabase/schema.sql`, and run it.
3. Go to **Project Settings → API** and copy:
   - **Project URL** → `SUPABASE_URL`
   - **service_role key** (not the anon key — the backend needs write access)
     → `SUPABASE_SERVICE_KEY`

## 2. Get a Claude API key

1. Go to https://console.anthropic.com and sign up (free $5 credit, no card needed)
2. Create an API key → `ANTHROPIC_API_KEY`

## 3. Run the backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then fill in your real keys
uvicorn main:app --reload --port 8000
```

Visit http://localhost:8000/health — you should see `{"status": "ok"}`.
On first run it seeds the levels/lessons/project content into Supabase.

## 4. Run the frontend

```bash
cd frontend
npm install
cp .env.example .env            # VITE_API_URL should point at your backend
npm run dev
```

Open the URL it prints (usually http://localhost:5173).

## How grading works

When you submit a level's project, the backend sends your code + the
level's rubric to the Claude API (Haiku 4.5 by default — cheap and plenty
capable for this) and asks for structured JSON back: a score, strengths,
things to fix, and what to focus on next. 70+ unlocks the next level;
below that, you can revise and resubmit.

## Adding more levels/lessons

Everything beyond Level 0 and Level 1 is stubbed out as empty levels in
`backend/content.py` — add lessons and a `LEVEL_PROJECTS` entry for each
one the same way the first two are written, restart the backend, and
they'll seed into Supabase automatically (existing progress isn't
touched — `seed_content` only inserts rows that don't exist yet).

## Deploying so it's reachable from any device

- **Frontend** → Vercel or Netlify (free tier): point it at this
  `frontend/` folder, set `VITE_API_URL` to your deployed backend's URL.
- **Backend** → Render or Railway (free tier): point it at `backend/`,
  set the same three env vars from `.env.example` in their dashboard.
- Supabase is already cloud-hosted, so nothing to do there.

Once both are deployed, the app works from your phone, laptop, anywhere —
same progress everywhere, since it all lives in one Supabase database.

## Cost

Realistically close to free. Grading one project is a few thousand
tokens at most — at Haiku rates that's a fraction of a cent. Your $5
signup credit covers hundreds of submissions before you'd ever need to
add funds.
