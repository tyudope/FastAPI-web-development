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


class Location(str, Enum):
    HOME = "home"
    GYM = "gym"
    OUTDOOR = "outdoor"
    


# Request
class WorkoutRequest(StrictModel):
    
    name:str | None = Field(default = None, min_length=3, max_length=50, description = "Person's name.") # Optional name.
    age: int = Field(..., ge = 13, le=80, description="Person's age")
    height: int = Field(..., ge=30, le = 250, description = "Person's height in terms of centimeters")
    weight: int = Field(..., ge = 30, le = 250, description = "Person's weight in terms of the kilograms")
    sex: Sex = Field(..., description="Biological sex, used to tailor training and calorie estimates")
    workout_days: set[Weekday] = Field(..., description = "List of training days.", min_length=1)
    preferred_location: Location = Field(default = Location.HOME, description = "User preferred working out location.")
    experience_level:int = Field(default = 3, ge = 1, le=5, description = "User fitness experience level between 1-5 (1 = NO EXPERIENCE, 5 = ADVANCED)")
    user_context: str | None = Field(default = None, min_length=5, max_length=200, description= "User personal context of the working out purpose.")
    


class Exercise(StrictModel):

    name:str = Field(..., min_length=2, max_length=40, description="Name of the exercise.")
    set_count:int = Field(..., ge=1, le=10, description="Number of sets that exercise performed")
    rep_count:int = Field(..., ge=1, le=50, description= "Number of repetition for the exercise per set.")
    rest_period:int = Field(..., ge= 10, le = 600, description = "Rest period between sets in seconds. ")



class Workout(StrictModel):
    name:str = Field(..., min_length=2, max_length=32, description = "Name of the workout. (i.e.  PUSH, PULL, UPPER etc..)")
    exercises:list[Exercise] = Field(..., min_length= 1, max_length=12, description = "List of Exercises")
    day:Weekday = Field(..., description="Day which Workout will be take place.")
    target_experience_level:int = Field(..., ge=1, le= 5,
                    description = "The expereicne level this day was designed for; must match the user's level. ")

class WorkoutResponse(StrictModel):
    
    workouts:list[Workout] = Field(..., min_length=1, max_length=7, description = "Workout programmes per training day.")
    reason:str = Field(..., min_length=100, max_length=1000, description = "Reason of why this type of program fits to the user's preferences." )
    pros:str = Field(..., min_length=10, max_length=400, description = "Pros of this workout plan.")
    cons:str = Field(..., min_length=10, max_length=400, description = "Cons of this workout plan.")
    
