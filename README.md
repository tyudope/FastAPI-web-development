## AI Engineering Lab

This repository is a workspace for small AI/ML experiments and mini‑projects. Each project lives under `projects/` and is mostly self‑contained with its own README and run steps.

## Structure
- `projects/` — individual projects (APIs, prototypes, notebooks, etc.)
- `requirements.txt` — top‑level Python tools used across projects

## Current projects
- `projects/uber_meal_recommender` — Meal recommendation API with a minimal UI. It uses SQLite for prior orders and OpenAI for a strict JSON response, then validates against a schema. README: `projects/uber_meal_recommender/README.md`.
- `projects/ai_dj` — Generates DJ‑ready playlists from a party theme and emotional flow. Includes a small UI, client‑side validation, and schema‑checked API responses. README: `projects/ai_dj/README.md`.
- `projects/dreamsense` — Dream reflection app focused on safe, structured, non‑diagnostic output. Server‑rendered UI, explicit guardrails, and a schema‑first prompt flow. README: `projects/dreamsense/README.md`.

## How to run a project
1. Go into the project folder.
2. Follow the project’s README for setup and run instructions.

## Notes
- Keep secrets in `.env` files inside each project and do not commit them.
- Each project may have its own dependencies and virtual environment.
