-- Python Dojo — Supabase schema
-- Run this in the Supabase SQL editor (Project > SQL Editor > New query)

create table if not exists levels (
  id int primary key,
  name text not null,
  description text
);

create table if not exists lessons (
  id text primary key,           -- e.g. 'L1-02'
  level_id int references levels(id) not null,
  position int not null,
  name text not null,
  lesson_md text not null
);

create table if not exists level_projects (
  level_id int primary key references levels(id),
  brief_md text not null,
  rubric_md text not null
);

create table if not exists lesson_progress (
  lesson_id text primary key references lessons(id),
  completed boolean not null default false,
  completed_at timestamptz
);

create table if not exists level_progress (
  level_id int primary key references levels(id),
  status text not null default 'locked',   -- locked | unlocked | passed
  best_score int,
  attempts int not null default 0,
  updated_at timestamptz default now()
);

create table if not exists submissions (
  id uuid primary key default gen_random_uuid(),
  level_id int references levels(id) not null,
  code text not null,
  score int,
  strengths text[],
  fixes text[],
  next_step text,
  raw_feedback jsonb,
  created_at timestamptz default now()
);

-- seed levels (lessons/projects/progress rows are seeded by the backend
-- on startup — see backend/content.py)
insert into levels (id, name, description) values
  (0, 'Setup & Basics', 'print, variables, data types, input, basic math'),
  (1, 'Control Flow', 'if/else, loops, comparison & logic operators'),
  (2, 'Data Structures', 'lists, dicts, tuples, sets'),
  (3, 'Functions', 'defining, args/kwargs, return values, scope'),
  (4, 'Files & Errors', 'reading/writing files, try/except'),
  (5, 'OOP', 'classes, objects, inheritance'),
  (6, 'Modules & Libraries', 'imports, pip, using external packages'),
  (7, 'Real Projects', 'combine everything — CLI tools, small games, automations')
on conflict (id) do nothing;
