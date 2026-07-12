from pydantic import ValidationError

from app.schemas import WorkoutResponse, WorkoutRequest
from app.prompts import SYSTEM_PROMPT, build_user_message
from app.claude_client import call_claude



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




def generate_workout_plan(req: WorkoutRequest) -> WorkoutResponse:
    user_msg = build_user_message(req)
    raw = call_claude(SYSTEM_PROMPT, user_msg)
    cleaned = _strip_fences(raw)


    try:
        return WorkoutResponse.model_validate_json(cleaned)
    except ValidationError as e:
        raise PlanGenerationError(
            f"Claude returned output that didn't fitr WorkoutRespone. Raw reply:\n{raw}"
        ) from e