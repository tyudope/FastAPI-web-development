from pydantic import BaseModel, ConfigDict, Field


class GoalCreate(BaseModel):

    title:str = Field(..., max_length=50)
    description:str = Field(..., max_length=200)



class GoalOut(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id:int
    title:str
    description:str