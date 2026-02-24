from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.order import Order


def get_all_orders() -> list[dict]:
    db = SessionLocal()
    try:
        orders = db.scalars(select(Order)).all()
        return [
            {
                "meal_name": o.meal_name,
                "phase_of_day": o.phase_of_day.value,
                "cuisine": o.cuisine,
                "price_level": o.price_level,
            }
            for o in orders
        ]
    finally:
        db.close()


