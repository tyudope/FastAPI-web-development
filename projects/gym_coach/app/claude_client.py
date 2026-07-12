import anthropic
from app.config import settings


MODEL = "claude-sonnet-4-5"
# A full 7-day plan (7 workouts x up to 12 exercises, plus a long reason/pros/cons)
# can run to ~3500-4000 output tokens. Keep real headroom so replies don't get cut
# off mid-JSON, which produced invalid (unparsable) responses at the old 2028 cap.
MAX_TOKENS = 3000


# Created once and reused, it manages connection pool

client = anthropic.Anthropic(api_key = settings.ANTHROPIC_API_KEY)


class ClaudeTruncatedError(RuntimeError):
    """Claude's reply was cut off before it finished (hit the max_tokens cap)."""


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

    if messsage.stop_reason == "max_tokens":
        raise ClaudeTruncatedError(
            f"Claude's reply was truncated at {MAX_TOKENS} max_tokens before finishing."
        )

    return messsage.content[0].text