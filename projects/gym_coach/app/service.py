from pydantic import ValidationError

from app.schemas import WorkoutResponse, WorkoutRequest
from app.prompts import SYSTEM_PROMPT, build_user_message
from app.claude_client import call_claude, ClaudeTruncatedError



class PlanGenerationError(Exception):
    """Claude's reply could not be turned into a valid WorkoutResponse """


def _strip_fences(text: str) -> str:
    """Remove ```json ... ``` fences if the model added them despite instructions"""

    text = text.strip()
    if text.startswith("```"):
        text = (
            text.removeprefix("```json")
            .removeprefix("```")
            .removesuffix("```")
            .strip()
        )

    
    return text




MAX_ATTEMPTS = 3


def generate_workout_plan(req: WorkoutRequest) -> WorkoutResponse:
    user_msg = build_user_message(req)
    last_error: Exception | None = None

    for _ in range(MAX_ATTEMPTS):
        try:
            raw = call_claude(SYSTEM_PROMPT, user_msg)
            cleaned = _strip_fences(raw)
            return WorkoutResponse.model_validate_json(cleaned)
        except ClaudeTruncatedError as e:
            last_error = e
        except ValidationError as e:
            last_error = PlanGenerationError(
                f"Claude returned output that didn't fit WorkoutResponse. Raw reply:\n{raw}"
            )
            last_error.__cause__ = e

    raise PlanGenerationError(
        f"Claude failed to produce a valid workout plan after {MAX_ATTEMPTS} attempts."
    ) from last_error