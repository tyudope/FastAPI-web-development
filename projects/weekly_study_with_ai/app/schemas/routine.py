from pydantic import Field, BaseModel, ConfigDict


class RoutineCreate(BaseModel):

    title:str = Field(..., max_length=50)



class RoutineOut(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    id:int
    title:str
    goal_id:int
    
