from pydantic import Field, BaseModel, ConfigDict


class StrictModel(BaseModel):
    model_config = ConfigDict(extra = "forbid")


# SQLAlchemy Model

# Create
# The caller has the bok detail's but no id yet, and hasn't ready any pages. 
class BookCreate(StrictModel):
    model_config = ConfigDict(from_attributes=True)
    name:str = Field(..., max_length=50)
    category:str | None = Field(default = None, max_length=50)
    total_page:int = Field(...)
    finished_page:int  = Field(default=0) # or we don't need it ?

# Read
# This is what comes back from the database, so it's complete id present, everything populated.
class BookRead(StrictModel):
    model_config = ConfigDict(from_attributes=True)
    id:int = Field(...)
    name:str = Field(..., max_length=50)
    category:str | None = Field(default = None, max_length=50)
    total_page:int = Field(...)
    finished_page:int = Field(...)


# Update
# The caller wants to change something, maybe just one field.
class BookUpdate(StrictModel):
    model_config = ConfigDict(from_attributes=True)
    name:str | None = Field(default = None, max_length=50)
    category:str | None = Field(default = None, max_length=50)
    total_page:int | None = Field(default=None)
    finished_page:int| None = Field(default= None)


