## Uber Meal Recommender

Small FastAPI app that recommends a meal based on time of day, mood, and hunger level. It uses OpenAI for the recommendation and a local SQLite database for previous orders. There’s a simple UI at `/` and a JSON API at `/recommend`.

## What’s inside
- FastAPI app with `/health`, `/recommend`, and `/` UI routes
- SQLite database seeded on startup
- Prompt builder that includes previous orders in the context
- Basic JSON schema validation for model output

## Setup
1. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Create `projects/uber_meal_recommender/.env`:
```bash
DATABASE_URL=sqlite:///./app.db
OPENAI_MODEL=gpt-4.1-mini
OPENAI_API_KEY=your_key_here
```

## Run the app
From the repo root:
```bash
uvicorn projects.uber_meal_recommender.app.main:app --reload
```

Then visit:
- `http://localhost:8000/` for the UI
- `http://localhost:8000/docs` for Swagger

## API
### POST `/recommend`
Request body:
```json
{
  "phase_of_day": "morning",
  "mood": "cozy",
  "hungry": 3
}
```

Response:
```json
{
  "meal": "Example Meal",
  "summary": "Why this meal is a good fit..."
}
```

### GET `/health`
Returns `{ "status": "ok" }`.

## Notes
- The database is seeded on app startup.
- `phase_of_day` is limited to `morning`, `afternoon`, `evening`.
- `mood` is optional and limited to 80 characters.

## Useful scripts
Print all orders:
```bash
cd projects/uber_meal_recommender
../.venv/bin/python -m app.db.get_all
```
