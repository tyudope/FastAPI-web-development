from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class StrictModel(BaseModel):
    model_config = ConfigDict(extra = "forbid")



class Weekday(str, Enum):

    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"
    

class Sex(str, Enum):
    MALE = "male"
    FEMALE = "female"



class WorkoutRequest(StrictModel):
    
    name:str | None = Field(default = None, min_length=3, max_length=50, description = "Person's name.") # Optional name.
    age: int = Field(..., ge = 13, le=80, description="Person's age")
    height: int = Field(..., ge=30, le = 250, description = "Person's height in terms of centimeters")
    weight: int = Field(..., ge = 30, le = 250, description = "Person's weight in terms of the kilograms")
    sex: Sex = Field(..., description="Biological sex, used to tailor training and calorie estimates")
    workout_days: set[Weekday] = Field(..., description = "List of training days.", min_length=1)
    user_context: str | None = Field(default = None, min_length=5, max_length=200, description= "User personal context of the working out purpose.")
    



class WorkoutResponse(StrictModel):
    pass