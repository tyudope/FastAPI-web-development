from pydantic import BaseModel
from pydantic import Field
from pydantic import ConfigDict



# Pydantic schema which we use for the creating (POST) request.
class VehicleCreate(BaseModel):
    make:str = Field(..., max_length=100)
    horse_power:int = Field(..., lt=2000, gt = 10)
    price:int = Field(..., gt = 0)
    door_count:int = Field(..., gt=0)
    car_model:str = Field(..., max_length=100)


# Pydantic schema which we use for the updating (PUT) request.
class VehicleUpdate(BaseModel):
    make: str | None = Field(default = None, max_length=100)
    horse_power: int | None = Field(default = None, gt = 10, lt = 2000)
    price:int | None = Field(default = None, gt = 0)
    door_count:int | None = Field(default = None, gt = 0)
    car_model:str | None = Field(default = None, max_length=100)





# Pydantic schema which we use for the returning (GET) request.
class VehicleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True) # Pydantic must know how to read attributes from that object.
    id:int
    make:str = Field(..., max_length=100)
    horse_power:int = Field(..., lt=2000, gt=10)
    price:int = Field(..., gt = 0)
    door_count:int = Field(..., gt= 0)
    car_model:str = Field(..., max_length=100)



