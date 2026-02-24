from app.schemas.order import RecommendOrderResponse
from app.models.order import PhaseOfDay





def recommender_user_prompt(phase_of_day : PhaseOfDay, mood:str | None, hungry:int) -> str:

    schema_json = RecommendOrderResponse.model_json_schema()

    return f"""

    You will recommend a meal to the user.

    Current Phase of Day: 
    {phase_of_day}

    Mood (Optional do nothing if user didn't provide)
    {mood}


    Hungry Level:
    {hungry}


    You will return a response exactly matching this JSON Schema
    {schema_json}

        """



