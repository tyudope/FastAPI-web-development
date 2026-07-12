# Projects

A collection of AI-powered backend projects built with FastAPI and the OpenAI API. Each project focuses on a specific set of engineering concepts — from structured LLM output and prompt design to database integration and service-layer architecture.

---

## Projects at a Glance

| Project | Focus | Stack |
|---|---|---|
| [DreamSense](#dreamsense) | Structured LLM output, output contracts, safety guardrails | FastAPI, OpenAI, Pydantic, Jinja2 |
| [AI DJ](#ai-dj) | Schema-driven generation, strict validation | FastAPI, OpenAI, Pydantic |
| [Uber Meal Recommender](#uber-meal-recommender) | Context-aware prompts, SQLite integration | FastAPI, OpenAI, SQLite |
| [Study with AI](#study-with-ai) | SQLAlchemy ORM, LLM wrapper pattern | FastAPI, OpenAI, SQLAlchemy |
| [Date Night Planner](#date-night-planner) | Schema-validated Claude output, themed UI | FastAPI, Anthropic Claude, Pydantic |
| [Gym Coach](#gym-coach) | Claude-generated workout programmes, strict field-length contracts | FastAPI, Anthropic Claude, Pydantic |

---

## DreamSense

> Structured, non-diagnostic psychological reflections on user-described dreams.

The focus of this project is on **building reliable systems around probabilistic models** — enforcing strict output contracts, handling model failures gracefully, and designing safe LLM interactions.

**Key concepts**
- Schema-first GenAI design with Pydantic
- Safety guardrails enforced in code, not just prompts
- Deterministic API contracts around unpredictable model output
- Defensive handling of invalid or unsafe model responses

**What it does**
Takes a dream description and returns a structured analysis: summary, detected emotions and themes, a soft psychological interpretation, reflective questions, and gentle feedback. No medical or mental-health claims are made.

**Endpoints**
- `POST /dreams/analyze` — analyze a dream description
- `GET /health/openai` — verify API key and model access

**Tech stack** — FastAPI · Pydantic · OpenAI (Responses API) · Jinja2

**Run**
```bash
cd projects/dreamsense
uvicorn app.main:app --reload
# UI → http://127.0.0.1:8000/
```

---

## AI DJ

> Generate a DJ-ready playlist from a party theme, emotional flow, and duration.

This project focuses on **strict schema-driven generation** — using structured output from OpenAI to produce playlists that conform to a validated response contract.

**Key concepts**
- Structured output with strict Pydantic validation on both request and response
- Prompt templates designed to produce consistent, schema-conforming results
- Client-side validation with live feedback in the UI

**What it does**
Takes a party theme, a sequence of emotional phases (e.g. mysterious → euphoric → warm glide-down), and a duration in minutes. Returns a curated song list with a short analysis of the curation choices.

**Endpoints**
- `POST /dj/create_playlist` — generate a playlist

**Validation limits**
- `theme_of_party`: 20–4000 characters
- `emotional_flow_of_the_songs`: 2–5 items
- `duration`: 10–600 minutes

**Tech stack** — FastAPI · Pydantic · OpenAI (Responses API)

**Run**
```bash
cd projects/ai_dj
uvicorn app.main:app --reload
# UI → http://127.0.0.1:8000/ui
```

---

## Uber Meal Recommender

> Context-aware meal recommendations powered by AI and informed by order history.

This project focuses on **enriching prompts with database context** — pulling previous orders from SQLite and including them in the prompt to make recommendations feel personalized.

**Key concepts**
- Prompt construction using live data from a relational database
- SQLite integration with a startup-seeded order history
- JSON schema validation for structured model output

**What it does**
Takes the time of day, mood, and hunger level, then recommends a meal and explains why it's a good fit — taking previous orders into account.

**Endpoints**
- `POST /recommend` — get a meal recommendation
- `GET /health` — health check

**Tech stack** — FastAPI · Pydantic · OpenAI · SQLite

**Run**
```bash
cd projects/uber_meal_recommender
uvicorn app.main:app --reload
# UI → http://localhost:8000/
# Docs → http://localhost:8000/docs
```

---

## Study with AI

> Define a study plan and get an AI-powered analysis of its strengths, risks, and improvements.

This project focuses on **SQLAlchemy ORM patterns and the LLM-as-service layer** — building a clean three-tier data hierarchy and wrapping the AI call in a dedicated service.

**Key concepts**
- SQLAlchemy 2.0 relationships: one-to-one (Goal ↔ Routine) and one-to-many (Routine ↔ Tasks) with cascade deletes
- Pydantic v2 schemas separating ORM models from API shapes
- FastAPI dependency injection for database sessions
- Prompt engineering from structured relational data
- Thin AI client wrapper for clean separation of concerns

**What it does**
You build a study plan in three layers — Goal → Routine → Tasks — then trigger an AI analysis. The model returns a structured evaluation covering strengths, weaknesses, risks, improvements, and recommended adjustments.

**Endpoints**
- `POST /goals` / `GET /goals` / `DELETE /goals/{id}` — manage goals
- `POST /goals/{id}/routine` — attach a routine to a goal
- `GET /routines` / `DELETE /routines/{id}` — manage routines
- `POST /routines/{id}/tasks` — add tasks to a routine
- `GET /tasks` / `DELETE /tasks/{id}` — manage tasks
- `POST /analysis/goals/{id}` — run AI analysis on a full study plan

**Tech stack** — FastAPI · SQLAlchemy 2.0 · SQLite · Pydantic v2 · OpenAI

**Run**
```bash
cd projects/weekly_study_with_ai
uvicorn app.main:app --reload
# UI → http://localhost:8000/
# Docs → http://localhost:8000/docs
```

---

## Date Night Planner

> Turn a theme, energy level, budget, and city into a main + backup date plan.

This project focuses on **schema-validated LLM output with Anthropic Claude** — embedding the response JSON schema in the system prompt, then validating Claude's reply against a strict Pydantic model and surfacing failures as clean API errors.

**Key concepts**
- Claude integration via a thin, schema-agnostic client wrapper
- Response contract enforced with `model_validate_json` + graceful `502` on invalid output
- Defensive parsing (stripping stray code fences from the model reply)
- Self-contained themed UI served directly from FastAPI

**What it does**
Takes a theme (cozy, romantic, adventure, comedy, food, unique), an energy level (1–5), a budget in PLN, a city, and optional context. Returns a main plan and a realistic backup plan — each with a title, description, and estimated cost — plus a short note on why it fits.

**Endpoints**
- `GET /` — browser UI
- `POST /date-night` — generate a date plan
- `GET /health` — health check

**Tech stack** — FastAPI · Pydantic v2 · Anthropic Claude (`claude-sonnet-4-6`)

**Run**
```bash
cd projects/date_night
uvicorn app.main:app --reload
# UI → http://127.0.0.1:8000/
# Docs → http://127.0.0.1:8000/docs
```

---

## Gym Coach

> Turn a stats sheet, training days, and a goal into a full Claude-generated workout programme.

This project focuses on **making an LLM's output contract actually stick** — the
system prompt states field-length limits in plain language *and* the Pydantic
schema enforces them numerically, truncated replies are detected via `stop_reason`
instead of being mis-parsed, and a bounded retry absorbs the occasional
out-of-contract response instead of failing the request outright.

**Key concepts**
- Claude integration via a thin, schema-agnostic client wrapper
- Response contract enforced with `model_validate_json` + bounded retry + graceful `502` on repeated failure
- Prompt-level *and* schema-level length limits, reinforcing each other
- Truncation detected via `stop_reason` rather than fed to the JSON parser as complete
- Defensive parsing (stripping stray code fences from the model reply)
- Self-contained industrial-styled UI served directly from FastAPI

**What it does**
Takes age, height, weight, sex, training days, preferred location (home/gym/outdoor),
and an experience level (1–5), plus an optional goal. Returns one workout per
training day — real, named exercises with sets, reps, and rest — plus a short
explanation of why the programme fits, and its pros and cons.

**Endpoints**
- `GET /` — browser UI
- `POST /workout-plan` — generate a workout programme
- `GET /health` — health check

**Tech stack** — FastAPI · Pydantic v2 · Anthropic Claude (`claude-sonnet-4-5`)

**Run**
```bash
cd projects/gym_coach
uvicorn app.main:app --reload
# UI → http://127.0.0.1:8000/
# Docs → http://127.0.0.1:8000/docs
```

---

## Common Setup

All projects use a `.env` file for configuration. At minimum:

```env
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4.1-mini
```

Date Night Planner and Gym Coach use Anthropic Claude instead, so they require:

```env
ANTHROPIC_API_KEY=your-anthropic-api-key
```

Projects that use a database also require:

```env
DATABASE_URL=sqlite:///./app.db
```

Install dependencies from the repo root:

```bash
pip install -r requirements.txt
```
