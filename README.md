# AI Engineering Lab

A personal workspace for building AI-powered backend projects. Each project explores a specific set of engineering concepts around LLMs, APIs, and data — from structured output and prompt design to ORM integration and service-layer architecture.

---

## Repository Structure

```
ai-engineering-lab/
├── projects/          # Standalone AI/backend projects
│   ├── dreamsense/
│   ├── ai_dj/
│   ├── uber_meal_recommender/
│   ├── weekly_study_with_ai/
│   └── date_night/
└── Learning_Phase/    # Chapter exercises and experiments
```

---

## Projects

| Project | Description | Key Concepts |
|---|---|---|
| [DreamSense](projects/dreamsense) | AI dream reflection with structured, safe output | Output contracts, safety guardrails, schema-first design |
| [AI DJ](projects/ai_dj) | Generates DJ-ready playlists from a theme and emotional flow | Strict schema validation, structured generation |
| [Uber Meal Recommender](projects/uber_meal_recommender) | Context-aware meal recommendations using order history | Prompt enrichment with DB context, SQLite integration |
| [Study with AI](projects/weekly_study_with_ai) | Study plan analyzer powered by AI | SQLAlchemy ORM, LLM wrapper pattern, dependency injection |
| [Date Night Planner](projects/date_night) | Generates a main + backup date plan from theme, energy, budget, and city | Claude integration, schema-validated output, themed UI |

See [projects/README.md](projects/README.md) for detailed breakdowns of each project.

---

## Tech Stack

All projects are built on a shared foundation:

- **FastAPI** — web framework and API layer
- **Pydantic v2** — request/response validation and schema enforcement
- **LLM APIs** — OpenAI (`gpt-4.1-mini`) and Anthropic Claude (`claude-sonnet-4-6`, used by Date Night Planner)
- **SQLAlchemy / SQLite** — data persistence where applicable
- **pydantic-settings** — environment variable management

---

## Running a Project

Each project is self-contained. The general steps are:

```bash
# 1. Go into the project folder
cd projects/<project-name>

# 2. Create a .env file with your credentials
#    (OPENAI_API_KEY for most projects, ANTHROPIC_API_KEY for date_night)
echo "OPENAI_API_KEY=your-key-here" > .env

# 3. Install dependencies (from the repo root)
pip install -r requirements.txt

# 4. Start the server
uvicorn app.main:app --reload
```

Refer to each project’s own README for specific setup details and endpoints.

---

## Notes

- `.env` files are gitignored — never commit API keys
- Each project may have its own virtual environment and dependencies
