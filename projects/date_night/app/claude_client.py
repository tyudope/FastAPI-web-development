import anthropic
from app.config import settings


MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024



# Created once and reused, it mnanages a connection pool.

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

def call_claude(system:str, user:str) -> str:

    """Send a system + user prompt to Claude, return the raw text reply.
    
    Deliberately generic: it knows nothing about PlanResponse.
    Parsing/validation lives one layer up, so this stays reusable.
    """

    try:
        message = client.messages.create(
            model = MODEL,
            max_tokens=MAX_TOKENS,
            system = system,
            messages = [{"role":"user", "content":user}],
        )
    except anthropic.APIError as e:
        raise RuntimeError(f"Claude API call failed: {e}") from e
    

    return message.content[0].text

