from pydantic import BaseModel, Field
from pydantic import ConfigDict
from enum import Enum

class Theme(Enum): 
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
    
    theme:Theme = Field(default = Theme.COZY)
    energy_level:int = Field(default = 3, ge=1, le = 5, description="1=low energy, 5=high")
    budget:int = Field(..., ge = 0, description="Total Budget in PLN")
    city:str = Field(..., min_length=3, max_length=100, description="The City where data took place")
    user_context:str | None = Field(default = None, max_length=200)

# Respone

class DateIdea(StrictModel):
    title:str = Field(..., description="Short, catchy name for the date.")
    description:str = Field(..., description="What you actually do, 1-3 sentences")
    estimated_cost:int = Field(..., ge=0, description="Estimated cost in PLN")


class PlanResponse(StrictModel):

    main_plan:DateIdea
    backup_plan:DateIdea
    why_it_fits:str = Field(..., description="Why this suits both energy levels and the theme.")