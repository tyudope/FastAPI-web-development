# 🌙 Date Night Planner

A small FastAPI app that turns a few preferences into a Claude-generated date-night
plan — complete with a **main plan**, a realistic **backup plan**, and a short note
on **why it fits**. It ships with a themed browser UI so you can plan a night without
ever touching the API directly.

---

## What It Does

You tell it the vibe:

```
Theme  +  Energy level  +  Budget  +  City  (+ optional context)
```

…and Claude returns two concrete, city-specific plans that stay within budget and
match both partners' energy. The UI renders them as cards with cost badges and a
budget check; the same data is available as JSON over the API.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web framework | FastAPI |
| Validation | Pydantic v2 |
| Config | pydantic-settings |
| AI | Anthropic Claude (`claude-sonnet-4-6`) |
| UI | Vanilla HTML / CSS / JS (no build step) |

---

## Project Structure

```
date_night/
├── app/
│   ├── main.py            # App entry point, CORS, serves the UI, /date-night endpoint
│   ├── service.py         # Orchestrates the call + validates Claude's reply
│   ├── claude_client.py   # Thin Anthropic API wrapper (generic, knows nothing of the schema)
│   ├── prompts.py         # System prompt + user-message builder
│   ├── schemas.py         # PlanRequest / PlanResponse Pydantic models
│   └── config.py          # Settings loaded from .env
├── static/
│   └── index.html         # Browser UI
└── .env                   # Environment variables (not committed)
```

---

## Request & Response

**Request — `PlanRequest`**

| Field | Type | Notes |
|---|---|---|
| `theme` | enum | `cozy` · `romantic` · `adventure` · `comedy` · `food` · `unique` (default `cozy`) |
| `energy_level` | int | 1–5, where 1 = low and 5 = high (default 3) |
| `budget` | int | total budget in PLN, ≥ 0 |
| `city` | string | required, 1–50 chars |
| `user_context` | string? | optional extra context, ≤ 200 chars |

**Response — `PlanResponse`**

```jsonc
{
  "main_plan":   { "title": "...", "description": "...", "estimated_cost": 180 },
  "backup_plan": { "title": "...", "description": "...", "estimated_cost": 90  },
  "why_it_fits": "..."
}
```

---

## Setup

**1. Install dependencies** (from the repo root, where `requirements.txt` lives):
```bash
pip install -r requirements.txt
pip install anthropic
```

**2. Create a `.env` file** in `projects/date_night/`:
```env
ANTHROPIC_API_KEY=your-anthropic-api-key
```

**3. Run the server** from `projects/date_night/`:
```bash
uvicorn app.main:app --reload
```

**4. Open the UI** at `http://127.0.0.1:8000`

Interactive API docs are at `http://127.0.0.1:8000/docs`.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET`  | `/` | Serves the browser UI |
| `GET`  | `/health` | Liveness check → `{"status": "ok"}` |
| `POST` | `/date-night` | Generate a date plan from a `PlanRequest` |

Example:
```bash
curl -X POST http://127.0.0.1:8000/date-night \
  -H "Content-Type: application/json" \
  -d '{"theme":"romantic","energy_level":3,"budget":200,"city":"Kraków"}'
```

---

## How It Works

1. The UI (or any client) sends a `PlanRequest` to `POST /date-night`.
2. `prompts.build_user_message` formats the request; `SYSTEM_PROMPT` embeds the
   `PlanResponse` JSON schema so Claude returns parseable output.
3. `claude_client.call_claude` makes the API call and returns the raw text.
4. `service.generate_date_plan` strips any stray code fences and validates the
   reply against `PlanResponse`. Invalid output raises `PlanGenerationError`,
   which the endpoint surfaces as a clean `502`.

---

## Notes

- Estimated costs and plans are AI suggestions — double-check opening hours and
  prices before you head out.
- The model is set in [`app/claude_client.py`](app/claude_client.py); swap `MODEL`
  to use a different Claude model.
