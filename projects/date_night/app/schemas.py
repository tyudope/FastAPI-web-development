from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class Theme(str, Enum):                 # str-valued → Claude sees "adventure", not 3
    COZY = "cozy"
    ROMANTIC = "romantic"
    ADVENTURE = "adventure"
    COMEDY = "comedy"
    FOOD = "food"
    UNIQUE = "unique"


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


# Request
class PlanRequest(StrictModel):
    theme: Theme = Field(default=Theme.COZY, description="Kind of date")
    energy_level: int = Field(default=3, ge=1, le=5, description="1=low, 5=high")
    budget: int = Field(..., ge=0, description="Total budget in PLN")
    city: str = Field(..., min_length=1, max_length=50, description="City for the date")
    user_context: str | None = Field(default=None, max_length=200, description="Optional extra context")


# Response
class DateIdea(StrictModel):
    title: str = Field(..., description="Short, catchy name for the date")
    description: str = Field(..., description="What you'll do, 1-3 sentences")
    estimated_cost: int = Field(..., ge=0, description="Estimated cost in PLN")


class PlanResponse(StrictModel):
    main_plan: DateIdea = Field(..., description="The primary date plan")
    backup_plan: DateIdea = Field(..., description="A fallback option")
    why_it_fits: str = Field(..., description="Why this suits both energy levels and the theme")