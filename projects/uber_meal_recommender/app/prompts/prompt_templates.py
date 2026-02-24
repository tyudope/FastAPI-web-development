from app.schemas.order import RecommendOrderResponse
from app.models.order import PhaseOfDay

from app.db.get_all import get_all_orders




def recommender_user_prompt(
    phase_of_day: PhaseOfDay,
    mood: str | None,
    hungry: int,
    previous_orders=None,
) -> str:
    if previous_orders is None:
        previous_orders = get_all_orders()

    schema_json = RecommendOrderResponse.model_json_schema()

    return f"""

    You will recommend a meal to the user.

    Current Phase of Day: 
    {phase_of_day}

    Mood (Optional do nothing if user didn't provide)
    {mood}


    Hungry Level:
    {hungry}

    "User's previous orders."
    {previous_orders}

    You will return a response exactly matching this JSON Schema
    {schema_json}

        """


