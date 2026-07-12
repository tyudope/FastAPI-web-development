import anthropic
from app.config import settings


MODEL = "claude-haiku-4-5"
MAX_TOKENS = 2028


# Created once and reused, it manages connection pool

client = anthropic.Anthropic(api_key = settings.ANTHROPIC_API_KEY)


def call_claude(system:str, user:str) -> str:
    """
    Send a system + user prompt to Claude, return raw text reply.
    """


    try:
        messsage = client.messages.create(
            model = MODEL,
            max_tokens=MAX_TOKENS,
            system = system,
            messages = [{"role":"user", "content":user}],
        )
    except anthropic.APIError as e:
        raise RuntimeError(f"ClaudeAPI call failed {e}") from e
    

    return messsage.content[0].text