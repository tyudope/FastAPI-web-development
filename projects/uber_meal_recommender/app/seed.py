from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.order import Order, PhaseOfDay


ORDERS_TO_SEED =[ 
    {
        "meal_name" : "Kebab Box",
        "phase_of_day" : PhaseOfDay.morning,
        "cuisine" : "Turkish",
        "price_level" : 100
    },
    {
        "meal_name" : "Chicken Pizza",
        "phase_of_day" : PhaseOfDay.evening,
        "cuisine" : "Italian",
        "price_level" : 125
    },
    {
        "meal_name": "KFC Stripes 30 pieces",
        "phase_of_day" : PhaseOfDay.afternoon,
        "cuisine" : "USA",
        "price_level" : 110
    },
    {
        "meal_name" : "Starbucks Home Office",
        "phase_of_day" : PhaseOfDay.morning,
        "cuisine": "USA",
        "price_level" : 90
    }
]


def seed_orders(db: Session) -> None:
    """
    Insert initial orders into database.
    Safe to run multiple times.
    """


    for order_data in ORDERS_TO_SEED:
        # check if order is already exists.
        existing = db.scalar(
            select(Order).where(Order.meal_name == order_data["meal_name"])
            )
        
        if existing:
            continue

        order = Order(**order_data)
        db.add(order)

    db.commit()