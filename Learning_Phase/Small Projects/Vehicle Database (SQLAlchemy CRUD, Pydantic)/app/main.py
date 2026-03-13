from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from app.db.session import engine, get_db

from app.models.models import Base
from app.models.models import Vehicle

from app.schemas.schemas import VehicleCreate, VehicleOut, VehicleUpdate


from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import delete

from typing import List



app = FastAPI(title = "Vehicle")


@app.get("/health")
def health():
    return {"status" : "live"}


@app.post("/vehicles", response_model=VehicleOut)
def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    # Convert validated Pydantic data into SQLAlchemy model
    db_vehicle = Vehicle(**vehicle.model_dump())

    # Add object to current database session
    db.add(db_vehicle)

    # Save transaction permanently
    db.commit()

    # Reload object from DB to get generated values like id
    db.refresh(db_vehicle)

    # Return ORM object; FastAPI converts it using VehicleOut
    return db_vehicle


@app.get("/vehicles", response_model=list[VehicleOut])
def get_vehicles(db: Session = Depends(get_db)):
    # Select all vehicle rows from database
    vehicles = db.scalars(select(Vehicle)).all()

    # Return list of ORM objects
    return vehicles

@app.get("/vehicles/{vehicle_id}", response_model = VehicleOut)
def get_vehicle_by_id(vehicle_id : int, db:Session = Depends(get_db)):

    # Select car with the given id.
    vehicle = db.scalar(select(Vehicle).where(Vehicle.id == vehicle_id))
    if vehicle is None:
        raise HTTPException(status_code=404, detail = "Vehicle is not found.")
    return vehicle


@app.delete("/vehicles/{vehicle_id}", response_model = VehicleOut)
def delete_vehicle_by_id(vehicle_id: int, db:Session = Depends(get_db)):

    # Find vehicle with the given id
    vehicle = db.scalar(select(Vehicle).where(Vehicle.id == vehicle_id))
    
    if vehicle is None:
        raise HTTPException(status_code = 404, detailt = "Vehicle with the given id is not found.")
    
    # Delete the ORM object.
    db.delete(vehicle)
    db.commit()

    return vehicle



@app.put("/vehicles/{vehicle_id}", response_model=VehicleOut)
def update_vehicle_by_id(
    vehicle_id:int,
    vehicle_update: VehicleUpdate,
    db:Session = Depends(get_db)
):
    # Find vehicle with the given id
    vehicle = db.scalar(select(Vehicle).where(Vehicle.id == vehicle_id))

    if vehicle is None:
        raise HTTPException(status_code=404, detail = "Vehicle with the given id is not found.")
    
    # Get only fields providede in the request body.
    update_data = vehicle_update.model_dump(exclude_unset=True)

    # Apply updated values to the ORM object.
    for key, value in update_data.items():
        setattr(vehicle, key, value)

    # Save changes
    db.commit()

    db.refresh(vehicle)

    return vehicle


@app.on_event("startup")
def on_startup():
    # Create a tables.
    Base.metadata.create_all(bind=engine)