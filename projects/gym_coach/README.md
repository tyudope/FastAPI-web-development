# 🏋️ Gym Coach

A FastAPI app that turns a short intake sheet — stats, training days, experience
level, and a goal — into a full Claude-generated workout programme. It ships with
an industrial, brutalist-styled browser UI, so you can build a programme without
touching the API directly.

---

## What It Does

You fill in the sheet:

```
Age + Height + Weight + Sex + Training Days + Location + Experience Level (+ optional Goal)
```

…and Claude returns one workout per training day — real, named exercises with sets,
reps, and rest periods — plus a short explanation of why the programme fits, and its
pros and cons. The UI renders it as a stack of day cards with a spec-sheet table per
workout; the same data is available as JSON over the API.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web framework | FastAPI |
| Validation | Pydantic v2 |
| Config | pydantic-settings |
| AI | Anthropic Claude (`claude-sonnet-4-5`) |
| UI | Vanilla HTML / CSS / JS (no build step) |

---

## Project Structure

```
gym_coach/
├── app/
│   ├── main.py            # App entry point, CORS, serves the UI, /workout-plan endpoint
│   ├── service.py         # Orchestrates the call + validates Claude's reply
│   ├── claude_client.py   # Thin Anthropic API wrapper (generic, knows nothing of the schema)
│   ├── prompts.py         # System prompt + user-message builder
│   ├── schemas.py         # WorkoutRequest / WorkoutResponse Pydantic models
│   └── config.py          # Settings loaded from .env
├── static/
│   └── index.html         # Browser UI
└── .env                   # Environment variables (not committed)
```

---

## Request & Response

**Request — `WorkoutRequest`**

| Field | Type | Notes |
|---|---|---|
| `name` | string? | optional, 3–50 chars |
| `age` | int | 13–80 |
| `height` | int | centimeters, 30–250 |
| `weight` | int | kilograms, 30–250 |
| `sex` | enum | `male` · `female` |
| `workout_days` | set of enum | one or more of `monday`…`sunday` |
| `preferred_location` | enum | `home` · `gym` · `outdoor` (default `home`) |
| `experience_level` | int | 1–5, where 1 = no experience and 5 = advanced (default 3) |
| `user_context` | string? | optional goal/context, 5–200 chars |

**Response — `WorkoutResponse`**

```jsonc
{
  "workouts": [
    {
      "name": "PULL STRENGTH",
      "day": "monday",
      "target_experience_level": 4,
      "exercises": [
        { "name": "Weighted pull-up", "set_count": 5, "rep_count": 5, "rest_period": 180 }
      ]
    }
  ],
  "reason": "...",
  "pros": "...",
  "cons": "..."
}
```

One workout is returned per training day requested — never more, never fewer.
Every exercise is chosen to be performable at the stated location and appropriate
for the stated experience level.

---

## Setup

**1. Install dependencies** (from the repo root, where `requirements.txt` lives):

```bash
pip install -r requirements.txt
```

**2. Create a `.env` file** inside `projects/gym_coach/`:

```env
ANTHROPIC_API_KEY=your-anthropic-api-key
```

**3. Run the server:**

```bash
cd projects/gym_coach
uvicorn app.main:app --reload
# UI    → http://127.0.0.1:8000/
# Docs  → http://127.0.0.1:8000/docs
```

---

## Endpoints

- `GET /` — browser UI
- `POST /workout-plan` — generate a workout programme
- `GET /health` — health check

---

## Design Notes

- **Response contract enforced, not hoped for.** Claude's reply is validated with
  `WorkoutResponse.model_validate_json`; anything that doesn't fit the schema is
  retried, and only surfaced as a clean `502` if it still doesn't fit after that.
- **Length limits are stated twice.** Field caps (`reason`, `pros`, `cons`) live in
  the Pydantic schema *and* are spelled out in plain language in the system prompt —
  relying on the JSON-schema `maxLength` alone wasn't enough to keep output
  consistently under the limit.
- **Truncation is detected, not silently mis-parsed.** `call_claude` checks
  `stop_reason`; a reply cut off by hitting `max_tokens` raises a distinct
  `ClaudeTruncatedError` instead of being fed to the JSON parser as if it were
  complete.
- **Duration-based exercises are called out explicitly.** `rep_count` means actual
  reps (1–50), never minutes — the prompt tells the model to put running/plank/carry
  durations in the exercise `name` instead, so a 60-minute run can't accidentally
  overflow the reps field.
- **Bounded retry as a reliability net.** `generate_workout_plan` retries up to 3
  times before giving up — even a well-behaved model occasionally drifts outside
  the contract, and a single retry is far cheaper than a failed request.
- **Defensive parsing.** Stray ` ```json ` code fences in the model's reply are
  stripped before validation, in case the model adds them despite instructions.
- **Self-contained themed UI**, served directly from FastAPI — no build step, no
  framework, no data stored server-side.
