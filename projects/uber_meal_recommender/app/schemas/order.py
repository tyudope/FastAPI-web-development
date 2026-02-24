from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from pydantic import ConfigDict
from app.models.order import PhaseOfDay






class StrictModel(BaseModel):
    model_config = ConfigDict(extra = "forbid") # If anything extra, just throw an error.





class RecommendOrderRequest(StrictModel):


    phase_of_day : PhaseOfDay = Field(..., description = "Current Phase of Day it could be (morning, afternoon, evening) not anything else.")


    mood : str | None = Field(min_length=3, max_length=80   ,description="(Optional) user's current mood.")


    hungry: int = Field(..., ge=1, le = 5, description = "User's current hungry level.")





class RecommendOrderResponse(StrictModel):

    meal:str = Field(..., min_length=3, max_length=100, description="Full name of Meal.")

    summary: str = Field(..., min_length=15, max_length=400, description="Why I Recommend this meal Summarize it.")

