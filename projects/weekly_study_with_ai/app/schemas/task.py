from pydantic import BaseModel # Every schema will inherit from this.
from pydantic import Field # is used to add validation rules and metadata
from pydantic import ConfigDict # allows pydantic to read SQLAlchemy objects.


class TaskCreate(BaseModel):

    name:str = Field(..., max_length=50)
    description:str = Field(..., max_length=200)



# 
class TaskOut(BaseModel):

    model_config = ConfigDict(from_attributes=True) # allows Pydantic to read ORM attributes (e.g., task.name)

    id:int
    name:str
    description:str