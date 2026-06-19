import json
from app.schemas import PlanRequest, PlanResponse
RESPONSE_SCHEMA = json.dumps(PlanResponse.model_json_schema(), indent = 2)



SYSTEM_PROMPT = f"""You are a thoughtful date-night planner.

Design a date that fits BOTH partners' energy levels and the chosen theme, stays \ 
within the stated budget, and is specific to their city (name real types of places, \
not generic filler). Always provide a main plan and a realistic backup plan.

estimated_cost is an integer in PLN, and both plans must stay within the budget.

Respond with ONLY a JSON object conforming to this schema — no markdown, no code \
fences, no text before or after:

{RESPONSE_SCHEMA}
"""




def build_user_message(req: PlanRequest) -> str:

    lines = [
        f"Theme: {req.theme}",
        f"Energ level (1-5): {req.energy_level}",
        f"Budget: {req.budget} PLN",
        f"City: {req.city}",
    ]

    if req.user_context:
        lines.append(f"Extra context: {req.user_context}")

    return "\n".join(lines)

