from openai import OpenAI
from fastapi import APIRouter
from app.core.config import settings
import json

from app.prompts.prompt_templates import recommender_user_prompt
from app.prompts.prompt import SYSTEM_PROMPT
from app.schemas.order import RecommendOrderResponse, RecommendOrderRequest



client = OpenAI(api_key=settings.openai_api_key)



class ModelOutputError(Exception):
    pass


def _extract_json(text: str) -> dict:
    """
    Best-effort JSON extraction:
    - If model returns pure JSON -> json.loads works.
    - If model adds text accidentally -> try to slice the first {...} block.
    """
    text = text.strip()

    # Fast path: perfect JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Recovery path: extract the first JSON object
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ModelOutputError("No JSON object found in model output.")

    candidate = text[start:end + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as e:
        raise ModelOutputError(f"Invalid JSON after extraction: {e}") from e
    


def recommend_meal(request:RecommendOrderRequest):

    user_prompt = recommender_user_prompt(phase_of_day=request.phase_of_day, mood = request.mood, hungry=request.hungry)
    print(user_prompt)

    response = client.responses.create(
        model = settings.openai_model,
        input=[
            {"role" : "system" , "content": SYSTEM_PROMPT},
            {"role" : "user", "content" : user_prompt}
        ],
    )
    

    raw_text = response.output_text
    data = _extract_json(raw_text)


    # Hard guarantee: validate against your contract
    try:
        return RecommendOrderResponse.model_validate(data)
    except Exception as e:
        raise ModelOutputError(f"Model output failed schema validation: {e}") from e
