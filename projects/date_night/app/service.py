from pydantic import ValidationError

from app.schemas import PlanResponse, PlanRequest
from app.prompts import SYSTEM_PROMPT, build_user_message
from app.claude_client import call_claude


class PlanGenerationError(Exception):
    """Claude's reply could not be turned into a valid PlanRespone."""


def _strip_fences(text: str) -> str:
    """Remove ```json ...``` fences if the model added them despite instructions."""
    text = text.strip()
    if text.startswith("```"):
        text = (
            text.removeprefix("```json")
            .removeprefix("```")
            .removesuffix("```")
            .strip()
        )

    return text




def generate_date_plan(req: PlanRequest) -> PlanResponse:
    user_msg = build_user_message(req)
    raw = call_claude(SYSTEM_PROMPT, user_msg)
    cleaned = _strip_fences(raw)

    try:
        return PlanResponse.model_validate_json(cleaned)
    except ValidationError as e:
        raise PlanGenerationError(
            f"Claude returned output that didn't fit PlanResponse. Raw reply:\n{raw}"
        ) from e
    
    