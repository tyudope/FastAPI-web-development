# Study with AI

A learning project that combines **SQLAlchemy ORM** and **OpenAI API** integration through a FastAPI backend. The app lets you define study goals, attach routines and tasks to them, and then get an AI-powered analysis of your study plan.

---

## What It Does

You build a study plan in three layers:

```
Goal  →  Routine  →  Tasks
```

Once the hierarchy is in place, you can trigger an AI analysis that evaluates your plan across five dimensions: strengths, weaknesses, risks, improvements, and recommended adjustments.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web framework | FastAPI |
| ORM | SQLAlchemy 2.0 |
| Database | SQLite |
| Validation | Pydantic v2 |
| AI | OpenAI API (`gpt-4.1-mini`) |
| Config | pydantic-settings |
| UI | Vanilla HTML / CSS / JS |

---

## Project Structure

```
weekly_study_with_ai/
├── app/
│   ├── main.py                  # App entry point, middleware, router registration
│   ├── core/
│   │   └── config.py            # Settings loaded from .env
│   ├── db/
│   │   └── session.py           # SQLAlchemy engine & session dependency
│   ├── models/
│   │   ├── base.py              # DeclarativeBase
│   │   ├── goal.py              # Goal model
│   │   ├── routine.py           # Routine model (one-to-one with Goal)
│   │   └── task.py              # Task model (many-to-one with Routine)
│   ├── schemas/
│   │   ├── goal.py
│   │   ├── routine.py
│   │   ├── task.py
│   │   └── analysis.py
│   ├── routers/
│   │   ├── goal.py
│   │   ├── routine.py
│   │   ├── task.py
│   │   └── analysis.py
│   └── services/
│       ├── prompt_builder.py    # Builds the prompt sent to OpenAI
│       └── ai_client.py         # OpenAI API wrapper
├── static/
│   └── index.html               # Browser UI
├── .env                         # Environment variables (not committed)
└── app.db                       # SQLite database file
```

---

## Setup

**1. Install dependencies**
```bash
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings openai
```

**2. Create a `.env` file** in the project root:
```env
DATABASE_URL=sqlite:///./app.db
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4.1-mini
```

**3. Run the server** from the project root:
```bash
uvicorn app.main:app --reload
```

**4. Open the UI** at `http://localhost:8000`

Interactive API docs are also available at `http://localhost:8000/docs`.

---

## API Endpoints

### Goals
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/goals` | Create a goal |
| `GET` | `/goals` | List all goals |
| `GET` | `/goals/{goal_id}` | Get a goal by ID |
| `DELETE` | `/goals/{goal_id}` | Delete a goal (cascades to routine & tasks) |
| `POST` | `/goals/{goal_id}/routine` | Create a routine for a goal |

### Routines
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/routines` | List all routines |
| `GET` | `/routines/{routine_id}` | Get a routine by ID |
| `DELETE` | `/routines/{routine_id}` | Delete a routine (cascades to tasks) |
| `POST` | `/routines/{routine_id}/tasks` | Add a task to a routine |

### Tasks
| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/tasks` | List all tasks |
| `GET` | `/tasks/{task_id}` | Get a task by ID |
| `DELETE` | `/tasks/{task_id}` | Delete a task |

### Analysis
| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/analysis/goals/{goal_id}` | Run AI analysis on a goal's full plan |

---

## How to Use

1. **Goals tab** — create a goal, then use its ID to attach a routine
2. **Routines tab** — use the routine ID to add tasks
3. **Analysis tab** — enter the goal ID and click **Analyze** to get AI feedback

> The analysis requires the full hierarchy: goal → routine → at least one task.

---

## Key Learning Concepts

- **SQLAlchemy relationships** — one-to-one (Goal ↔ Routine) and one-to-many (Routine ↔ Tasks) with cascade deletes
- **Pydantic v2 schemas** — separating ORM models from API input/output shapes
- **FastAPI dependency injection** — database sessions via `Depends(get_db)`
- **LLM prompt engineering** — structuring a prompt from relational data and parsing the response
- **OpenAI API wrapper** — thin service layer around the client for clean separation of concerns
